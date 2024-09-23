from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, MenuItemForm
from .models import Category, MenuItem, Order, OrderItem,User,Blog
from django.contrib import messages
import datetime
from decimal import Decimal
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib.auth.models import User ,auth
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required
from .email_utils import send_order_confirmation_email, send_admin_order_notification



def health_check(request):
    return HttpResponse("OK", status=200)


@csrf_exempt
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        
        # Save the blog post
        Blog.objects.create(title=title, image=image, description=description)
        return redirect('dashboard')  # Redirect to a success page or the blog list

    return render(request, 'create_blog.html')

@csrf_exempt
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        
        # Check if a new image is uploaded
        new_image = request.FILES.get('image')
        if new_image:
            blog.image = new_image
        
        blog.description = request.POST.get('description')
        blog.save()
        return redirect('blog_list')  # Redirect to the blog list after editing
    
    return render(request, 'edit_blog.html', {'blog': blog})

@csrf_exempt
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('blog_list')
    

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_items(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_items.html', {'blogs': blogs})

def events(request):
    return render(request, 'events.html')

@csrf_exempt
def add_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Check if phone number already exists in the database
        existing_user = User.objects.filter(phone_number=phone_number).first()
        if existing_user and existing_user != request.user:
            messages.error(request, 'Phone number is already taken.')
            return redirect('add_phone_number')

        # Save phone number to user profile
        if phone_number:
            request.user.phone_number = phone_number
            request.user.save()
            return redirect('/')  # Redirect to home after saving phone number

    return render(request, 'add_phone_number.html')

User = get_user_model()
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_details.html', {'order': order})

def users_table(request):
    users =User.objects.all()
    return render(request,'users.html',{'users':users})
def orders_table(request):
    orders = Order.objects.all().prefetch_related('items__menu_item')
    return render(request, 'orders_table.html', {'orders': orders})

def back(request):
    return redirect('/')

def dashboard(request):
    # Fetch counts
    category_count = Category.objects.count()
    menu_item_count = MenuItem.objects.count()

    # Fetch recent orders (example: last 10 orders)
    recent_orders = Order.objects.all().order_by('created_at')[:10]

    context = {
        'category_count': category_count,
        'menu_item_count': menu_item_count,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def supervisorlogout(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def supervisor(request):
    if request.method =='POST':
        username =request.POST['username']
        password =request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if  user is not None:
            if user.is_staff:
              auth.login(request,user)
              return redirect ("dashboard")
            else:
              messages.info(request,'You are not authorized  to  access this page.')
              return redirect('supervisor')
        else:
          messages.info(request, 'You are not authorized  to  access this page.')
          return redirect('supervisor')
    else:
        return render(request,'admin.html')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(phone_number=phone_number).exists():
                messages.info(request, 'Phone number is already taken')
                context={
                    'first_name':first_name,
                    'phone_number':phone_number,
                    'username':username,
                    'email':email   
                }
                return render(request,'signup.html',context)
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                context={
                    'first_name':first_name,
                    'phone_number':phone_number,
                    'username':username,
                    'email':email   
                }
                return render(request,'signup.html',context)
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                context={
                    'first_name':first_name,
                    'phone_number':phone_number,
                    'username':username,
                    'email':email   
                }
                return render(request,'signup.html',context)
            
            user = User.objects.create_user(
                phone_number=phone_number,
                password=password1,
                first_name=first_name,
                email=email,
                username=username
            )
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Passwords do not match')
            context={
                    'first_name':first_name,
                    'phone_number':phone_number,
                    'username':username,
                    'email':email   
                }
            return render(request,'signup.html',context)
    
    return render(request, 'signup.html')



@csrf_exempt
def log(request):
    if request.method == 'POST':
        phone_number =request.POST.get('phone_number')
        password =request.POST.get('password')

        user = auth.authenticate(phone_number=phone_number,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")
            context={
                'phone_number':phone_number
            }
            return render(request,'login.html',context)

    return render(request,'login.html')



def index(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'index.html', context)

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('add_category')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@csrf_exempt
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():  
            form.save()
            messages.success(request, 'Menu item added successfully.')
            return redirect('add_menu_item')
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form})

def menu_items(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    
    cart = request.session.get('cart', {})
    
    # Pass the cart (which contains saved quantities) to the template
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'cart': cart,
    }
    
    return render(request, 'menu.html', context)


# @csrf_exempt
# def menu_items(request):
#     if request.method == 'POST':
#         selected_items = request.POST.getlist('menu_items')
#         quantities = request.POST.getlist('quantities')

#         cart_items = request.session.get('cart_items', [])
#         total_price = Decimal(request.session.get('total_price', 0.00))

#         new_cart_items = []
#         total_items_count = 0

#         # Filter out items where the quantity is greater than 0
#         for item_id, quantity in zip(selected_items, quantities):
#             if int(quantity) > 0:  # Add only if quantity is greater than 0
#                 item = MenuItem.objects.get(id=item_id)
#                 item_total_price = item.price * Decimal(quantity)
#                 total_price += item_total_price
#                 total_items_count += int(quantity)  # Increment item count
#                 new_cart_items.append({
#                     'menu_item': item.dish_name,
#                     'quantity': quantity,
#                     'price': float(item_total_price)
#                 })

#         # Update session with new items and total price
#         if new_cart_items:
#             cart_items.extend(new_cart_items)
#             request.session['cart_items'] = cart_items
#             request.session['total_price'] = float(total_price)
#             request.session['total_items_count'] = total_items_count

#         # Redirect to the bag (or cart) page or remain on the menu page
#         return redirect('menu_items')
#     return redirect('menu_items')


# @require_POST
# def add_to_bag(request):
#     data = json.loads(request.body)
#     dish_id = str(data.get('dish_id'))  # Convert to string for session keys
#     action = data.get('action')

#     # Retrieve or initialize the bag from the session
#     bag = request.session.get('bag', {})
#     total_items_count = request.session.get('total_items_count', 0)

#     if action == 'selected':
#         # If dish is already in the bag, increase quantity
#         if dish_id in bag:
#             bag[dish_id] += 1
#         else:
#             bag[dish_id] = 1  # Add dish with a quantity of 1
#         total_items_count += 1
#     elif action == 'unselected':
#         # Remove dish if it's in the bag
#         if dish_id in bag:
#             total_items_count -= bag[dish_id]  # Reduce total by item quantity
#             del bag[dish_id]  # Remove the item completely

#     # Update the session with new bag contents and item count
#     request.session['bag'] = bag
#     request.session['total_items_count'] = total_items_count
#     request.session.modified = True  # Mark session as modified to trigger save

#     return JsonResponse({
#         'total_items_count': total_items_count,
#         'item_quantity': bag.get(dish_id, 0)  # Return updated quantity for the item
#     })

@csrf_exempt
def add_to_bag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dish_id = str(data['dish_id'])  # Convert to string for consistency with session
        action = data['action']

        # Ensure the session 'bag' is a dictionary
        bag = request.session.get('bag', {})

        # If bag is not a dictionary, reinitialize it
        if not isinstance(bag, dict):
            bag = {}

        total_items_count = request.session.get('total_items_count', 0)

        if action == 'selected':
            # Add or increment the item in the bag
            if dish_id in bag:
                bag[dish_id] += 1  # Increment the quantity
            else:
                bag[dish_id] = 1  # Add a new item with a quantity of 1
            total_items_count += 1
        elif action == 'unselected':
            if dish_id in bag:
                total_items_count -= bag[dish_id]  # Adjust the count
                del bag[dish_id]  # Remove the item from the bag

        # Update the session with the new bag and item count
        request.session['bag'] = bag
        request.session['total_items_count'] = total_items_count

        return JsonResponse({'total_items_count': total_items_count})


# @login_required(login_url='log')
# def view_bag(request):
#     # Retrieve the bag from the session
#     bag = request.session.get('bag', {})
#     items = []

#     # Fetch the items from the database
#     if bag:
#         for dish_id in bag.items():
#             dish = MenuItem.objects.get(id=dish_id)
#             items.append({
#                 'id': dish.id,
#                 'name': dish.dish_name,
                
#             })

#     # Handle order placement
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return JsonResponse({'success': False, 'message': "Please login to place the order."}, status=403)

#         if bag:
#             # Create a new order
#             order = Order.objects.create(user=request.user)
            
#             # Add order items
#             for dish_id in bag.items():
#                 dish = get_object_or_404(MenuItem, id=dish_id)
#                 OrderItem.objects.create(order=order, menu_item=dish)

#             # Clear the bag after the order is placed
#             request.session['bag'] = {}
#             request.session['total_items_count'] = 0
#             request.session.modified = True

#             # Set a session variable to show a success popup
#             request.session['show_popup'] = True

#             # Return a success JSON response
#             return JsonResponse({'success': True})

#     # Check if the popup should be displayed
#     show_popup = request.session.pop('show_popup', False)

#     context = {
#         'items': items,
#         'show_popup': show_popup
#     }

#     return render(request, 'view_bag.html', context)

@csrf_exempt

def view_bag(request):
    # Retrieve the bag from the session
    bag = request.session.get('bag', [])
    items = []

    # If there are any items in the bag
    if bag:
        for dish_id in bag:
            dish = MenuItem.objects.get(id=dish_id)  # Fetch the dish from the database
            items.append({
                'name': dish.dish_name
            })
    else:
        items = None

    # Handle POST request for placing an order
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': "Please login to place the order."}, status=403)

        if bag:
            # Create a new order
            order = Order.objects.create(
                user=request.user
            )
            
            # Add order items (only using menu_item, no quantity or total)
            for dish_id in bag:
                dish = MenuItem.objects.get(id=dish_id)
                OrderItem.objects.create(
                    order=order,
                    menu_item=dish
                )
            
            # Clear the bag after placing the order
            request.session['bag'] = []
            request.session['total_items_count'] = 0

            # Set session variable to trigger popup
            request.session['show_popup'] = True

            # Send confirmation email
            send_order_confirmation_email(order, request.user.email)
            send_admin_order_notification(order)

            # Return a success JSON response
            return JsonResponse({'success': True})

    # Check if the popup should be displayed
    show_popup = request.session.pop('show_popup', False)

    context = {
        'items': items,
        'show_popup': show_popup
    }
    
    return render(request, 'view_bag.html', context)


@csrf_exempt
def order_successful(request):
    order_items = request.session.get('order_items')
    total_price = request.session.get('total_price')
    user = request.user

    if not order_items or not total_price:
        return redirect('menu_items')
    

    # Create the order in the database
    order = Order.objects.create(
        user =user,
        total_price=Decimal(total_price),
        created_at=datetime.datetime.now(),
    ) 

    # Create order items
    for item in order_items:
        menu_item = MenuItem.objects.get(id=item['menu_item_id'])
        OrderItem.objects.create(order=order, menu_item=menu_item, quantity=item['quantity'])

    # Clear session data after creating the order
    del request.session['order_items']
    del request.session['total_price']

        # Send order confirmation email
    subject = 'Order Summary'
    html_message = render_to_string('order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'user': user,
    })
    plain_message = strip_tags(html_message)
    from_email = 'madhuramKitchens.com@gmail.com'
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    
    subject_admin = 'New Order Placed'
    html_message_admin = render_to_string('order_placed_email.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'user': user,
    })
    plain_message_admin = strip_tags(html_message_admin)
    to_admin = 'madhuramKitchens.com@gmail.com'  

    send_mail(subject_admin, plain_message_admin, from_email, [to_admin], html_message=html_message_admin)

    return render(request, 'order_successful.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'user':user
    })



def edit_items(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'edit_menuitems.html', context)

@csrf_exempt
def edit_menuitem(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('edit_items')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'add_menu_item.html', {'form': form, 'menu_item': menu_item})

@csrf_exempt
def delete_menuitem(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('edit_items')
    return render(request, 'delete_menuitem.html', {'menu_item': menu_item})

@csrf_exempt
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@csrf_exempt
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')

@csrf_exempt
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})



