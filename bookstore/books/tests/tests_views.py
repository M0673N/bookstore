from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bookstore.books.models import Book

UserModel = get_user_model()


class HomeViewTests(TestCase):

    def test_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_context_data(self):
        user = UserModel.objects.create(email='aaa', password='aaa')
        book = Book.objects.create(title='aaa', genre='aaa', price=99, author=user)

        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context_data['books']), 1)


class RedirectToHomeViewTests(TestCase):

    def test_redirect_to_home(self):
        response = self.client.get('')
        self.assertRedirects(response, reverse('home'))


class ListBooksViewTests(TestCase):

    def test_correct_template(self):
        response = self.client.get(reverse('all books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_books.html')

    def test_context_data(self):
        user = UserModel.objects.create(email='aaa', password='aaa')
        book = Book.objects.create(title='aaa', genre='aaa', price=99, author=user)

        response = self.client.get(reverse('all books'))
        self.assertEqual(len(response.context_data['books']), 1)
        self.assertIsNotNone(response.context_data['page_obj'])
        self.assertEqual(['aaa'], list(response.context_data['genres']))
