from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='sign up'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
