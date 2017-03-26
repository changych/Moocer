#-*- coding: utf-8 -*-  
import hashlib
import time
import datetime
from lxml import etree
from minghua.models import UserInfo

class User(object):

	def update(self, openId, schoolKey, schoolId, schoolPwd, name, level):
		u = UserInfo.objects.filter(open_id=openId)
		if len(u) == 0:
			schoolKey = '' if schoolKey == None else schoolKey
			schoolId = '' if schoolId == None else schoolId
			schoolPwd = '' if schoolPwd == None else schoolPwd
			name = '' if name == None else name
			level = '' if level == None else level
			u = UserInfo(
				open_id=openId, 
				school_key=schoolKey, 
				school_id=schoolId, 
				school_password=schoolPwd, 
				name=name, 
				level=level,
				create_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			)
			u.save()
		else:
			schoolKey = u[0].school_key if schoolKey == None else schoolKey
			schoolId = u[0].school_id if schoolId == None else schoolId
			schoolPwd = u[0].school_password if schoolPwd == None else schoolPwd
			name = u[0].name if name == None else name
			level = u[0].name if level == None else level
			u.update(
				school_key=schoolKey, 
				school_id=schoolId, 
				school_password=schoolPwd, 
				name=name, 
				level=level,
			)
