"""Models for automatically-generated database-access API."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """A Question class has a question, publication date and end date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date closed')

    def __str__(self):
        """Representations the Question object."""
        return self.question_text

    def was_published_recently(self):
        """Return is the question was published less than 1 day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return is the question published yet."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return is the question can vote now."""
        now = timezone.now()
        return self.is_published() and now < self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    is_published.boolean = True
    is_published.short_description = 'Is published?'
    can_vote.boolean = True
    can_vote.short_description = 'Can vote?'


class Choice(models.Model):
    """A Choice class is associated with a Question object."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Representations the Choice object."""
        return self.choice_text
