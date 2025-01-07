import threading
from django.core.mail import EmailMessage


def send_mail(mail_subject, message, to_email):
    # Handle the email sending
    def send_email():
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

    # Create and start a new thread for sending the email
    email_thread = threading.Thread(target=send_email)
    email_thread.start()
