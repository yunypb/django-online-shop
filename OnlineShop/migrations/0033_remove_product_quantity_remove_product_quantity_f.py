# Generated by Django 4.2 on 2023-08-15 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineShop', '0032_alter_category_brands_slug_alter_category_for_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity_f',
        ),
    ]
