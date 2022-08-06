from django.test import TestCase

from polls.models import Choice


class ChoiceModelTests(TestCase):

    def test_to_string(self):
        text = "To String Test"
        choice = Choice(choice_text=text)
        self.assertEqual(choice.__str__(), text)
