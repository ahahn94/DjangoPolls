from django.utils import timezone
from django.views import generic

from polls.models import Question


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        already_published_questions = Question.objects.filter(pub_date__lte=timezone.now())
        return already_published_questions
