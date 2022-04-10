from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, FormView

from bookstore.profiles.forms import ProfileForm, AuthorReviewForm, AuthorMessageForm
from .models import AuthorLike, AuthorDislike, AuthorReview

from .signals import *
from .misc import list_of_countries
from bookstore.tasks import send_mail

UserModel = get_user_model()


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = context['profile']

        if self.request.user.is_authenticated:
            is_owner = author == self.request.user.profile
        else:
            is_owner = False

        is_liked_by_user = author.authorlike_set.filter(user_id=self.request.user.id).exists()
        is_disliked_by_user = author.authordislike_set.filter(user_id=self.request.user.id).exists()
        has_reviewed = author.authorreview_set.filter(user_id=self.request.user.id).exists()
        context['form'] = AuthorReviewForm()
        context['reviews'] = author.authorreview_set.all().order_by('-date_posted')
        context['is_liked'] = is_liked_by_user
        context['is_disliked'] = is_disliked_by_user
        context['likes'] = author.authorlike_set.count()
        context['dislikes'] = author.authordislike_set.count()
        context['is_owner'] = is_owner
        context['has_reviewed'] = has_reviewed

        return context


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


class LikeAuthorView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        author = Profile.objects.get(pk=self.kwargs['pk'])
        liked_by_user = author.authorlike_set.filter(user_id=self.request.user.id).first()
        disliked_by_user = author.authordislike_set.filter(user_id=self.request.user.id).first()
        if liked_by_user:
            liked_by_user.delete()
        elif disliked_by_user:
            disliked_by_user.delete()
            like = AuthorLike(author=author, user=self.request.user)
            like.save()
        else:
            like = AuthorLike(author=author, user=self.request.user)
            like.save()
        return redirect('profile', author.pk)


class DislikeAuthorView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        author = Profile.objects.get(pk=self.kwargs['pk'])
        liked_by_user = author.authorlike_set.filter(user_id=self.request.user.id).first()
        disliked_by_user = author.authordislike_set.filter(user_id=self.request.user.id).first()
        if liked_by_user:
            liked_by_user.delete()
            dislike = AuthorDislike(author=author, user=self.request.user)
            dislike.save()
        elif disliked_by_user:
            disliked_by_user.delete()
        else:
            dislike = AuthorDislike(author=author, user=self.request.user)
            dislike.save()
        return redirect('profile', author.pk)


class ReviewAuthorView(LoginRequiredMixin, View):
    form_class = AuthorReviewForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            author = Profile.objects.get(pk=self.kwargs['pk'])
            review = AuthorReview(
                text=form.cleaned_data['text'],
                author=author,
                user=self.request.user,
            )
            review.save()

            return redirect('profile', author.pk)


class DeleteAuthorReviewView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        author = Profile.objects.get(pk=self.kwargs['pk'])
        review = author.authorreview_set.filter(user_id=self.request.user.id)
        review.delete()
        return redirect('profile', author.pk)


class SendAuthorAMessageView(FormView):
    template_name = 'send_author_a_message.html'
    form_class = AuthorMessageForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            mail_subject = 'Message from user'
            message = render_to_string('contact_author_email.html', {
                'message': form.cleaned_data['message'],
                'subject': form.cleaned_data['subject'],
                'name': f'{self.request.user.profile.first_name} {self.request.user.profile.first_name}',
                'email': self.request.user.email
            })
            to_email = UserModel.objects.get(pk=self.kwargs['pk']).email
            send_mail.delay(mail_subject, message, to_email)
            return render(self.request, 'message_sent.html')
        else:
            return render(self.request, 'send_author_a_message.html', {'form': form})
