from django.urls import path, include
from .views import index, health_check,add_category, add_menu_item, menu_items, order_successful, log,signup,logout,supervisor, \
supervisorlogout, orders_table,users_table,back,dashboard,add_phone_number,create_blog,edit_blog,blog_list,delete_blog, \
blog_items, edit_items,edit_menuitem,delete_menuitem


urlpatterns = [
    path('', index, name='index'),
    path('health/', health_check, name='health_check'),
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
    path('edit_items',edit_items,name="edit_items"),
    path('add_category', add_category, name='add_category'),
    path('add_menu_item', add_menu_item, name='add_menu_item'),
    path('menu_items/', menu_items, name='menu_items'),
    path('edit_menuitem/<int:item_id>/', edit_menuitem, name='edit_menuitem'),
    path('delete_menuitmem/<int:item_id>/',delete_menuitem, name='delete_menuitem'),
    path('order_successful/', order_successful, name='order_successful'),  # Updated from place_order
]
