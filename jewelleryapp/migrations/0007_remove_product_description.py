# Generated by Django 5.1.4 on 2025-05-17 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jewelleryapp', '0006_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]
