#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.http import HttpResponse
from minghua.models import SchoolInfo, QuizInfo

#import Browser
#import LogUtil

class School(object):

	def updateSchool(self):
		j = pyquery.PyQuery(requests.get('http://mooc.minghuaetc.com/school/view/list.mooc').content)
		for li in j('.sc-list li'):
			url = pyquery.PyQuery(li)('.view-img a').attr('href')
			nameSet = []
			for name in pyquery.PyQuery(li)('.shadow-box p'):
				nameSet.append(pyquery.PyQuery(name).text())

			chName = nameSet[0]
			enName = nameSet[1]
			key = url[url.find('//')+2:url.find('.')]
			print(chName)
			s = SchoolInfo.objects.filter(key=key)
			if(len(s) == 0):
				s = SchoolInfo(
					key=key, 
					ch_name=chName, 
					en_name=enName, 
					url=url
				)
				s.save()
			else:
				s.update(
					ch_name=chName,
					en_name=enName,
					url=url
				)

	def getSchool(self, school):
		s = SchoolInfo.objects.filter(ch_name__contains=school) 
		print(s)
		if(len(s) == 0):
			return None
		else:
			return s

	def getSchoolList(self, pageSize, offset):
		result = []
		schoolList = SchoolInfo.objects.all()[int(offset):int(offset)+int(pageSize)]
		for school in schoolList:
			result.append({'key':school.key, 'name':school.ch_name})
		return result
