# Generated by Django 4.2 on 2023-04-20 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineShop', '0004_sex_alter_product_size_product_sex'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Category_brands',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='category_brands',
        ),
    ]
