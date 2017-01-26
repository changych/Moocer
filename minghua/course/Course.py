#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import re
import random
import math
import traceback

from minghua.course.Browser import Browser

class Course(object):

	def __init__(self, prefix, browser, userName):
		self.baseUri = 'http://' + prefix + '.minghuaetc.com'
		self.browser = browser
		self.urlCourseIndex = self.baseUri + '/portal/ajaxMyCourseIndex.mooc'

	# 学习所有课程
	def courseList(self):

		courseSet = {}

		# 获取所有课程列表
		courseRes = self.browser.session.post(self.urlCourseIndex, data = {
			'keyWord' : '',
			'tabIndex' : '1',
			'searchType' : '0',
			'schoolcourseType' : '0',
			'pageIndex' : '1'
		})

		#print courseRes
		j = pyquery.PyQuery(courseRes.content)
		#print courseRes.content
		#print j('.view-shadow')
		for li in j('.view-item'):
			title = pyquery.PyQuery(li)('.view-title').text()
			courseSet[1] = title
			# href = pyquery.PyQuery(a).attr('href')
			# courseId = href[href.rfind('/')+1 : len(href)-len('.mooc')]

			# try:
			# 	print(courseId)
			# 	#self.sudyCourse(courseId)
			# 	print('--------------------')	
					
			# 	#print courseId
			# 	#print '--------------------'
			# except Exception as e: 
			# 	traceback.print_exc()
			# 	continue
		return courseSet	