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

class Validate(object):

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
		2、绑定账号可输入题目内容查询测试答案。"

		res = textTpl%(fromUserName, toUserName, now, msgType, content)
		return res

	def msg(self, data):
		textTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
		#print(data)
		xml = etree.fromstring(data)
		fromUserName = xml.find('FromUserName').text
		toUserName = xml.find('ToUserName').text
		content = xml.find('Content').text

		if content.startswith('#'):
			resContent = self.bind(fromUserName, content)
		elif content.startswith('@'):
			resContent = self.course(fromUserName, content)
		else:
			resContent = self.query(fromUserName, content)		

		msgType = 'text'
		now = int(time.time())
		

		res = textTpl%(fromUserName, toUserName, now, msgType, resContent)
		return res

	def course(self, fromUserName, content):
		infoSet = content.split('@')
		if len(infoSet) > 2:
			schoolCh = infoSet[1]
			userName = infoSet[2]

			school = School()
			schoolList = school.getSchool(schoolCh)
			resContent = userName + ":\n"
			if schoolList == None:
				return resContent + '账号/密码错误或未提交订单'
			for schoolInfo in schoolList:
				r = RecordInfo.objects.filter(user=userName)
				for item in r:
					examStart = '未开始' if item.exam_start == None else item.exam_start.strftime('%Y-%m-%d %H:%M')
					resContent = resContent + item.course_title + '(' + \
						str(item.videoremain+item.videocomplete+item.testremain+item.testcomplete) + \
						'/' + str(item.videocomplete+item.testcomplete) + \
						' 分数:' + str(item.score) + ',开始:' + examStart + ")\n" 
				return resContent
			return resContent + '账号/密码错误或未提交订单'

		


	def bind(self, fromUserName, content):
		infoSet = content.split('#')
		content = "请输入：#账号#密码，如：#123000000#123456"
		if len(infoSet) > 2:
			schoolId = infoSet[1]
			schoolPwd = infoSet[2]
			user = User()
			user.update(fromUserName, None, schoolId, schoolPwd, None, 1)
			content = "绑定成功，输入题目内容可查测试答案，淘宝搜“名华慕课”提供刷课考试服务"
		return content


	def query(self, fromUserName, content):
		now = datetime.date.today()
		# 0: 该用户查询记录不存在, 1: 用户查询没超限, 2: 用户查询超限
		queryFlag = 2
		q = QueryInfo.objects.filter(open_id=fromUserName)

		u = UserInfo.objects.filter(open_id=fromUserName)
		quota = 0
		if (len(u) > 0):
			quota = u[0].level * 2
		else:
			user = User()
			user.update(fromUserName, None, '', '', None, 1)

		if (len(q) == 0):
			queryFlag = 0
		else:
			if now.year == q[0].last_time.year and now.month == q[0].last_time.month \
				and now.day == q[0].last_time.day and q[0].count >= quota:
				queryFlag = 2
			else:
				queryFlag = 1

		#print(fromUserName)
		#print(quota)
		#print(content)
		# 构造返回内容
		if queryFlag == 2:
			resContent = "您今天查询答案次数已达上限，绑定账号或淘宝下单刷课可提高上限"
		else:
			quiz = Quiz()
			quizInfo = quiz.getQuizInfo(content)
			#print(quizInfo)
			if quizInfo == None:
				resContent = "您所查题目不存在，请查其他题目"
			else:
				quizContent = quizInfo['quiz_content']
				answerContent = quizInfo['answer_content']
				resContent = "原题：" + quizContent + "\n答案：" + answerContent
				if queryFlag == 0:
					q = QueryInfo(
						open_id=fromUserName, 
						count=1, 
						last_time=now.strftime('%Y-%m-%d %H:%M:%S')
					)
					q.save()
				else:
					q.update(
						count=q[0].count+1,
						last_time=now.strftime('%Y-%m-%d %H:%M:%S')
					)
		return resContent
