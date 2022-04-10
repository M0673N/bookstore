from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('edit/<int:pk>', views.EditProfileView.as_view(), name='edit profile'),
    path('delete/<int:pk>', views.DeleteProfileView.as_view(), name='delete profile'),
    path('like/<int:pk>', views.LikeAuthorView.as_view(), name='like author'),
    path('dislike/<int:pk>', views.DislikeAuthorView.as_view(), name='dislike author'),
    path('review-author/<int:pk>', views.ReviewAuthorView.as_view(), name='review author'),
    path('delete-author-review/<int:pk>', views.DeleteAuthorReviewView.as_view(), name='delete author review'),
    path('message/<int:pk>', views.SendAuthorAMessageView.as_view(), name='send author a message'),
]
