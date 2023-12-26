from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'
    from_email = 'ecommerce@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)