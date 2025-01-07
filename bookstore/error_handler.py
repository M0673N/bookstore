from decouple import config
from django.conf import settings
import traceback

from django.shortcuts import render

from bookstore.tasks import send_mail


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if exception:
                message = f"**{request.build_absolute_uri()}**\n\n{repr(exception)}\n\n````{traceback.format_exc()}````"
                mail_subject = "Site Error"
                text = message
                to_email = config("SITE_OWNER_EMAIL")
                send_mail(mail_subject, text, to_email)

            return render(request, "error.html")
