from rest_framework import serializers

from bookstore.books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["author", "description"]
