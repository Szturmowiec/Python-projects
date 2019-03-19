from django.db import models
import datetime
from django.contrib.auth.models import User

class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

class ReportQuestion(models.Model):
	question=models.CharField(max_length=400)

class Profile(models.Model):
	last_report=models.DateTimeField('Last report submission date',default=None,blank=True,null=True)
	report_tmp=models.IntegerField(default=0)
	last_poll=models.DateTimeField('Last poll submission date',default=None,blank=True,null=True)
	key=models.OneToOneField(User,on_delete=models.CASCADE)