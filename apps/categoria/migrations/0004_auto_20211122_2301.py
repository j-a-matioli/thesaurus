# Generated by Django 3.0.2 on 2021-11-23 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0003_auto_20211121_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nome',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
    ]