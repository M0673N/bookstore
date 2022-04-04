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
]
