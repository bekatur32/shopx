import random
import string
from Shopx import settings
import requests
from django.core.mail import send_mail,EmailMessage
from .models import CustomUser


def generate_verification_code(length=6):
    """Generate a random verification code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def send_verification_code(email_or_phone):

    verification_code = generate_verification_code()

    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    sender_email = 'tolomushev33@gmail.com'
    recipient_email = email_or_phone


    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)
    user_obj = CustomUser.objects.get(email_or_phone=email_or_phone)
    user_obj.code = verification_code
    user_obj.save()




def send_code_to_number(email_or_phone):
    login = 'erko'
    password = 'Bishkek2022'
    sender = 'SMSPRO.KG'

    transactionId = generate_verification_code()
    code = generate_verification_code()

    xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <message>
        <login>{login}</login>
        <pwd>{password}</pwd>
        <id>{transactionId}</id>
        <sender>{sender}</sender>
        <text>{code}</text>
        <phones>
            <phone>{email_or_phone}</phone>
        </phones>
    </message>"""


    url = 'https://smspro.nikita.kg/api/message'
    headers = {'Content-Type': 'application/xml'}

    response = requests.post(url, data=xml_data, headers=headers)
    user_obj = CustomUser.objects.get(email_or_phone=email_or_phone)
    user_obj.code = code
    print(user_obj.number)
    user_obj.save()
    if response.status_code == 200:
        print('Ответ сервера:', response.text)