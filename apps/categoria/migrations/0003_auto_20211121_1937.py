# Generated by Django 3.0.2 on 2021-11-21 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0002_auto_20211121_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]