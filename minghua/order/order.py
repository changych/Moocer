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
		strTime = now.strftime('%Y%m%d%H%M%S')
		return strTime + str(random.randrange(10000, 99999, 1))