from decouple import config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    RedirectView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView,
)

from bookstore.books.forms import BookForm, BookReviewForm, ContactForm, OrderForm
from bookstore.books.misc import list_of_genres
from .models import Like, Dislike, BookReview

from .signals import *
from django.db.models import signals
from bookstore.tasks import send_mail
from ..profiles.forms import GuestOrderForm
from ..profiles.misc import list_of_countries


class HomeView(ListView):
    context_object_name = "books"
    model = Book
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.order_by("?")[:6]
        return context


class RedirectToHomeView(RedirectView):
    pattern_name = "home"


class ListBooksView(ListView):
    template_name = "books/all_books.html"
    context_object_name = "books"
    model = Book
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = (
            Book.objects.all().values_list("genre", flat=True).distinct()
        )
        return context


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("all books")
    template_name = "books/add_book.html"

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            signals.pre_save.disconnect(
                receiver=delete_old_book_image_on_change, sender=Book
            )
            book = form.save(commit=False)
            book.author = self.request.user
            book.save()
            signals.pre_save.connect(
                receiver=delete_old_book_image_on_change, sender=Book
            )
            return redirect("all books")
        else:
            return render(request, "books/add_book.html", {"form": form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = list_of_genres
        return context


class BookDetailsView(DetailView):
    model = Book
    template_name = "books/book_details.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context["book"]

        is_owner = book.author == self.request.user

        is_liked_by_user = book.like_set.filter(user_id=self.request.user.id).exists()
        is_disliked_by_user = book.dislike_set.filter(
            user_id=self.request.user.id
        ).exists()
        has_reviewed = book.bookreview_set.filter(user_id=self.request.user.id).exists()
        context["form"] = BookReviewForm()
        context["reviews"] = book.bookreview_set.all().order_by("-date_posted")
        context["is_liked"] = is_liked_by_user
        context["is_disliked"] = is_disliked_by_user
        context["likes"] = book.like_set.count()
        context["dislikes"] = book.dislike_set.count()
        context["is_owner"] = is_owner
        context["has_reviewed"] = has_reviewed

        return context


class EditBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("all books")
    template_name = "books/edit_book.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = list_of_genres
        return context


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = "books/delete_book.html"
    model = Book
    success_url = reverse_lazy("all books")


class LikeBookView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=self.kwargs["pk"])
        liked_by_user = book.like_set.filter(user_id=self.request.user.id).first()
        disliked_by_user = book.dislike_set.filter(user_id=self.request.user.id).first()
        if liked_by_user:
            liked_by_user.delete()
        elif disliked_by_user:
            disliked_by_user.delete()
            like = Like(book=book, user=self.request.user)
            like.save()
        else:
            like = Like(book=book, user=self.request.user)
            like.save()
        return redirect("book details", book.id)


class DislikeBookView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=self.kwargs["pk"])
        liked_by_user = book.like_set.filter(user_id=self.request.user.id).first()
        disliked_by_user = book.dislike_set.filter(user_id=self.request.user.id).first()
        if liked_by_user:
            liked_by_user.delete()
            dislike = Dislike(book=book, user=self.request.user)
            dislike.save()
        elif disliked_by_user:
            disliked_by_user.delete()
        else:
            dislike = Dislike(book=book, user=self.request.user)
            dislike.save()
        return redirect("book details", book.id)


class ReviewBookView(LoginRequiredMixin, View):
    form_class = BookReviewForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            book = Book.objects.get(pk=self.kwargs["pk"])
            review = BookReview(
                text=form.cleaned_data["text"],
                book=book,
                user=self.request.user,
            )
            review.save()

            return redirect("book details", book.id)

        return redirect("book details", self.kwargs["pk"])


class DeleteBookReviewView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=self.kwargs["pk"])
        review = book.bookreview_set.filter(user_id=self.request.user.id)
        review.delete()
        return redirect("book details", book.pk)


