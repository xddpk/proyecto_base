# Generated by Django 2.0.2 on 2024-05-02 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20240502_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_name',
        ),
    ]
