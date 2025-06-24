from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import os
from twilio.rest import Client
from e_comm import settings
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class User(AbstractUser):
    telephone = PhoneNumberField(blank=True, null=True, verbose_name="Numéro de téléphone")

    photo = models.ImageField(upload_to='profile_photo/', verbose_name='Photo de profile',blank=True,null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        import random
        self.otp = str(random.randint(100000, 999999))  # Génère un OTP à 6 chiffres
        self.otp_expiry = timezone.now() + timedelta(minutes=10)  # Expire dans 10 minutes
        self.save()
#

class OTPVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expiration_time

# class Message(models.Model):
#     name=models.CharField(max_length=100)
#     score=models.IntegerField(default=0)
    
#     def __str__(self):
#         return self.name
    
#     def save(self,*args, **kwargs):
#         if self.score >= 70:
#             account_sid = os.environ["TWILIO_ACCOUNT_SID"]
#             auth_token = os.environ["TWILIO_AUTH_TOKEN"]
#             client = Client(account_sid, auth_token)

#             message = client.messages.create(
#                 body=f"Veuillez reinitialiser votre mot de passe en suivant ce lien",
#                 from_="+13603299009",
#                 to="+22667487164",
#             )

#             print(message.body)

#         return super().save(*args, **kwargs)