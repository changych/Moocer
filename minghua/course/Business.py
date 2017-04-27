#-*- coding: utf-8 -*-  
import time
import os

from minghua.school.school import School
from minghua.course.Login import Login
from minghua.course.Course import Course
from minghua.models import RecordInfo

class Business(object):

	def run(self, school, userName, password):
		r = RecordInfo.objects.filter(school=school).filter(user=userName)
		if(len(r) > 0):
			courseSet = []
			for record in r:
				courseSet.append({
					'id': record.courseid, 
					'title':course.course_title, 
					'video_remain': record.videoremain,
					'video_complete': record.videocomplete,
					'test_remain': record.testremain,
					'test_complete': record.testcomplete,
					'exam_start': record.exam_start,
					'exam_end': record.exam_end,
					'exam_score': record.score
				})
			return courseSet
		else:
			login = Login(school)
			res,browser = login.login(userName, password)
			course = Course(school, browser, userName)
			courseSet = course.courseList()
			#schoolKey = schoolInfo['key']
			#print(schoolKey)
			return courseSet
