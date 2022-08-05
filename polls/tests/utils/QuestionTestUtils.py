import datetime

from django.utils import timezone

from polls.models import Question


class QuestionTestUtils:

    @staticmethod
    def create_question(question_text, days):
        time = timezone.now() + datetime.timedelta(days)
        new_question = Question.objects.create(question_text=question_text, pub_date=time)
        return new_question
