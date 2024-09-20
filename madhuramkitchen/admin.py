# Register your models here.
from django.contrib import admin
from .models import Category, Order, OrderItem, MenuItem,Blog
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ckeditor.widgets import CKEditorWidget
from .models import User

from ckeditor.widgets import CKEditorWidget
from django import forms

class BlogAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm

admin.site.register(Blog, BlogAdmin)

class UserAdmin(BaseUserAdmin):
    # Customize the admin options here if necessary
    pass

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('dish_name','category')
    list_filter = ('category', 'dish_type')
    search_fields = ('dish_name', 'description')
admin.site.register(User, UserAdmin)