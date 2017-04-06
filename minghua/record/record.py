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

	def addRecord(self, school, user, password, courseId, courseTitle, videoRemain, videoComplete, testRemain, testComplete, examScore, examStart, examEnd, studyStatus, examStatus, updateTime):
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
				study_status=studyStatus,
				exam_status=examStatus,
				update_time=updateTime
			)
			r.save()
		else:
			resStudyStatus = studyStatus if studyStatus>0 else r[0].study_status
			resExamStatus = examStatus if examStatus>0 else r[0].exam_status
			resScore = examScore if int(examScore)>0 else r[0].score
			r.update(
				videoremain=videoRemain,
				videocomplete=videoComplete,
				testremain=testRemain,
				testcomplete=testComplete,
				score=resScore,
				study_status=resStudyStatus,
				exam_status=resExamStatus,
				update_time=updateTime
			)
		

		return True

	def updateScore(self, user, courseId, examScore, updateTime):
		r = RecordInfo.objects.filter(courseid=courseId).filter(user=user)
		if(len(r) > 0):
			r.update(
				exam_status=1,
				score=int(examScore),
				update_time=updateTime
			)
		return True

	def getUndoStudy(self):
		result = []
		r = RecordInfo.objects.filter(Q(videoremain__gt=0) | Q(testremain__gt=0)).filter(study_status=1)
		for record in r:
			result.append({
				'school':record.school, 
				'user':record.user,
				'password':record.password,
				'courseid':record.courseid
			})
		return result



