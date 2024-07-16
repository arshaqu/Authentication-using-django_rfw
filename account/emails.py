from django.conf import settings
import random
from django.core.mail import send_mail
from .models import *


def send_otp_via_email(email,otp):
    subject='Account Verification Email'
    otp=random.randint(1000,9999)
    message=f'Your OTP is {otp}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)

    user_obj = UserData.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()