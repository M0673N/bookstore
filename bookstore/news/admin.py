from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from bookstore.news.models import Article, ArticleComment


class InlineArticleCommentAdmin(TabularInline):
    model = ArticleComment
    list_display = ('id', 'text', 'date_posted', 'user')


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('id', 'title', 'text', 'image_tag', 'user', 'date_posted')
    inlines = (InlineArticleCommentAdmin,)
    list_filter = ('user', 'title', 'id', 'date_posted')
    ordering = ('date_posted',)
    readonly_fields = ('image_tag',)


@admin.register(ArticleComment)
class ArticleCommentAdmin(ModelAdmin):
    list_display = ('id', 'text', 'date_posted', 'article', 'user')
    list_filter = ('user', 'date_posted')
    ordering = ('date_posted',)
