from django import forms

from bookstore.profiles.models import Profile, AuthorReview


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('is_complete', 'user')


class AuthorReviewForm(forms.ModelForm):
    class Meta:
        model = AuthorReview
        fields = ['text']
