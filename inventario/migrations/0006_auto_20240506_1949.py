# Generated by Django 2.0.2 on 2024-05-06 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_remove_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='inventario.Category_group'),
        ),
    ]