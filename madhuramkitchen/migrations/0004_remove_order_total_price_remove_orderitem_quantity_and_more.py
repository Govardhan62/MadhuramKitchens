# Generated by Django 5.1 on 2024-09-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('madhuramkitchen', '0003_rename_recommened_dish_menuitem_recommended_dish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]