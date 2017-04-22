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

		for li in j('li'):
			href = pyquery.PyQuery(li)('.view-shadow').attr('href')
			if href == None:
				continue
			courseId = href[href.rfind('/')+1 : len(href)-len('.mooc')]




		# for li in j('.view-item'):
		# 	title = pyquery.PyQuery(li)('.view-title').text()
		# 	subTitile = pyquery.PyQuery(li)('.view-subtitle')
		# 	link = pyquery.PyQuery(subTitile)('a').filter('.link-action')
		# 	href = pyquery.PyQuery(link).attr('href')
		# 	href = href[ : href.rfind('/')]
		# 	courseId = href[href.rfind('/')+1 : ]
		# 	print(courseId)

			video_remain = 0
			video_complete = 0
			test_remain = 0
			test_complete = 0

			videoListRes = self.browser.session.get(self.baseUri + '/portal/session/unitNavigation/' + str(courseId) + '.mooc')
			jj = pyquery.PyQuery(videoListRes.content)
			videoListDiv = jj('#unitNavigation')
			title = jj('.model-title').attr('title')

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


			examStart = ''
			examEnd = ''
			examScore = 0
			examFlag = 1 if videoListRes.content.decode().find('线上考试') != -1 else 0
			if examFlag == 1:
				examListRes = self.browser.session.get(self.baseUri + '/portal/examine/list/' + str(courseId) + '.mooc')
				itemList = pyquery.PyQuery(examListRes.content)('.flipped-item')
				for item in itemList:
					examId = pyquery.PyQuery(item)('.btn-area').attr('examineid')
					timeList = pyquery.PyQuery(item)('.fclass-para')
					for time in timeList:
						text = pyquery.PyQuery(time).text()
						if text.find('开始') != -1:
							examStart = text[text.find('：')+1:]
						if text.find('截止') != -1:
							examEnd = text[text.find('：')+1:]
						if text.find('得分') != -1:
							examScore = text[text.find('：')+1:]
							examScore = examScore[:len(examScore)-1]

			courseSet.append({
				'id': courseId, 
				'title':title, 
				'video_remain': video_remain,
				'video_complete': video_complete,
				'test_remain': test_remain,
				'test_complete': test_complete,
				'exam_start': examStart,
				'exam_end': examEnd,
				'exam_score': examScore
			})

		print(courseSet)
		return courseSet	
