# Generated by Django 2.0.2 on 2024-06-02 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_auto_20240527_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='pago',
        ),
        migrations.DeleteModel(
            name='Pago',
        ),
    ]
