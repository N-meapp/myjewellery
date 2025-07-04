# from twilio.rest import Client
# import os
# from dotenv import load_dotenv

# load_dotenv()

# account_sid = os.getenv("TWILIO_ACCOUNT_SID")
# auth_token = os.getenv("TWILIO_AUTH_TOKEN")
# twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

# client = Client(account_sid, auth_token)

# def send_otp_via_sms(phone, otp):
#     # Safety check: 'to' number should NOT be the same as Twilio 'from' number
#     if phone == twilio_number:
#         raise ValueError("Recipient phone number must be different from the Twilio sender number.")
    
#     message = client.messages.create(
#         body=f"Your OTP is {otp}",
#         from_=twilio_number,
#         to=phone
#     )
#     return message.sid
from twilio.rest import Client
import os
from dotenv import load_dotenv
from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

def send_otp_via_sms(phone, otp):
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=twilio_number,
        to=phone
    )
    return message.sid

def send_whatsapp_message(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=to,
        body=body
    )
    return message.sid


def create_google_social_app():
    if not SocialApp.objects.filter(provider='google').exists():
        site = Site.objects.get_current()
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google Login',
            client_id=settings.GOOGLE_CLIENT_ID,
            secret=settings.GOOGLE_CLIENT_SECRET
        )
        google_app.sites.add(site)