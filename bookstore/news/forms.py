from django import forms

from bookstore.news.models import Article, ArticleComment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["user", "date_posted"]


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        exclude = ["user", "article", "date_posted"]
