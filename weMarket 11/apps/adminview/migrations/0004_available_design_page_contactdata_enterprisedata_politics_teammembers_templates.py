# Generated by Django 2.2.1 on 2019-06-30 18:57

import apps.adminview.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminview', '0003_available_design_page_contactdata_enterprisedata_teammembers_templates'),
    ]

    operations = [
        
        migrations.CreateModel(
            name='politics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conditions', models.TextField(blank=True, null=True)),
                ('cookies', models.TextField(blank=True, null=True)),
                ('privacy', models.TextField(blank=True, null=True)),
            ],
        ),
    ]