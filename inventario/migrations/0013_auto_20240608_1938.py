# Generated by Django 2.0.2 on 2024-06-08 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_auto_20240607_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='estado_producto',
            field=models.CharField(blank=True, default='Bueno', max_length=100, null=True),
        ),
    ]
