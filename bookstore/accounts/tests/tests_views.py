from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bookstore.profiles.models import Profile

UserModel = get_user_model()

VALID_PROFILE_DATA = {'email': 'heahea@abv.bg', 'password1': 'nqkvaparola', 'password2': 'nqkvaparola'}


class ProfileCreateViewTests(TestCase):

    def test_sign_up__valid_data__expect_to_create(self):
        response = self.client.post(
            reverse('sign up'),
            data=VALID_PROFILE_DATA,
        )

        user = UserModel.objects.first()
        profile = Profile.objects.first()

        self.assertIsNotNone(user)
        self.assertEqual('heahea@abv.bg', user.email)
        self.assertFalse(user.is_active)

        self.assertIsNotNone(profile)
        self.assertFalse(profile.is_complete)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('confirm account'))

    def test_sign_up__invalid_data__expect_fail(self):
        response = self.client.post(
            reverse('sign up'),
            data={},
        )

        user = UserModel.objects.first()
        profile = Profile.objects.first()

        self.assertIsNone(user)

        self.assertIsNone(profile)

        self.assertEqual(response.status_code, 200)
