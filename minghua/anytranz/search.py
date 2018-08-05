#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.http import HttpResponse

#import Browser
#import LogUtil

class Search(object):

	def __init__(self):
		self.sogou_uri = "http://weixin.sogou.com/weixin?type=2"
		self.sogou_search_type_artilce = 2
		self.sogou_search_type_site = 1

	def getInfo(self, area, language, job_type):
		keyword = area + "+" + language + "+" + job_type
		data = {}
		data['type'] = self.sogou_search_type_artilce
		data['query'] = keyword

		result_raw = requests.get(self.sogou_uri, params = data)
		j = pyquery.PyQuery(result_raw.content)

		href = 'none'
		for li in j('.news-list'):
			href = pyquery.PyQuery(li)('div')('a').attr('href')
			break

		return href