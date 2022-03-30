from django.urls import path

from . import views

urlpatterns = [
    path('', views.RedirectToHomeView.as_view()),
    path('home/', views.HomeView.as_view(), name='home'),
]
