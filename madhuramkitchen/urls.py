from django.urls import path, include
from .views import index,add_category, add_menu_item, menu_items, order_successful, log,signup,logout,supervisor, \
supervisorlogout, orders_table,users_table,back,dashboard,add_phone_number,create_blog,edit_blog,blog_list,delete_blog, \
blog_items, events, edit_items,edit_menuitem,delete_menuitem,category_list,delete_category,edit_category,view_bag,add_to_bag


urlpatterns = [
    path('', index, name='index'),
    path('log',log,name='log'),
    path('add_phone_number',add_phone_number,name='add_phone_number'),
    path('signup',signup,name='signup'),
    path('logout',logout,name='logout'),
    path('supervisorlogout',supervisorlogout,name='supervisorlogout'),
    path('supervisor',supervisor,name='supervisor'),
    path('orders_table',orders_table,name="orders_table"),
    path('users_table',users_table,name='users_table'),
    path('back',back,name='back'),
    path('dashboard',dashboard,name='dashboard'),
    path('create_blog',create_blog,name='create_blog'),
    path('edit/<int:pk>/', edit_blog, name='edit_blog'),
    path('delete_blog/<int:pk>/',delete_blog, name='delete_blog'),
    path('blog_list',blog_list,name='blog_list'),
    path('blog_items',blog_items,name='blog_items'),
    path('events',events,name='events'),
    path('edit_items',edit_items,name="edit_items"),
    path('add_category', add_category, name='add_category'),
    path('add_menu_item', add_menu_item, name='add_menu_item'),
    path('menu_items/', menu_items, name='menu_items'),
    path('edit_menuitem/<int:item_id>/', edit_menuitem, name='edit_menuitem'),
    path('delete_menuitmem/<int:item_id>/',delete_menuitem, name='delete_menuitem'),
    path('order_successful/', order_successful, name='order_successful'),  # Updated from place_order
    path('category_list', category_list, name='category_list'),
    path('categories/delete/<int:pk>/', delete_category, name='delete_category'),
    path('categories/edit/<int:pk>/', edit_category, name='edit_category'),
    path('view_bag', view_bag, name='view_bag'),
    path('add_to_bag', add_to_bag, name='add_to_bag'),
]
