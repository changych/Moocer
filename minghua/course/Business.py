import time
import os

from minghua.school.school import School
from Login import Login

class Business(object):

	def run(self, school, userName, passward):
		schoolHandler = School()
		print(school)
		schoolInfoList = schoolHandler.getSchool(school)
		for schoolInfo in schoolInfoList:
			print(schoolInfo.key)
			login = Login.Login(schoolKey)
			res,browser = login.login(userName, password)
			break
		#schoolKey = schoolInfo['key']
		#print(schoolKey)
