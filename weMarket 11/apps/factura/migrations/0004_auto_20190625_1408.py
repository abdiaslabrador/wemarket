# Generated by Django 2.1.4 on 2019-06-25 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0003_auto_20190625_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='activa',
            field=models.BooleanField(default=True),
        ),
    ]