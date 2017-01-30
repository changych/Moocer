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
		q = QuizInfo.objects.filter(quiz_content__contains=quizContent)
		print(q)
		if(len(q) == 0):
			return None
		else:
			return q

	def addQuizInfo(self, courseId, quizId, answerId, markResult, markQuizScore, quizContent, answerContent):
		q = QuizInfo.objects.filter(course_id=courseId).filter(quiz_id=quizId)
		print(q)
		if(len(q) == 0):
			q = QuizInfo(
				course_id=courseId, 
				quiz_id=quizId, 
				answer_id=answerId, 
				mark_result=markResult,
				mark_quiz_score=markQuizScore,
				quiz_content=quizContent,
				answer_content=answerContent
			)
			q.save()
		else:
			q.update(
				answer_id=answerId, 
				mark_result=markResult,
				mark_quiz_score=markQuizScore,
				quiz_content=quizContent,
				answer_content=answerContent
			)
		return True