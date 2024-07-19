from django import forms
from .models import Category, MenuItem, Order

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['dish_name','dish_type','recommended_dish','description', 'price', 'category', 'image']

    def clean_title(self):
        dish_name = self.cleaned_data.get('dish_name')
        category = self.cleaned_data.get('category')
        if MenuItem.objects.filter(dish_name=dish_name, category=category).exists():
            raise forms.ValidationError("Menu item with this title already exists in this category.")
        return dish_name
         
    def clean_dish_type(self):
        dish_type = self.cleaned_data.get('dish_type')
        if dish_type not in ['veg', 'non_veg', 'green_leafy']:
            raise forms.ValidationError("Invalid dish type.")
        return dish_type