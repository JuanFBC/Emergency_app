# Generated by Django 5.1.2 on 2024-12-03 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_administrador_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seguimiento',
            old_name='id_colaborador',
            new_name='id_colaborador_id',
        ),
    ]
