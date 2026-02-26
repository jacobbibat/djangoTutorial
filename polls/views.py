from django.shortcuts import get_object_or_404, render, redirect
from .models import Question, Choice
from django.utils import timezone

def index(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    # Get the question or return 404 if not found
    question = get_object_or_404(Question, pk=question_id)

    try:
        # Get the choice the user selected
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # If no choice was selected, redisplay the voting form with an error
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Increment the vote count
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect to results page to prevent duplicate submissions
        return redirect('results', question_id=question.id)