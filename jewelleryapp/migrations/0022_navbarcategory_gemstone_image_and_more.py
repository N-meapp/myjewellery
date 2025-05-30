# Generated by Django 5.1.4 on 2025-05-20 09:20

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewelleryapp', '0021_navbarcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='navbarcategory',
            name='gemstone_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='navbarcategory',
            name='is_gemstone',
            field=models.BooleanField(default=False),
        ),
    ]
