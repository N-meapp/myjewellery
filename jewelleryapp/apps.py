# from django.apps import AppConfig
# from django.contrib.sites.models import Site
# from django.conf import settings

# class JewelleryappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'jewelleryapp'

#     def ready(self):
#         import jewelleryapp.signals




# class JewelleryappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'jewelleryapp'

#     def ready(self):
#         from django.conf import settings
#         if settings.DEBUG:
#             from .utils import create_google_social_app  # ✅ move your logic into utils.py or similar
#             create_google_social_app()
# jewelleryapp/apps.py
from django.apps import AppConfig

class JewelleryappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jewelleryapp'

    def ready(self):
        import jewelleryapp.signals  # ✅ move logic into a signal

