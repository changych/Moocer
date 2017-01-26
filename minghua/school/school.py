#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys
from chardet import detect

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
			detect(chName)
			print(chardet.detect(chName))
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
