from django.views.generic import TemplateView, RedirectView, ListView

from bookstore.books.models import Book


class HomeView(TemplateView):
    template_name = 'index.html'


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
