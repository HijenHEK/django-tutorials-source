from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from .models import Question , Choice
from django.template import loader
from django.urls import reverse

from django.http import Http404
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list' : latest_question_list
    }
    
    return HttpResponse(template.render(context, request))
    
    #or use render and remove loader and HttpResponse
    # return render(request , 'polls/index.html' , context)
def details(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    # or use a try block
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question %s does not exist' % question_id)
    return render(request, 'polls/details.html', {'question': question})
    
def results(request, question_id):
    question = get_object_or_404(Question , pk = question_id)
    return render(request , 'polls/result.html' ,{'question' : question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message' : "You didn't select a choice .",
        })
    else:
        select_choice.votes += 1
        select_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("you are voting on  question %s" % question_id)