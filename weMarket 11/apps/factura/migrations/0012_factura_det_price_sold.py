# Generated by Django 2.1.4 on 2019-07-04 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0011_auto_20190704_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura_det',
            name='price_sold',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]