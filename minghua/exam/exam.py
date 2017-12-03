#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.http import HttpResponse
from minghua.models import ExamInfo

class Exam(object):

	def getExamInfoByQuizId(self, quizId):
		quizId = quizId.strip()
		q = ExamInfo.objects.filter(quiz_id=quizId)
		if(len(q) == 0):
			return None
		else:
			for quiz in q:
				return {
					'answer':quiz.answer,
					'quiz_type':quiz.quiz_type
				}