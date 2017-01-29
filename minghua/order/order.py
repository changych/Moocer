#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys

from django.http import HttpResponse
from minghua.models import OrderInfo

class Order(object):

	def addOrder(self, school, user, study, exam):
		o = OrderInfo(
			school=school, 
			user=user, 
			study=study, 
			exam=exam,
		)
		o.save()

		return True