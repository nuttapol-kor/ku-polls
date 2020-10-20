"""Takes a Web request and returns a Web response."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Generic views for show question list on index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Generic views for show the result page."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """Vote a choice in the question."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        vote, created = Vote.objects.update_or_create(question=question, user=request.user, defaults={"user_choice": selected_choice})
        if created:
            messages.success(request, "Successfully voted!!")
        else:
            messages.success(request, "Replaces your previous vote successful!!")
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(user_choice=choice).count()
            choice.save()
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def vote_for_poll(request, pk):
    """Show the detail only valid question."""
    question = get_object_or_404(Question, pk=pk)
    if not question.can_vote():
        messages.error(request, "This Question can not vote")
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question})
