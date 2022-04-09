from django import forms

from bookstore.books.models import Book, BookReview


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['author']


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['text']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


class OrderForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    book_pk = forms.IntegerField(min_value=1)
