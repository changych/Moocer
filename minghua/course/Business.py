#-*- coding: utf-8 -*-  
import time
import os

from minghua.school.school import School
from minghua.course.Login import Login
from minghua.course.Course import Course

class Business(object):

	def run(self, school, userName, password):
		login = Login(school)
		res,browser = login.login(userName, password)
		course = Course(school, browser, userName)
		courseSet = course.courseList()
		#schoolKey = schoolInfo['key']
		#print(schoolKey)
		return courseSet
