#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import datetime
import traceback
import sys
import time

from django.db.models import Q
from django.http import HttpResponse
from minghua.models import RecordInfo

class Record(object):

	def addRecord(self, school, user, password, courseId, courseTitle, videoRemain, videoComplete, testRemain, testComplete, examScore, examStart, examEnd, studyStatus, examStatus, updateTime):
		r = RecordInfo.objects.filter(courseid=courseId).filter(user=user)
		resExamStart = examStart if examStart != '' else None
		resExamEnd = examEnd if examEnd != '' else None
		resId = 0
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
				update_time=updateTime,
				status=0
			)
			r.save()
			resId = r.id
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
			resId = r[0].id
		

		return resId

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
				status=0
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

	def getOneUndoStudy(self):
		result = []
		r = RecordInfo.objects.filter(Q(videoremain__gt=0) | Q(testremain__gt=0)).filter(study_status=1).filter(status=0)
		for record in r:
			result.append({
				'school':record.school, 
				'user':record.user,
				'password':record.password,
				'courseid':record.courseid
			})
			break
		return result

	def getReadyExam(self):
		result = []
		now = datetime.datetime.now()
		start = now + datetime.timedelta(hours=1,minutes=0,seconds=0)
		print(start)
		r = RecordInfo.objects.filter(Q(score__lt=100)).filter(exam_status=1)

		
		for record in r:
			examStart = '' if (record.exam_start == None or record.exam_start == 'NULL') else record.exam_start
			examEnd = '' if (record.exam_end == None or record.exam_end == 'NULL') else record.exam_end
			
			
			try:
				if time.mktime(examStart.timetuple()) < time.time():
					examStart = examStart if type(examStart) is str else examStart.strftime('%Y-%m-%d %H:%M:%S')
					examEnd = examEnd if type(examEnd) is str else examEnd.strftime('%Y-%m-%d %H:%M:%S')
					result.append({
						'school':record.school, 
						'user':record.user,
						'password':record.password,
						'courseid':record.courseid,
						'exam_start': examStart,
						'exam_end': examEnd,
						'exam_score': record.score
					})
			except:
				continue
		return result

	def getOneReadyExam(self):
		result = []
		now = datetime.datetime.now()
		start = now + datetime.timedelta(hours=1,minutes=0,seconds=0)
		print(start)
		r = RecordInfo.objects.filter(Q(score__lt=100)).filter(exam_status=1).filter(status=0)
		
		for record in r:
			examStart = '' if (record.exam_start == None or record.exam_start == 'NULL') else record.exam_start
			examEnd = '' if (record.exam_end == None or record.exam_end == 'NULL') else record.exam_end
			
			try:
				if time.mktime(examStart.timetuple()) < time.time():
					examStart = examStart if type(examStart) is str else examStart.strftime('%Y-%m-%d %H:%M:%S')
					examEnd = examEnd if type(examEnd) is str else examEnd.strftime('%Y-%m-%d %H:%M:%S')
					result.append({
						'school':record.school, 
						'user':record.user,
						'password':record.password,
						'courseid':record.courseid,
						'exam_start': examStart,
						'exam_end': examEnd,
						'exam_score': record.score
					})
					break
			except:
				continue
		return result

	def getEmptyExam(self):
		result = []
		now = datetime.datetime.now()
		start = now + datetime.timedelta(hours=1,minutes=0,seconds=0)
		print(start)
		r = RecordInfo.objects.filter(Q(score__lt=100)).filter(exam_status=1)

		
		for record in r:
			examStart = '' if (record.exam_start == None or record.exam_start == 'NULL') else record.exam_start
			examEnd = '' if (record.exam_end == None or record.exam_end == 'NULL') else record.exam_end
			
			
			try:
				if examStart == '':
					result.append({
						'school':record.school, 
						'user':record.user,
						'password':record.password,
						'courseid':record.courseid,
						'exam_start': examStart,
						'exam_end': examEnd,
						'exam_score': record.score
					})
			except:
				result.append({
					'school':record.school, 
					'user':record.user,
					'password':record.password,
					'courseid':record.courseid,
					'exam_start': examStart,
					'exam_end': examEnd,
					'exam_score': record.score
				})
				continue
		return result


	# status: 0:default(available), 1:doing, 2:finish
	def updateRecordStatus(self, school, user, courseId, status, updateTime):
		r = RecordInfo.objects.filter(school=school).filter(user=user).filter(courseid=courseId)
		if(len(r) > 0):
			r.update(
				status=status,
				update_time=updateTime
			)
		return True

