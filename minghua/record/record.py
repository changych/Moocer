#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.db.models import Q
from django.http import HttpResponse
from minghua.models import RecordInfo

class Record(object):

	def addRecord(self, school, user, password, courseId, courseTitle, videoRemain, videoComplete, testRemain, testComplete, examScore, examStart, examEnd, updateTime):
		r = RecordInfo.objects.filter(courseid=courseId).filter(user=user)
		if(len(r) == 0):
			r = RecordInfo(
				school=school,
				user=user, 
				password=password,
				courseid=courseId,
				course_title=courseTitle,
				videoremain=videoRemain,
				videocomplete=videoComplete,
				testremain=testRemain,
				testcomplete=testComplete,
				score=int(examScore),
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
				score=int(examScore),
				update_time=updateTime
			)
		

		return True

	def updateScore(self, user, courseId, examScore, updateTime):
		r = RecordInfo.objects.filter(courseid=courseId).filter(user=user)
		if(len(r) > 0):
			r.update(
				score=int(examScore),
				update_time=updateTime
			)
		return True

	def getUndoStudy(self):
		result = []
		r = RecordInfo.objects.filter(Q(videoremain__gt=0) | Q(testremain__gt=0))
		for record in r:
			result.append({
				'school':record.school, 
				'user':record.user,
				'password':record.password,
				'courseid':record.courseid
			})
		return result



