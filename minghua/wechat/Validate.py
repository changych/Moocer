#-*- coding: utf-8 -*-  
import hashlib
import time
import datetime
from lxml import etree
from minghua.quiz.quiz import Quiz
from minghua.user.user import User
from minghua.models import QueryInfo

class Validate(object):

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
		user.update(fromUserName, None, None, None, None)

		msgType = 'text'
		now = int(time.time())
		content = "感谢您的关注。1、本公众号不定期公布名华慕课所有课程答案。\
		2、淘宝网搜索“名华慕课”，可进入名华慕课专业服务。3、回复题目名称可查询答案。"

		res = textTpl%(fromUserName, toUserName, now, msgType, content)
		return res

	def msg(self, data):
		textTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
		#print(data)
		xml = etree.fromstring(data)
		fromUserName = xml.find('FromUserName').text
		toUserName = xml.find('ToUserName').text
		content = xml.find('Content').text

		now = datetime.date.today()

		# 0: 该用户查询记录不存在, 1: 用户查询没超限, 2: 用户查询超限
		queryFlag = 2
		q = QueryInfo.objects.filter(open_id=fromUserName)
		if(len(q) == 0):
			queryFlag = 0
		else:
			if now.year == q[0].last_time.year and now.month == q[0].last_time.month \
				and now.day == q[0].last_time.day and q[0].count >= 5:
				queryFlag = 2
			else:
				queryFlag = 1

		# 构造返回内容
		if queryFlag == 2:
			content = "您今天查询答案次数已达上限，可下单刷课提高上限"
		else:
			quiz = Quiz()
			quizInfo = quiz.getQuizInfo(content)
			if quizInfo == None:
				content = "您所查题目不存在，请查其他题目"
			else:
				quizContent = quizInfo['quiz_content']
				answerContent = quizInfo['answer_content']
				content = "原题：" + quizContent + "\n答案：" + answerContent
				if queryFlag == 0:
					q = QueryInfo(
						open_id=fromUserName, 
						count=1, 
						last_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
					)
					q.save()
				else:
					q.update(
						count=q[0].count+1,
						last_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
					)

		msgType = 'text'
		now = int(time.time())
		

		res = textTpl%(fromUserName, toUserName, now, msgType, content)
		return res

