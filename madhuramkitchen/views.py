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


def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        
        # Save the blog post
        Blog.objects.create(title=title, image=image, description=description)
        return redirect('dashboard')  # Redirect to a success page or the blog list

    return render(request, 'create_blog.html')


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



def log(request):
    if request.method == 'POST':
        phone_number =request.POST['phone_number']
        password =request.POST['password']

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
    error_message = None

    if request.method == 'POST':
        selected_items = request.POST.getlist('menu_items')
        quantities = request.POST.getlist('quantities')

        if not selected_items:
            error_message = "Please select at least one item."
        else:
            order_items = []
            total_price = Decimal('0.00')
            valid_order = False

            for item_id, quantity in zip(selected_items, quantities):
                if int(quantity) > 0:  # Ensure that the quantity is greater than 0
                    valid_order = True
                    item = MenuItem.objects.get(id=item_id)
                    item_total_price = item.price * Decimal(quantity)
                    total_price += item_total_price
                    order_items.append({
                        'menu_item_id': item.id,
                        'menu_item_dish_name': item.dish_name,
                        'quantity': quantity,
                        'price': float(item_total_price)
                    })

            if valid_order:
                # Save order details in session
                request.session['order_items'] = order_items
                request.session['total_price'] = float(total_price)
                # Redirect to order successful page
                return redirect('order_successful')
            else:
                error_message = "Please select at least one item with a quantity greater than 0."

    return render(request, 'menu_items.html', {
        'menu_items': menu_items,
        'categories': categories,
        'error_message': error_message
    })

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

def delete_menuitem(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('edit_items')
    return render(request, 'delete_menuitem.html', {'menu_item': menu_item})