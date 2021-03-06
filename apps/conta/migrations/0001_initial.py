# Generated by Django 3.0.2 on 2021-11-24 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0009_auto_20211123_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(db_index=True, max_length=50, unique=True)),
                ('descricao', models.CharField(max_length=255)),
                ('status', models.BooleanField(choices=[(True, 'Ativa'), (False, 'Inativa')], default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='categoria.Categoria')),
            ],
        ),
    ]
