# Generated by Django 3.0.2 on 2021-11-23 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0007_categoria_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[('1', 'Receita'), ('2', 'Despesa')], default=1),
        ),
    ]
