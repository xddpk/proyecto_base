# Generated by Django 2.0.2 on 2024-05-13 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0008_producto_codigo_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo_producto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
