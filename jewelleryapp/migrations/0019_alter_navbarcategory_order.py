# Generated by Django 5.1.4 on 2025-05-20 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewelleryapp', '0018_rename_handcrafted_navbarcategory_is_all_jewellery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navbarcategory',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
