# Generated by Django 4.2 on 2023-04-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineShop', '0019_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost',
            field=models.IntegerField(null=True),
        ),
    ]
