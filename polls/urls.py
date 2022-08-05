from django.urls import path

from polls.views import QuestionsIndexView, QuestionDetailView, QuestionResultsView, QuestionVoteView

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path('', QuestionsIndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', QuestionDetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', QuestionResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', QuestionVoteView.vote, name='vote'),
]
