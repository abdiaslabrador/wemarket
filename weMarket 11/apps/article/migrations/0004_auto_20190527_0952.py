# Generated by Django 2.1.4 on 2019-05-27 13:52

import apps.article.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20190527_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='nombre_imagen',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=apps.article.models.upload_location, width_field='width_field'),
        ),
    ]