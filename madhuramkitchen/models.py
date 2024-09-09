from django.db import models
from django.contrib.auth.models import AbstractUser,User
from phonenumber_field.modelfields import PhoneNumberField # type: ignore

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title

class User(AbstractUser):
    phone_number =PhoneNumberField()


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
     dish_type = models.CharField(max_length=20, choices=DISH_TYPE_CHOICES,default='veg')
     dish_name = models.CharField(max_length=100)
     description = models.TextField()
     price = models.DecimalField(max_digits=10, decimal_places=2)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
     recommended_dish =models.BooleanField(default=False)
     def __str__(self):
            return self.dish_name

     class Meta:
        unique_together = ('dish_name', 'category')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.dish_name}"
    




