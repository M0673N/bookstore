from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from bookstore.profiles.forms import ProfileForm

from .signals import *
from .misc import list_of_countries

UserModel = get_user_model()


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = list_of_countries
        return context


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_profile.html'
    model = UserModel
    success_url = reverse_lazy('home')
