import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=tomorrow)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        a_second_too_old = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=a_second_too_old)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        almost_a_day_ago = timezone.now() - datetime.timedelta(days=0, hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=almost_a_day_ago)
        self.assertIs(recent_question.was_published_recently(), True)
