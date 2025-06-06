# Generated by Django 5.1.4 on 2025-06-04 09:25

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gemstone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_images', models.JSONField(blank=True, default=list, null=True)),
                ('main_mobile_img', models.JSONField(blank=True, default=list, null=True)),
                ('main_img', models.JSONField(blank=True, default=list, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('confirmpassword', models.CharField(max_length=128)),
                ('mobile', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SearchGif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('categories', 'Categories'), ('occasions', 'Occasions'), ('price', 'Price'), ('gender', 'Gender')], max_length=20)),
                ('label', models.CharField(max_length=100)),
                ('icon', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Metal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('karat', models.FloatField(blank=True, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='NavbarCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_handcrafted', models.BooleanField(default=False)),
                ('handcrafted_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('is_all_jewellery', models.BooleanField(default=False)),
                ('all_jewellery_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('is_gemstone', models.BooleanField(default=False)),
                ('gemstone_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('order', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.category')),
                ('gemstone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.gemstone')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.material')),
                ('occasion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.occasion')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=255)),
                ('metal_weight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('karat', models.FloatField(blank=True, null=True)),
                ('images', models.JSONField(blank=True, null=True)),
                ('ar_model_glb', models.URLField(blank=True, null=True)),
                ('ar_model_gltf', models.URLField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=1550, null=True)),
                ('pendant_width', models.CharField(blank=True, max_length=20, null=True)),
                ('pendant_height', models.CharField(blank=True, max_length=20, null=True)),
                ('frozen_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('making_charge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('making_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('product_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('gst', models.DecimalField(decimal_places=2, default=3, max_digits=10)),
                ('handcrafted_charge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_handcrafted', models.BooleanField(default=False)),
                ('is_classic', models.BooleanField(default=False)),
                ('designing_charge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.category')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.gender')),
                ('metal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.metal')),
                ('occasion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.occasion')),
                ('stones', models.ManyToManyField(blank=True, related_name='products', to='jewelleryapp.gemstone')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='jewelleryapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductStone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1)),
                ('weight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.product')),
                ('stone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.gemstone')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.BigIntegerField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='jewelleryapp.register')),
            ],
        ),
        migrations.CreateModel(
            name='UserVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.register')),
            ],
            options={
                'verbose_name': 'User Visit',
                'verbose_name_plural': 'User Visits',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='jewelleryapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to='jewelleryapp.register')),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]
