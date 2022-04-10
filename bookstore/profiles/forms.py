from django import forms

from bookstore.profiles.misc import list_of_countries
from bookstore.profiles.models import Profile, AuthorReview
from bookstore.profiles.validators import validate_city, validate_phone_number


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('is_complete', 'user')


class AuthorReviewForm(forms.ModelForm):
    class Meta:
        model = AuthorReview
        fields = ['text']


class GuestOrderForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    country = forms.ChoiceField(choices=[(country, country) for country in list_of_countries])
    city = forms.CharField(max_length=200, validators=[validate_city])
    street_address = forms.CharField(max_length=200)
    post_code = forms.CharField(max_length=20)
    phone = forms.CharField(validators=[validate_phone_number], max_length=30)
    email = forms.EmailField()


class AuthorMessageForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
