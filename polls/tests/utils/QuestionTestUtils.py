import datetime

from django.utils import timezone

from polls.models import Question, Choice


class QuestionTestUtils:

    @staticmethod
    def create_question(question_text, days):
        time = timezone.now() + datetime.timedelta(days)
        new_question = Question.objects.create(question_text=question_text, pub_date=time)
        return new_question

    @staticmethod
    def create_choice(choice_text, question_id):
        new_choice = Choice.objects.create(choice_text=choice_text, question_id=question_id)
        return new_choice
