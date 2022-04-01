import os

from celery import shared_task

from django.core.mail import EmailMessage


@shared_task
def send_verification_mail(mail_subject, message, to_email):
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
