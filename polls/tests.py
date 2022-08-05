import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

QUESTION_LIST_NAME = 'latest_question_list'


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


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.get_response_from_index()
        self.assert_no_recent_questions(response)

    def test_past_question(self):
        question = QuestionTestUtils.create_question("Past question.", -30)
        response = self.get_response_from_index()
        self.assert_response_queryset_equals(response, [question])

    def test_future_question(self):
        QuestionTestUtils.create_question("Future question.", 30)
        response = self.get_response_from_index()
        self.assert_no_recent_questions(response)

    def test_future_and_past_question(self):
        past_question = QuestionTestUtils.create_question("Past question.", -30)
        QuestionTestUtils.create_question("Future question.", 30)
        response = self.get_response_from_index()
        self.assert_response_queryset_equals(response, [past_question])

    def test_two_past_questions_order(self):
        past_question_1 = QuestionTestUtils.create_question("First past question.", -30)
        past_question_2 = QuestionTestUtils.create_question("Seconds past question.", -5)
        response = self.get_response_from_index()
        self.assert_response_queryset_equals(response, [past_question_2, past_question_1])

    def get_response_from_index(self):
        response = self.client.get(reverse('polls:index'))
        return response

    def assert_no_recent_questions(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context[QUESTION_LIST_NAME], [])

    def assert_response_queryset_equals(self, response, expected_queryset):
        self.assertQuerysetEqual(response.context[QUESTION_LIST_NAME], expected_queryset)


class QuestionDetailViewTests(TestCase):

    def test_future_question_not_accessible(self):
        future_question = QuestionTestUtils.create_question("Future question.", 5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_is_accessible(self):
        past_question = QuestionTestUtils.create_question("Past question.", -5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionTestUtils:

    @staticmethod
    def create_question(question_text, days):
        time = timezone.now() + datetime.timedelta(days)
        new_question = Question.objects.create(question_text=question_text, pub_date=time)
        return new_question
