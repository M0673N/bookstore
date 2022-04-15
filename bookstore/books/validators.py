import re

from django.core.exceptions import ValidationError

from bookstore.books.misc import list_of_genres


def validate_genre(value):
    if value not in list_of_genres:
        raise ValidationError('Enter a valid genre')


def validate_title(value):
    match = re.search(r'^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', value)
    if not match:
        raise ValidationError('Enter a valid title')
