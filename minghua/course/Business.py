#-*- coding: utf-8 -*-  
import time
import os

from minghua.school.school import School
from minghua.course.Login import Login
from minghua.course.Course import Course
from minghua.models import RecordInfo
from minghua.record.record import Record

class Business(object):

	def run(self, school, userName, password):
		r = RecordInfo.objects.filter(school=school).filter(user=userName)
		if(len(r) > 0):
			courseSet = []
			for record in r:
				courseSet.append({
					'id': record.courseid, 
					'title':record.course_title, 
					'video_remain': record.videoremain,
					'video_complete': record.videocomplete,
					'test_remain': record.testremain,
					'test_complete': record.testcomplete,
					'exam_start': str(record.exam_start),
					'exam_end': str(record.exam_end),
					'exam_score': record.score
				})
			return courseSet
		else:
			login = Login(school)
			res,browser = login.login(userName, password)
			course = Course(school, browser, userName)
			courseSet = course.courseList()
			for course in courseSet:
				res = record.addRecord(
					school,
					userName,
					password,
					course.id,
					course.title,
					course.video_remain,
					course.video_complete,
					course.test_remain,
					course.test_complete,
					course.exam_score,
					course.exam_start,
					course.exam_end,
					0,
					0,
					#datetime.datetime.now().strftime("YYYY-MM-DD HH:MM")
					time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				)
			#schoolKey = schoolInfo['key']
			#print(schoolKey)
			return courseSet
