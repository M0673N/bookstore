from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from bookstore.news.models import Article, ArticleComment
from bookstore.profiles.models import AuthorReview, Profile

UserModel = get_user_model()


class InlineProfileAdmin(StackedInline):
    model = Profile
    fields = ("first_name", "last_name", "biography", "image_tag")
    readonly_fields = ("image_tag",)


class InlineArticleAdmin(StackedInline):
    model = Article
    fields = ("title", "text")
    readonly_fields = ("date_posted", "image_tag")


class InlineArticleCommentAdmin(StackedInline):
    model = ArticleComment
    fields = ("text", "article")
    readonly_fields = ("date_posted",)


class InlineAuthorReviewAdmin(StackedInline):
    model = AuthorReview
    fields = ("text", "author")
    readonly_fields = ("date_posted",)


@admin.register(UserModel)
class BookstoreUserAdmin(UserAdmin):
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "groups")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("date_joined",)
    inlines = (
        InlineProfileAdmin,
        InlineArticleAdmin,
        InlineArticleCommentAdmin,
        InlineAuthorReviewAdmin,
    )


@admin.register(AuthorReview)
class AuthorReviewAdmin(ModelAdmin):
    list_display = ("text", "user", "author")
    list_filter = ("user", "date_posted", "author")
    ordering = ("date_posted",)
