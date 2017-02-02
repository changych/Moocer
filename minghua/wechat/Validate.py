#-*- coding: utf-8 -*-  
import hashlib
import time
import datetime
from lxml import etree
from minghua.quiz.quiz import Quiz
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

		q = QueryInfo.objects.filter(open_id=fromUserName)
		if(len(q) == 0):
			quiz = Quiz()
			quizInfo = quiz.getQuizInfo(content)
			quizContent = quizInfo['quiz_content']
			answerContent = quizInfo['answer_content']
			q = QueryInfo(
				open_id=fromUserName, 
				count=1, 
				last_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			)
			q.save()
			content = "原题：" + quizContent + "\n答案：" + answerContent
		else:
			now = datetime.now()
			count = q[0].count
			lastTime = q[0].last_time
			lastTime = lastTime.replace(tzinfo=None)
			if now.yaer == lastTime.year and now.month == lastTime.month and now.day == lastTime.day \
			and count >= 5:
				print(lastTime)
				content = "您今天查询答案次数已达上限，可下单刷课提高上限"		

		msgType = 'text'
		now = int(time.time())
		

		res = textTpl%(fromUserName, toUserName, now, msgType, content)
		return res

