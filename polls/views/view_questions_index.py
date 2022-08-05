from django.utils import timezone
from django.views import generic

from polls.models import Question


class QuestionsIndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        questions_published_before_now = Question.objects.filter(pub_date__lte=timezone.now())
        five_most_recent_questions = questions_published_before_now.order_by('-pub_date')[:5]
        return five_most_recent_questions
