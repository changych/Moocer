#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys
import datetime

from django.http import HttpResponse
from minghua.models import JobInfo

#import Browser
#import LogUtil

class Search(object):

	def __init__(self):
		self.sogou_uri = "http://weixin.sogou.com/weixin?type=2"
		self.sogou_search_type_artilce = 2
		self.sogou_search_type_site = 1
		self.secret = "Lindi1!"

	def getInfo(self, area, language, job_type, page):
		keyword = area + " " + language + " " + job_type
		data = {}
		data['type'] = self.sogou_search_type_artilce
		data['query'] = keyword
		data['page'] = page
		data['s_from']= 'input'
		data['ie']= 'utf8'
		data['_sug_']= 'n'
		data['_sug_type_']= ''

		result_raw = requests.get(self.sogou_uri, params = data)
		
		j = pyquery.PyQuery(result_raw.content)

		href = 'none'
		job_list = []
		for li in j('li'):

			#print(pyquery.PyQuery(li).html())
		
			href = pyquery.PyQuery(li)('h3')('a').attr('href')
			title = pyquery.PyQuery(li)('h3')('a').text()
			description = pyquery.PyQuery(li)('p').text()
			timestamp = pyquery.PyQuery(li)('.s-p').attr('t')
			account = pyquery.PyQuery(li)('.account').text()

			print(timestamp)
			print(account)
			
			if title != '':
				job_list.append({
					'title': title,
					'description': description,
					'link': href
				})

				j = JobInfo.objects.filter(title=title).filter(account=account)
				d = datetime.datetime.fromtimestamp(float(timestamp))
				deliver_time = d.strftime("%Y-%m-%d %H:%M:%S.%f")
				if(len(j) == 0):
					j = JobInfo(
						title=title, 
						description=description, 
						url=href,
						deliver_time=deliver_time,
						account=account,
						keyword=keyword
					)
					j.save()
				else :
					j.update(
						url=href
					)

			#href = href + "#######" + href2
			#break

		return job_list

	def save(self, title, account, timestamp, description, url, keyword, secret):
		if secret === self.secret:
			j = JobInfo.objects.filter(title=title).filter(account=account)
			d = datetime.datetime.fromtimestamp(float(timestamp))
			deliver_time = d.strftime("%Y-%m-%d %H:%M:%S.%f")
			if(len(j) == 0):
				j = JobInfo(
					title=title, 
					description=description, 
					url=url,
					deliver_time=deliver_time,
					account=account,
					keyword=keyword
				)
				j.save()
			else :
				j.update(
					url=href
				)

	def html_escape(self, html):
		html = html.replace('&quot;', '"')
		html = html.replace('&amp;', '&')
		html = html.replace('&lt;', '<')
		html = html.replace('&gt;', '>')
		html = html.replace('&nbsp;', ' ')
		return html




