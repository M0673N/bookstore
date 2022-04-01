from django import forms

from bookstore.profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('is_complete', 'user')
