#-*- coding: utf-8 -*-  
import requests
import json
import pyquery
import time
import traceback
import sys
import datetime
import random

from django.http import HttpResponse
from minghua.models import OrderInfo

class Order(object):

	def addOrder(self, openId, school, user, password, recordIds, status, createTime):
		orderId = self.genOrderId()
		print(orderId)
		orderId = 'aaaaaaaaa'
		o = OrderInfo(
			order_id=str(orderId),
			open_id=openId,
			school=school, 
			user=user, 
			password=password, 
			record_ids=recordIds,
			status=status,
			create_time=createTime
		)
		o.save()

		return True

	def genOrderId(self):
		now = datetime.datetime.now()
		return str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + \
			str(now.second) + str(now.microsecond) + str(random.randrange(1001,9999,1))