# Generated by Django 4.2 on 2023-04-22 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineShop', '0010_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='photo'),
        ),
    ]
