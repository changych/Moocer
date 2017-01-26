import time
import os

from minghua.school.school import School

class Business(object):

	def run(self, school, userName, passward):
		schoolHandler = School()
		print(school)
		schoolInfo = schoolHandler.getSchool(school)
		print(schoolInfo)
		#schoolKey = schoolInfo['key']
		#print(schoolKey)
