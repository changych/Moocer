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
		for li in j('li'):
			#txt_box = pyquery.PyQuery(li)('.txt-box')

			print(pyquery.PyQuery(li).html())
			print("##################")

			href = pyquery.PyQuery(li)('h3')('a').attr('href')
			print(href)
			print("******************")

			#]href2 = self.html_escape(href)
			#print(href2)
			#print("##################")

			title = pyquery.PyQuery(li)('h3')('a').text()
			print(title)
			print("******************")

			description = pyquery.PyQuery(li)('p').text()
			print(description)
			print("******************")

			#href = href + "#######" + href2
			#break

		return ''

	def html_escape(self, html):
		html = html.replace('&quot;', '"')
		html = html.replace('&amp;', '&')
		html = html.replace('&lt;', '<')
		html = html.replace('&gt;', '>')
		html = html.replace('&nbsp;', ' ')
		return html




