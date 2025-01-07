from django.urls import path

from . import views

urlpatterns = [
    path("author/<int:pk>/books/", views.ApiListBooksView.as_view(), name="api books")
]
