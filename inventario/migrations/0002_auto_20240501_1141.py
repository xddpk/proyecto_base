# Generated by Django 2.0.2 on 2024-05-01 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='producto',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto'),
        ),
    ]
