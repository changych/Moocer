import time
import os

from minghua.school.school import School

class Business(object):

	def run(self, school, userName, passward):
		school = School()
		schoolInfo = school.getSchool(school)
		print(schoolInfo)
		#schoolKey = schoolInfo['key']
		#print(schoolKey)
