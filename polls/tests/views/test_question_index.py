from django.test import TestCase
from django.urls import reverse

from utils.QuestionTestUtils import QuestionTestUtils


class QuestionIndexViewTests(TestCase):
    QUESTION_LIST_NAME = 'latest_question_list'

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
        self.assertQuerysetEqual(response.context[self.QUESTION_LIST_NAME], [])

    def assert_response_queryset_equals(self, response, expected_queryset):
        self.assertQuerysetEqual(response.context[self.QUESTION_LIST_NAME], expected_queryset)
