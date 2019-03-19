from django.shortcuts import get_object_or_404, render
from django.http import *
from .models import *
from django.template import loader
from django.urls import reverse
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
import datetime
import os
from django.utils import timezone
now=timezone.now()

def start(request):
	return render(request,'polls/begin.html')

@login_required
def index(request):
    if request.user.profile.last_poll is None or now.day-request.user.profile.last_poll.day>=1:
        request.user.profile.last_poll=now
        request.user.profile.save()
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)
    else :
        return render(request, 'polls/index.html', {
            'error_message': "You can vote in poll only once per day.",
        })

@login_required
def page(request):
    return render(request,'polls/page.html')

@login_required
def results(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/results.html', {'q_list': latest_question_list})

@login_required
def report(request):
    answer=request.POST.getlist('textfield')
    if (request.user.profile.last_report is None or now.day-request.user.profile.last_report.day>=1) or request.user.profile.report_tmp==1:
        request.user.profile.report_tmp+=1
        latest_question_list2 = ReportQuestion.objects.order_by('-question')[:5]
        context = {'latest_question_list2': latest_question_list2}
        f=open("report_"+str(request.user)+now.strftime("%Y-%m-%d %H:%M"),"a")
        for (q,a) in zip(latest_question_list2,answer):
            f.write(q.question)
            f.write(": ")
            if a=="": f.write("unanswered")
            else: f.write(a)
            f.write("\n")
        if len(answer)>0:
            f.write("\nThis report was written by ")
            f.write(str(request.user))
            f.write(" at "+now.strftime("%Y-%m-%d %H:%M"))
        request.user.profile.last_report=now
        request.user.profile.save()
        if request.user.profile.report_tmp==1: return render(request,'polls/report.html',context)
        else:
            request.user.profile.report_tmp=0
            request.user.profile.save()
            return render(request,'polls/report2.html')
    else:
        request.user.profile.report_tmp=0
        request.user.profile.save()
        return render(request,'polls/report2.html', {
                'error_message': "You can submit only one report per day."
                })


@login_required
def vote(request):
    a=[]
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    try:
        for q in latest_question_list:
            selected_choice = q.choice_set.get(pk=request.POST['choice_{}'.format(q.id)])
            a.append(selected_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/index.html', {
            'question': q,
            'error_message': "No choice has been selected.",
        })
    else:
        for i in a:
            i.votes += 1
            i.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results'))