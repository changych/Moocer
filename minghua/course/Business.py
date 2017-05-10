#-*- coding: utf-8 -*-  
import time
import os
import datetime
from django.db.models import Q

from minghua.school.school import School
from minghua.course.Login import Login
from minghua.course.Course import Course
from minghua.models import RecordInfo
from minghua.record.record import Record

class Business(object):

	def update(self):
		now = datetime.datetime.now()
		start = now + datetime.timedelta(hours=-24,minutes=0,seconds=0)
		print(start)
		sql = 'SELECT * FROM minghua_recordinfo WHERE update_time<\"' + str(start) + '\" and (videoremain>0 or testremain>0) GROUP BY user'
		print(sql)
		userSet = []
		r = RecordInfo.objects.raw(sql)
		for record in r:
			userSet.append({
				'school': record.school,
				'user': record.user,
				'password': record.password
			})
			
		return userSet

	def run(self, school, userName, password):
		now = datetime.datetime.now()
		# r = RecordInfo.objects.filter(school=school).filter(user=userName)
		# if(len(r) > 0):
		# 	courseSet = []
		# 	for record in r:
		# 		courseSet.append({
		# 			'id': record.courseid, 
		# 			'title':record.course_title, 
		# 			'video_remain': record.videoremain,
		# 			'video_complete': record.videocomplete,
		# 			'test_remain': record.testremain,
		# 			'test_complete': record.testcomplete,
		# 			'exam_start': str(record.exam_start),
		# 			'exam_end': str(record.exam_end),
		# 			'exam_score': record.score,
		# 			'study_status': record.study_status,
		# 			'exam_status': record.exam_status
		# 		})
		# 	return courseSet
		# else:
		login = Login(school)
		res,browser = login.login(userName, password)
		course = Course(school, browser, userName)
		courseSet = course.courseList()
		record = Record()
		for course in courseSet:
			studyStatus = 0
			examStatus = 0
			r = RecordInfo.objects.filter(school=school).filter(user=userName).filter(courseid=course['id'])
			if(len(r) > 0):
				studyStatus = r[0].study_status
				examStatus = r[0].exam_status
			res = record.addRecord(
				school,
				userName,
				password,
				course['id'],
				course['title'],
				course['video_remain'],
				course['video_complete'],
				course['test_remain'],
				course['test_complete'],
				course['exam_score'],
				course['exam_start'],
				course['exam_end'],
				studyStatus,
				examStatus,
				now.strftime('%Y-%m-%d %H:%M:%S')
			)
		#schoolKey = schoolInfo['key']
		#print(schoolKey)
		return courseSet
