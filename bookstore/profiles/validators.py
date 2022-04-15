import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    match = re.search(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', value)
    if not match:
        raise ValidationError('Enter a valid phone number')


def validate_city(value):
    match = re.search(r'^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', value)
    if not match:
        raise ValidationError('Enter a valid city')


def validate_name(value):
    match = re.search(r'^[A-Z][A-Za-z]{1,24}$', value)
    if not match:
        raise ValidationError('Enter a valid name')
