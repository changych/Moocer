#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import datetime
import traceback
import sys
import time

from django.db.models import Q
from django.http import HttpResponse
from minghua.models import Stat

class Stat(object):

	def updateStat(self, school, user, password, courseId, courseTitle, myDuration, avgDuration, myScores, avgScores):
		r = Stat.objects.filter(school=school).filter(courseid=courseId).filter(user=user)
		if(len(r) == 0):
			r = Stat(
				school=school,
				user=user, 
				password=password,
				courseid=courseId,
				course_title=courseTitle,
				my_duration=myDuration,
				avg_duration=avgDuration,
				my_scores=myScores,
				avg_scores=avgScores,
				update_time=updateTime
			)
			r.save()
			resId = r.id
		else:
			r.update(
				my_duration=myDuration,
				avg_duration=avgDuration,
				my_scores=myScores,
				avg_scores=avgScores,
				update_time=updateTime
			)
			resId = r[0].id
		
		return resId