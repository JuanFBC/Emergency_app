# Generated by Django 4.2.7 on 2024-11-25 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_localidad_remove_seguimiento_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('users', models.CharField(max_length=200)),
                ('pagina', models.CharField(max_length=255)),
                ('fecha', models.DateTimeField()),
            ],
        ),
    ]
