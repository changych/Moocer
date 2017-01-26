import time
import os

from minghua.school.school import School
from minghua.course.Login import Login

class Business(object):

	def run(self, school, userName, password):
		schoolHandler = School()
		schoolInfoList = schoolHandler.getSchool(school)
		for schoolInfo in schoolInfoList:
			login = Login(schoolInfo.key)
			res,browser = login.login(userName, password)
			break
		#schoolKey = schoolInfo['key']
		#print(schoolKey)
