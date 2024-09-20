from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField  # type: ignore

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class User(AbstractUser):
    phone_number = PhoneNumberField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='pics/', null=True, blank=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    DISH_TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('green_leafy', 'Green Leafy Vegetables'),
    ]
    dish_type = models.CharField(max_length=20, choices=DISH_TYPE_CHOICES, default='veg')
    dish_name = models.CharField(max_length=100)
    description = models.TextField()
    # Use FloatField to avoid Djongo issues with DecimalField
    # price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    recommended_dish = models.BooleanField(default=False)

    def __str__(self):
        return self.dish_name

    class Meta:
        unique_together = ('dish_name', 'category')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.dish_name}"
    
    
    
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField  # type: ignore

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class User(AbstractUser):
    phone_number = PhoneNumberField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='pics/', null=True, blank=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    DISH_TYPE_CHOICES = [
        (1, 'Vegetarian'),
        (2, 'Non-Vegetarian'),
        (3, 'Green Leafy Vegetables'),
    ]
    Category_TYPE_CHOICES = [
        (1, 'Biryani'),
        (2, 'Curries'),
        (3, 'Drinks'),
    ]
    dish_type = models.IntegerField(choices=DISH_TYPE_CHOICES, default=1)
    dish_name = models.CharField(max_length=100)
    description = models.TextField()
    # Use FloatField to avoid Djongo issues with DecimalField
    #price = models.FloatField()
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category =models.IntegerField(choices=Category_TYPE_CHOICES,default=1)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    # Changing BooleanField to IntegerField for compatibility with MongoDB
    recommended_dish = models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0)

    def __str__(self):
        return self.dish_name

    def is_recommended(self):
        return self.recommended_dish == 1

    def get_recommended_dish_display(self):
        return 'Yes' if self.recommended_dish == 1 else 'No'

    def __str__(self):
        return self.dish_name

    class Meta:
        unique_together = ('dish_name', 'category')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.dish_name}"

"""
