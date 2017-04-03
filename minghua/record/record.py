#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.http import HttpResponse
from minghua.models import RecordInfo

class Record(object):

	def addRecord(self, school, user, password, courseId, videoRemain, videoComplete, testRemain, testComplete, score, examStart, examEnd, updateTime):
		r = RecordInfo.objects.filter(courseid=courseId).filter(user=user)
		if(len(r) == 0):
			print(examStart)
			print(examEnd)
			print(score)
			r = RecordInfo(
				school=school, 
				user=user, 
				password=password, 
				courseid=courseId,
				videoremain=videoRemain,
				videocomplete=videoComplete,
				testremain=testRemain,
				testcomplete=testComplete,
				score=score,
				exam_start=examStart,
				exam_end=examEnd,
				update_time=updateTime
			)
			r.save()
		else:
			r.update(
				videoremain=videoRemain,
				videocomplete=videoComplete,
				testremain=testRemain,
				testcomplete=testComplete,
				score=score,
				update_time=updateTime
			)
		

		return True