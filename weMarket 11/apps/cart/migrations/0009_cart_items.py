# Generated by Django 2.1.4 on 2019-06-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='cart.CartItem'),
        ),
    ]
