from django import forms

from bookstore.books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['author']
