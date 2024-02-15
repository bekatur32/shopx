import random
import string
from Shopx import settings
from django.core.mail import send_mail,EmailMessage
from .models import CustomUser


def generate_verification_code(length=6):
    """Generate a random verification code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def send_verification_code(email):

    verification_code = generate_verification_code()

    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    sender_email = 'tolomushev33@gmail.com'
    recipient_email = email


    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)
    user_obj = CustomUser.objects.get(email=email)
    user_obj.code = verification_code
    user_obj.save()