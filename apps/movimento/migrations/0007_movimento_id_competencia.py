# Generated by Django 4.0.1 on 2022-02-03 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fechamento', '0002_alter_fechamento_options_remove_fechamento_nome_and_more'),
        ('movimento', '0006_alter_movimento_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimento',
            name='id_competencia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='fechamento.fechamento'),
            preserve_default=False,
        ),
    ]
