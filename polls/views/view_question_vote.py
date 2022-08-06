from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from polls.models import Choice, Question


class QuestionVoteView:

    def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            choice_id = request.POST['choice']
            selected_choice = question.choice_set.get(pk=choice_id)
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice."
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
