# Generated by Django 3.0.2 on 2021-11-23 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0005_auto_20211122_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='slug',
        ),
    ]
