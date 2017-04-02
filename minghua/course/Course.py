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
		courseSet = []

		# 获取所有课程列表
		courseRes = self.browser.session.post(self.urlCourseIndex, data = {
			'keyWord' : '',
			'tabIndex' : '1',
			'searchType' : '0',
			'schoolcourseType' : '0',
			'pageIndex' : '1'
		})

		#print courseRes
		j = pyquery.PyQuery(courseRes.text)
		#print courseRes.content
		#print j('.view-shadow')
		for li in j('.view-item'):
			title = pyquery.PyQuery(li)('.view-title').text()
			subTitile = pyquery.PyQuery(li)('.view-subtitle')
			link = pyquery.PyQuery(subTitile)('a').filter('.link-action')
			href = pyquery.PyQuery(link).attr('href')
			href = href[ : href.rfind('/')]
			courseId = href[href.rfind('/')+1 : ]
			print(courseId)

			video_remain = 0
			video_complete = 0
			test_remain = 0
			test_complete = 0

			videoListRes = browser.get(self.baseUri + '/portal/session/unitNavigation/' + str(courseId) + '.mooc')
			jj = q(videoListRes.content)
			videoListDiv = jj('#unitNavigation')

			for div in videoListDiv('i').items():
				status = pyquery.PyQuery(div).attr('class')
				if status.find('icon-play-done') != -1:
					video_complete = video_complete + 1
				elif status.find('icon-play01') != -1:
					video_remain = video_remain + 1
				elif status.find('icon-edit-done') != -1:
					test_complete = test_complete + 1
				elif status.find('icon-edit02') != -1:
					test_remain = test_remain + 1

			courseSet.append({
				'id': courseId, 
				'title':title, 
				'video-remain': video_remain,
				'video_complete': video_complete,
				'test_remain': test_remain,
				'test_complete': test_complete
			})

		print(courseSet)
		return courseSet	
