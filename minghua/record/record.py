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
		resExamStart = examStart if examStart != '' else None
		resExamEnd = examEnd if examEnd != '' else None
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
				exam_start=resExamStart,
				exam_end=resExamEnd,
				study_status=studyStatus,
				exam_status=examStatus,
				update_time=updateTime
			)
			r.save()
		else:
			resStudyStatus = studyStatus if int(studyStatus)>0 else r[0].study_status
			resExamStatus = examStatus if int(examStatus)>0 else r[0].exam_status
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

	def updateExam(self, school, user, password, courseId, courseTitle, examStart, examEnd, updateTime):
		r = RecordInfo.objects.filter(courseid=courseId).filter(user=user)
		resExamStart = examStart if examStart != '' else None
		resExamEnd = examEnd if examEnd != '' else None
		if(len(r) > 0):
			r.update(
				exam_status=1,
				exam_start=resExamStart,
				exam_end=resExamEnd,
				update_time=updateTime
			)
		else:
			r = RecordInfo(
				school=school,
				user=user, 
				password=password,
				courseid=courseId,
				course_title=courseTitle,
				videoremain=0,
				videocomplete=0,
				testremain=0,
				testcomplete=0,
				score=0,
				exam_start=resExamStart,
				exam_end=resExamEnd,
				study_status=0,
				exam_status=1,
				update_time=updateTime
			)
			r.save()
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



