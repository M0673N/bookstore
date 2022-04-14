from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from bookstore.books.models import Book, BookReview


class InlineBookReviewAdmin(TabularInline):
    model = BookReview
    list_display = ('id', 'text', 'date_posted', 'user')


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('id', 'title', 'description', 'image_tag', 'author')
    inlines = (InlineBookReviewAdmin,)
    list_filter = ('author', 'title', 'id')
    ordering = ('title',)
    readonly_fields = ('image_tag',)


@admin.register(BookReview)
class BookReviewAdmin(ModelAdmin):
    list_display = ('id', 'text', 'date_posted', 'user', 'book')
    list_filter = ('user', 'date_posted')
    ordering = ('date_posted',)