class SearchView(View):

    def get(self, request, *args, **kwargs):
        context = {}

        books = cache.get("books")
        if not books:
            return redirect("all books")

        genres = cache.get("genres")

        paginator = Paginator(books, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["genres"] = genres

        return render(request, "books/search_books.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        books = None
        if self.request.POST.get("title"):
            books = Book.objects.filter(title__icontains=self.request.POST.get("title"))
        elif self.request.POST.get("my-books"):
            books = Book.objects.filter(author_id=self.request.user.id)
        elif self.request.POST.get("genre"):
            books = Book.objects.filter(genre=self.request.POST.get("genre"))

        genres = books.values_list("genre", flat=True).distinct()
        context["genres"] = genres

        paginator = Paginator(books, 12)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj

        cache.set("books", books)
        cache.set("genres", genres)

        return render(request, "books/search_books.html", context)


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm

    def form_valid(self, form):
        mail_subject = form.cleaned_data.get("subject")
        message = render_to_string(
            "profile/contact_email.html",
            {
                "name": form.cleaned_data.get("name"),
                "message": form.cleaned_data.get("message"),
                "email": form.cleaned_data.get("email"),
            },
        )
        to_email = config("SITE_OWNER_EMAIL")
        send_mail(mail_subject, message, to_email)
        return redirect("message sent")


class MessageSentView(TemplateView):
    template_name = "message_sent.html"


class ConfirmOrderView(View):

    def post(self, request, *args, **kwargs):
        form = OrderForm(self.request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            book_pk = form.cleaned_data["book_pk"]
            book = Book.objects.get(pk=book_pk)
            total_price = book.price * amount
            context = {"book": book, "total_price": total_price, "amount": amount}
            return render(self.request, "orders/confirm_order.html", context)
        else:
            return redirect("book details", self.request.POST["book_pk"])


class FinalizeOrderView(View):

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.profile.is_complete:
            book = Book.objects.get(pk=self.request.POST["book_pk"])
            amount = int(self.request.POST["amount"])
            mail_subject = "New Order"
            message = render_to_string(
                "orders/order_email.html",
                {
                    "name": f"{self.request.user.profile.first_name} {self.request.user.profile.last_name}",
                    "address": f"Country: {self.request.user.profile.country}\n"
                    f"City: {self.request.user.profile.city}\n"
                    f"Post Code: {self.request.user.profile.post_code}\n"
                    f"Street Address: {self.request.user.profile.street_address}",
                    "email": self.request.user.email,
                    "phone": self.request.user.profile.phone,
                    "book": book,
                    "signed": True,
                    "amount": amount,
                    "total": amount * book.price,
                },
            )
            to_email = book.author.email
            send_mail(mail_subject, message, to_email)
            return redirect("order sent")
        else:
            context = {
                "book_pk": self.request.POST["book_pk"],
                "amount": self.request.POST["amount"],
                "countries": list_of_countries,
            }
            return render(self.request, "orders/guest_order.html", context)


class OrderSentView(TemplateView):
    template_name = "orders/order_complete.html"


class FinalizeGuestOrderView(View):

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(pk=self.request.POST["book_pk"])
        amount = int(self.request.POST["amount"])
        form = GuestOrderForm(self.request.POST)
        if form.is_valid():
            mail_subject = "New Order"
            message = render_to_string(
                "orders/order_email.html",
                {
                    "name": f'{form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}',
                    "address": f'Country: {form.cleaned_data["country"]}\n'
                    f'City: {form.cleaned_data["city"]}\n'
                    f'Post Code: {form.cleaned_data["post_code"]}\n'
                    f'Street Address: {form.cleaned_data["street_address"]}',
                    "email": form.cleaned_data["email"],
                    "phone": form.cleaned_data["phone"],
                    "signed": False,
                    "book": book,
                    "amount": amount,
                    "total": amount * book.price,
                },
            )
            to_email = book.author.email
            send_mail(mail_subject, message, to_email)
            return redirect("order sent")
        else:
            context = {
                "book_pk": book.pk,
                "amount": amount,
                "countries": list_of_countries,
                "form": form,
            }
            return render(self.request, "orders/guest_order.html", context)
