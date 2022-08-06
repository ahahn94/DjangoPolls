from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from polls.models import Choice
from utils.QuestionTestUtils import QuestionTestUtils


class QuestionVoteViewTests(TestCase):

    def test_vote_increments_choice(self):
        question = QuestionTestUtils.create_question("Test question.", -1)
        choice_a = QuestionTestUtils.create_choice("Test choice A", question.id)
        choice_b = QuestionTestUtils.create_choice("Test choice B", question.id)
        old_votes_a = choice_a.votes
        old_votes_b = choice_b.votes
        url = reverse('polls:vote', args=(question.id,))
        self.client.post(url, {'choice': choice_b.id})
        new_votes_a = Choice.objects.get(pk=choice_a.id).votes
        new_votes_b = Choice.objects.get(pk=choice_b.id).votes
        self.assertEqual(new_votes_a, old_votes_a)
        self.assertEqual(new_votes_b, old_votes_b + 1)

    def test_vote_redirects_to_results(self):
        question = QuestionTestUtils.create_question("Test question.", -1)
        QuestionTestUtils.create_choice("Test choice A", question.id)
        choice_b = QuestionTestUtils.create_choice("Test choice B", question.id)
        vote_url = reverse('polls:vote', args=[question.id])
        response = self.client.post(vote_url, {'choice': choice_b.id})
        result_url = reverse('polls:results', args=[question.id])
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, result_url)

    def test_empty_choice(self):
        question = QuestionTestUtils.create_question("Test question.", -1)
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url, {'choice': 0})
        result_text_with_escaped_apostrophe = escape("You didn't select a choice.")
        self.assertContains(response, result_text_with_escaped_apostrophe)
