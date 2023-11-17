from django.test import TestCase
from user.models import User
from django.contrib.auth.hashers import check_password

class CheckPasswordTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            nickname='mlb',
            password='808'
        )

    def test_check_password(self):
        is_valid_password = self.user.password == '808'
        self.assertTrue(is_valid_password)

        is_valid_password = self.user.password == 'wrongpassword'
        self.assertFalse(is_valid_password)

