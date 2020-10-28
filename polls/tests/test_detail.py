"""Unittest for testing the polls detail"""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question

def create_question(question_text, days, end_date=7):
    """
    Create a question.

    Keyword arguments:
    question_text -- a question text
    days -- published the given number of days offset to now
    end_date -- end date for the question (default 7)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_date_time = time + datetime.timedelta(days=end_date)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_date_time)

class QuestionDetailViewTests(TestCase):
    """Testing class for detail (views)."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        User.objects.create_user(username="User1",email='User1@gmail.com',password='isp123456')
        self.client.post(reverse('login'), {'username':'User1', 'password':'isp123456'}, follow=True)
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)