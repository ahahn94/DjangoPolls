from django.test import TestCase
from django.urls import reverse

from utils.QuestionTestUtils import QuestionTestUtils


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
