# Generated by Django 2.1.4 on 2019-07-05 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0016_auto_20190705_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='factura',
            name='hora',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
