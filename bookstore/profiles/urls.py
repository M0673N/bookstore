from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('edit/<int:pk>', views.EditProfileView.as_view(), name='edit profile'),
    path('delete/<int:pk>', views.DeleteProfileView.as_view(), name='delete profile'),
]
