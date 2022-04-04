from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, ListView, CreateView, DetailView, UpdateView, DeleteView

from bookstore.books.forms import BookForm
from bookstore.books.misc import list_of_genres

from .signals import *
from django.db.models import signals


class HomeView(ListView):
    context_object_name = 'books'
    model = Book
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.order_by('?')[:8]
        return context


class RedirectToHomeView(RedirectView):
    pattern_name = 'home'


class ListBooksView(ListView):
    template_name = 'all_books.html'
    context_object_name = 'books'
    model = Book
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Book.objects.all().values_list('genre', flat=True).distinct()
        return context


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('all books')
    template_name = 'add_book.html'

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            signals.pre_save.disconnect(receiver=delete_old_book_image_on_change, sender=Book)
            book = form.save(commit=False)
            book.author = self.request.user
            book.save()
            signals.pre_save.connect(receiver=delete_old_book_image_on_change, sender=Book)
            return redirect('all books')
        else:
            return render(request, 'add_book.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = list_of_genres
        return context


class BookDetailsView(DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context['book']

        is_owner = book.author == self.request.user

        # comments, likes and dislikes planned for the future
        # is_liked_by_user = book.like_set.filter(user_id=self.request.user.id).exists()
        # is_disliked_by_user = book.dislike_set.filter(user_id=self.request.user.id).exists()
        # context['form'] = CommentForm()
        # context['comments'] = book.comment_set.all()
        # context['is_liked'] = is_liked_by_user
        # context['is_liked'] = is_disliked_by_user
        # context['likes'] = pet.like_set.count()
        # context['dislikes'] = pet.dislike_set.count()
        context['is_owner'] = is_owner

        return context


class EditBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('all books')
    template_name = 'edit_book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = list_of_genres
        return context


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_book.html'
    model = Book
    success_url = reverse_lazy('all books')
