# Generated by Django 2.1.4 on 2019-06-21 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_auto_20190620_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='id_productos_fk',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='id_cart_fk',
            field=models.ForeignKey(blank=True, db_column='id_cart_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart'),
        ),
    ]