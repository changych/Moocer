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

		return requests.get(url, params = data).text