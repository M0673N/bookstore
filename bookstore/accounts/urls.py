from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sign up'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('confirm/', views.ConfirmAccount.as_view(), name='confirm account'),
    path('signin/', views.SignInView.as_view(), name='sign in'),
    path('signout/', views.SignOutView.as_view(), name='sign out'),
]
