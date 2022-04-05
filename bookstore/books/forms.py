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
