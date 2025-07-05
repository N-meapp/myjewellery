from django.db import models
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from cloudinary import uploader
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils import timezone 
from django.contrib.auth import get_user_model
# User = get_user_model()
from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random

from django.db.models import Avg
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Base material like Gold
# , Silver, Diamond, etc.
class Material(models.Model):
    name = models.CharField(max_length=50)
    image = CloudinaryField('image', folder="Material/")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = CloudinaryField('image', folder="category/")

    def __str__(self):
        return self.name

class Occasion(models.Model):
    name = models.CharField(max_length=50)
    image = CloudinaryField('image', folder='Occasions')

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=20)  # e.g., Men, Women, Unisex
    image = CloudinaryField('image', folder='gender')

    def __str__(self):
        return self.name

class Metal(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='metal')
    karat = models.FloatField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.karat}K)"

class Gemstone(models.Model):
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', folder='stones')
    color = models.CharField(max_length=50, null=True, blank=True)
    clarity = models.CharField(max_length=50, null=True, blank=True)
    shape = models.CharField(max_length=50, null=True, blank=True)
    def calculate_price(self, weight):
        return weight * self.unit_price

    def __str__(self):
        return self.name

# --- Product Model ---
class Product(models.Model):
    head = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    metal_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    karat = models.FloatField(null=True, blank=True)
    images = models.JSONField(blank=True, null=True)
    ar_model_glb = models.URLField(blank=True, null=True)
    ar_model_gltf = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=1550, blank=True, null=True)
    pendant_width = models.CharField(max_length=20,blank=True, null=True)
    pendant_height = models.CharField(max_length=20,blank=True, null=True)
    frozen_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    making_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    making_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=3)
    handcrafted_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_handcrafted = models.BooleanField(default=False)

    is_classic = models.BooleanField(default=False)  # ✅ New field
    designing_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ✅ New field
    total_stock = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    
    stones = models.ManyToManyField(Gemstone, related_name="products", blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    @property
    def stone_price_total(self):
        total = sum(
            (ps.get_stone_price() or Decimal('0.00') for ps in self.productstone_set.all()),
            Decimal('0.00')
        )
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def subtotal(self):
        if self.frozen_unit_price and self.frozen_unit_price > 0:
            base_price = self.metal_weight * self.frozen_unit_price
        else:
            base_price = self.metal_weight * self.metal.unit_price

        subtotal = (
            base_price
            + self.making_charge
            + self.stone_price_total
            - self.making_discount
            - self.product_discount
        )

        if self.is_classic:
            subtotal += self.designing_charge

        return subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def grand_total(self):
        subtotal = self.subtotal
        total_with_gst = subtotal * (1 + (self.gst / 100))

        if self.is_handcrafted:
            total_with_gst += self.handcrafted_charge

        return total_with_gst.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def average_rating(self):
        avg = self.ratings.aggregate(avg_rating=Avg('rating')).get('avg_rating')
        if avg is None:
            return 0.0
        return round(avg, 2)
    
    @property
    def available_stock(self):
        return max(self.total_stock - self.sold_count, 0)

    def sell(self, quantity):
        if quantity > self.available_stock:
            raise ValueError("Not enough stock available to sell.")
        self.sold_count += quantity
        self.save()
        return self.available_stock == 0

    def __str__(self):
        return self.head
    

class ProductStone(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stone = models.ForeignKey(Gemstone, on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=1)
    weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    def get_stone_price(self):
        if self.stone and self.weight and self.stone.unit_price:
            return (self.weight * self.stone.unit_price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return None
    
    def __str__(self):
        return self.product.head  

class ProductRating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5 stars, you can add validation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating} for {self.product.head}"




class NavbarCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True, blank=True)
    occasion = models.ForeignKey('Occasion', on_delete=models.SET_NULL, null=True, blank=True)
    gemstone = models.ForeignKey('Gemstone', on_delete=models.SET_NULL, null=True, blank=True)

    is_handcrafted = models.BooleanField(default=False)
    handcrafted_image = CloudinaryField('image', folder='handcrafted/', null=True, blank=True)

    is_all_jewellery = models.BooleanField(default=False)
    all_jewellery_image = CloudinaryField('image', folder='all_jewellery/', null=True, blank=True)

    is_gemstone = models.BooleanField(default=False)
    gemstone_image = CloudinaryField('image', folder='gemstone/', null=True, blank=True)

    # ✅ New custom image field for occasion
    occasion_image = CloudinaryField('image', folder='occasion_navbar/', null=True, blank=True)

    order = models.PositiveIntegerField(default=0)

    def clean(self):
        fields = [
            self.category, self.material, self.occasion, self.gemstone,
            self.is_handcrafted, self.is_all_jewellery, self.is_gemstone
        ]
        count = sum(bool(f) for f in fields)
        if count == 0:
            raise ValidationError("At least one type must be selected.")
        if count > 1:
            raise ValidationError("Only one type can be selected at a time.")

    def __str__(self):
        return self.get_name() or "Unnamed NavbarItem"

    def get_name(self):
        if self.category:
            return self.category.name
        if self.material:
            return self.material.name
        if self.occasion:
            return self.occasion.name
        if self.gemstone:
            return self.gemstone.name
        if self.is_handcrafted:
            return "Handcrafted"
        if self.is_all_jewellery:
            return "All Jewellery"
        if self.is_gemstone:
            return "Gemstone"
        return None

    def get_image(self):
        if self.category and getattr(self.category, 'image', None):
            return self.category.image.url
        if self.material and getattr(self.material, 'image', None):
            return self.material.image.url
        if self.occasion and self.occasion_image:
            return self.occasion_image.url  # ✅ Use custom occasion image
        if self.gemstone and self.gemstone_image:
            return self.gemstone_image.url
        if self.is_handcrafted and self.handcrafted_image:
            return self.handcrafted_image.url
        if self.is_all_jewellery and self.all_jewellery_image:
            return self.all_jewellery_image.url
        if self.is_gemstone and self.gemstone_image:
            return self.gemstone_image.url
        return None




class Header(models.Model):
    slider_images = models.JSONField(default=list, null=True, blank=True)
    main_mobile_img = models.JSONField(default=list, null=True, blank=True)
    main_img = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return f"Header with {len(self.slider_images)} images" if self.slider_images else "Empty Header"

class Contact(models.Model):
    number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.number
import uuid

class RegisterManager(BaseUserManager):
    def create_user(self, username, mobile, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        if not mobile:
            raise ValueError('The Mobile number must be set')

        user = self.model(username=username, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, mobile, password, **extra_fields)


class Register(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RegisterManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class PhoneOTP(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class ProductEnquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='enquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.product.head}"

    def get_message_or_default(self):
        if self.message and self.message.strip():
            return self.message.strip()
        return "I wanted to know more about this"


class AdminLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Automatically hash password on create
        if not self.pk:  # Only hash when creating, not updating
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
# class Register(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128)
#     confirmpassword = models.CharField(max_length=128)
#     mobile = models.BigIntegerField()

#     def __str__(self):
#         return self.username

#     def save(self, *args, **kwargs):
#         # Ensure passwords match before saving
#         if self.password != self.confirmpassword:
#             raise ValidationError("Passwords do not match")
        
#         # Hash the password before saving
#         self.password = make_password(self.password)
#         super().save(*args, **kwargs)
    

# class PhoneOTP(models.Model):
#     phone = models.CharField(max_length=15, unique=True)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.phone} - {self.otp} - Verified: {self.is_verified}"

#     def generate_otp(self):
#         import random
#         self.otp = str(random.randint(100000, 999999))


class UserProfile(models.Model):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Ms', 'Ms'),
        ('Mrs', 'Mrs'),
        # You can add more as needed
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.OneToOneField('Register', on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.BigIntegerField()
    email = models.EmailField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    agree = models.BooleanField(default=False, help_text="User must agree to privacy policy")
    def __str__(self):
        return f"{self.title} {self.full_name}" if self.title else self.full_name
         
# wishlist functioning


class Wishlist(models.Model):
    user = models.ForeignKey(
        'Register',
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        to_field='id',  # Optional, but good practice
        db_column='user_id'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"


class UserVisit(models.Model):
    user = models.ForeignKey('Register', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Visit"
        verbose_name_plural = "User Visits"
        ordering = ['-timestamp']

    def __str__(self):
        if self.user:
            return f"{self.user.username} visited {self.product.head} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        return f"Anonymous visited {self.product.head} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class SubCategory(models.Model):
    CATEGORY_TYPES = [
        ('categories', 'Categories'),
        ('occasions', 'Occasions'),
        ('price', 'Price'),
        ('gender', 'Gender'),
    ]
    type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    label = models.CharField(max_length=100)
    icon = models.URLField()

    def __str__(self):
        return f"{self.type} - {self.label}"

# class SearchGif(models.Model):
#     image = models.ImageField(upload_to='gifs/', blank=True, null=True)

#     def __str__(self):
#         return self.image.name if self.image else 'No Image'


class SearchGif(models.Model):
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.image.public_id if self.image else 'No Image'



