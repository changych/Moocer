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
		data['s_from']= 'input'
		data['ie']= 'utf8'
		data['_sug_']= 'n'
		data['_sug_type_']= ''

		result_raw = requests.get(self.sogou_uri, params = data)
		j = pyquery.PyQuery(result_raw.content)

		href = 'none'
		for li in j('.news-list'):
			#txt_box = pyquery.PyQuery(li)('.txt-box')

			href = pyquery.PyQuery(li)('.txt-box')('h3')('a').attr('href')
			href2 = self.html_escape(href)
			title = pyquery.PyQuery(li)('.txt-box')('h3')('a')
			description = pyquery.PyQuery(li)('.txt-box')('p').text

			#href = href + "#######" + href2
			break

		return description

	def html_escape(self, html):
		html = html.replace('&quot;', '"')
		html = html.replace('&amp;', '&')
		html = html.replace('&lt;', '<')
		html = html.replace('&gt;', '>')
		html = html.replace('&nbsp;', ' ')
		return html




