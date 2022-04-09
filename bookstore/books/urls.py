from django.urls import path

from . import views

urlpatterns = [
    path('', views.RedirectToHomeView.as_view()),
    path('home/', views.HomeView.as_view(), name='home'),
    path('books/', views.ListBooksView.as_view(), name='all books'),
    path('add-book/', views.AddBookView.as_view(), name='add book'),
    path('book-details/<int:pk>', views.BookDetailsView.as_view(), name='book details'),
    path('edit-book/<int:pk>', views.EditBookView.as_view(), name='edit book'),
    path('delete-book/<int:pk>', views.DeleteBookView.as_view(), name='delete book'),
    path('like/<int:pk>', views.LikeBookView.as_view(), name='like book'),
    path('dislike/<int:pk>', views.DislikeBookView.as_view(), name='dislike book'),
    path('review-book/<int:pk>', views.ReviewBookView.as_view(), name='review book'),
    path('delete-book-review/<int:pk>', views.DeleteBookReviewView.as_view(), name='delete book review'),
    path('search/', views.SearchView.as_view(), name='search books'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('message-sent/', views.MessageSentView.as_view(), name='message sent'),
    path('confirm-order/', views.ConfirmOrderView.as_view(), name='confirm order'),
    path('finalize-order/', views.FinalizeOrderView.as_view(), name='finalize order'),
    path('order-sent/', views.OrderSentView.as_view(), name='order sent'),
    path('finalize-guest-order/', views.FinalizeGuestOrderView.as_view(), name='finalize guest order'),

]
