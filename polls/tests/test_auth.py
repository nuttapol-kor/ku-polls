"""Unittest for testing the authentication"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from polls.models import Question


def create_user(username, email, password):
    User.objects.create_user(username=username, email=email, password=password)


class LoginTest(TestCase):
    """Class for test login system"""

    def test_simple_login(self):
        """If can login, that user must be authenticated in website"""
        create_user("Test_User1", "Test_User1@gmail.com", "isp123456")
        response = self.client.post(reverse('login'), {'username': 'Test_User1', 'password': 'isp123456'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_can_not_login_with_user_that_not_enter_password(self):
        """Can not login with enter the username but not enter the password"""
        create_user("User1", "User1@gmail.com", "isp123456")
        response = response = self.client.post(reverse('login'), {'username':'User1'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_can_not_login_with_user_that_enter_wrong_password(self):
        """Can not login, if enter the wrong password"""
        create_user("User1", "User1@gmail.com", "isp123456")
        response = self.client.post(reverse('login'), {'username':'User1', 'password':'isp555555'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

class LogOutTest(TestCase):
    """Class for test logout system"""

    def test_simple_logout(self):
        """If logout is work it should redirect to somewhere"""
        create_user("User1", "User1@gmail.com", "isp123456")
        self.client.login(username='User1', password='isp123456')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
