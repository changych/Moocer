#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.http import HttpResponse
from minghua.models import RecordInfo

class Record(object):

	def addRecord(self, school, user, password, courseId, videoRemain, videoComplete, testRemain, testComplete):
		r = RecordInfo(
			school=school, 
			user=user, 
			password=password, 
			courseid=courseId,
			videoremain=videoRemain,
			videocomplete=videoComplete,
			testremain=testRemain,
			testcomplete=testComplete
		)
		r.save()

		return True