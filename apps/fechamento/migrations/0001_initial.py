# Generated by Django 4.0 on 2022-01-08 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fechamento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(db_index=True, max_length=50, unique=True)),
                ('mes_ano', models.DateField()),
                ('saldo_anterior', models.DecimalField(decimal_places=2, default=0.0, max_digits=13)),
                ('entradas', models.DecimalField(decimal_places=2, default=0.0, max_digits=13)),
                ('saidas', models.DecimalField(decimal_places=2, default=0.0, max_digits=13)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=13)),
                ('fechado', models.BooleanField(default=False)),
            ],
        ),
    ]