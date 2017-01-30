#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.http import HttpResponse
from minghua.models import QuizInfo

class Quiz(object):

	def getQuizInfo(self, quizContent):
		print('quiz content:')
		print(quizContent)
		q = QuizInfo.objects.filter(quiz_content__contains=quizContent)
		print q
		if(len(q) == 0):
			return None
		else:
			return q