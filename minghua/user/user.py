#-*- coding: utf-8 -*-  
import hashlib
import time
import datetime
from lxml import etree
from minghua.models import UserInfo

class User(object):

	def update(self, openId, schoolKey, schoolId, schoolPwd):
		u = UserInfo.objects.filter(open_id=openId)
		if len(u) == 0:
			u = UserInfo(
				open_id=openId, 
				school_key=schoolKey, 
				school_id=schoolId, 
				school_password=schoolPwd, 
				create_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			)
			u.save()
		else:
			schoolKey = u.school_key if schoolKey == None else schoolKey
			schoolId = u.school_id if schoolId == None else schoolId
			schoolPwd = u.school_password if schoolPwd == None else schoolPwd
			u.update(
				school_key=schoolKey, 
				school_id=schoolId, 
				school_password=schoolPwd, 
			)