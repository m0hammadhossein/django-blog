from django.test import TestCase

from accounts.models import CustomUser


class TestAccount(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(username='test_user', password='12345678Aa!', biography='test_bio')

    def test_check_user(self):
        self.assertEqual(self.user.biography, 'test_bio')
        self.assertEqual(self.user.username, 'test_user')

