#-*- coding: utf-8 -*-  
import hashlib
import time
import datetime
import json
import os
from lxml import etree
from minghua.quiz.quiz import Quiz
from minghua.user.user import User
from minghua.course.Course import Course
from minghua.school.school import School
from minghua.course.Business import Business
from minghua.models import QueryInfo
from minghua.models import UserInfo
from minghua.models import RecordInfo

class XcxValidate(object):

	def getOpenId(self, loginCode):
		url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxda91b42c38afe4f9&secret=6a50f0b32c167af02221920dd771fb3c&grant_type=authorization_code&js_code='+loginCode
		r = os.popen('curl "' + url + '"')
		return r.read()

	def validate(self, signature, timestmp, nonce):
		token = '715074363yuan'
		params = [token, timestmp, nonce]
		params.sort()
		rawStr = ''.join(params)
		shaStr = hashlib.sha1(rawStr.encode('utf-8')).hexdigest()
		if shaStr == signature:
			return True
		else:
			return False

	def subscribe(self, data):
		textTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"

		xml = etree.fromstring(data)
		fromUserName = xml.find('FromUserName').text
		toUserName = xml.find('ToUserName').text

		user = User()
		user.update(fromUserName, None, None, None, None, 0)

		msgType = 'text'
		now = int(time.time())
		content = "感谢您的关注。1、输入：#账号#密码 绑定账号，如：#123000000#123456。\
		3、绑定账号可输入题目内容查询测试答案。2、淘宝网搜索“名华慕课”，可进入名华慕课专业服务。"

		res = textTpl%(fromUserName, toUserName, now, msgType, content)
		return res