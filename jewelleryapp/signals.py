from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductStone

@receiver([post_save, post_delete], sender=ProductStone)
def update_product_totals(sender, instance, **kwargs):
    product = instance.product
    product.save()

# jewelleryapp/signals.py

from django.db.models.signals import post_migrate
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings



@receiver(post_migrate)
def create_google_social_app(sender, **kwargs):
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
    from django.conf import settings

    if not SocialApp.objects.filter(provider='google').exists():
        site = Site.objects.get(pk=1)
        app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id=settings.GOOGLE_CLIENT_ID,
            secret=settings.GOOGLE_SECRET,
        )
        app.sites.add(site)