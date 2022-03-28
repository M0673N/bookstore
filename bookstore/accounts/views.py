from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.views import View
from django.views.generic import CreateView, TemplateView

from .forms import SignupForm

from .tasks import send_verification_mail
from .tokens import account_activation_token

UserModel = get_user_model()


class ConfirmAccount(TemplateView):
    template_name = 'successfully_registered.html'


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('confirm account')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        send_verification_mail.delay(mail_subject, message, to_email)
        return super().form_valid(form)


class ActivateView(View):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = UserModel.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Activation link is invalid!')


class SignInView(LoginView):
    template_name = 'signup.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('home')


class SignOutView(LogoutView):
    next_page = reverse_lazy('home')
