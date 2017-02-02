#-*- coding: utf-8 -*-  
import json
from pyquery import PyQuery as pq
from lxml import etree

from django.shortcuts import render
from django.http import HttpResponse
from minghua.models import SchoolInfo, QuizInfo
from minghua.school.school import School
from minghua.order.order import Order
from minghua.quiz.quiz import Quiz
from minghua.course.Business import Business
from minghua.wechat.Validate import Validate

def index(request):
	return HttpResponse("Hello, world. You're at the minghua index.")

def wechatValid(request):
	wechatValid = Validate()

	#echoStr = request.GET['echostr']
	#signature = request.GET['signature']
	#timestamp = request.GET['timestamp']
	#nonce = request.GET['nonce']	
	#res = wechatValid.validate(signature, timestamp, nonce)

	data = request.body
	#print(data)
	xml = etree.fromstring(data)
	# fromUserName = xml.find('FromUserName').text
	# toUserName = xml.find('ToUserName').text
	# createTime = xml.find('CreateTime').text
	# msgType = xml.find('MsgType').text
	event = xml.find('Event').text
	# eventKey = xml.find('EventKey').text
	
	# print(fromUserName)
	# print(toUserName)
	# print(createTime)
	# print(msgType)
	# print(event)
	# print(eventKey)

	# for key in request.GET:
	# 	#rec = request.stream.read()
	# 	print(key)
	# 	print(request.GET[key])
	#if res == True:
	#	return HttpResponse(echoStr)
	#else:
	#	return HttpResponse('error')

	res = 'end'
	if event == 'subscribe':
		res = wechatValid.subscribe(data)
	elif: event == 'unsubscribe':
		res = wechatValid.subscribe(data)

	return HttpResponse(res)

	

def updateSchool(request):
	school = School()
	school.updateSchool()
	return HttpResponse('success')

def getCourse(request):
	business = Business()
	courseSet = business.run(
		request.GET['school'], 
		request.GET['user_name'], 
		request.GET['password']
	)
	return HttpResponse(json.dumps(courseSet))

def addQuiz(request):
	quiz = Quiz()
	res = quiz.addQuizInfo(
		request.POST['course_id'],
		request.POST['quiz_id'],
		request.POST['answer_id'],
		request.POST['mark_result'],
		request.POST['mark_quiz_score'],
		request.POST['quiz_content'],
		request.POST['answer_content']
	)
	return HttpResponse(json.dumps({'status':res}))

def getQuiz(request):
	quiz = Quiz()
	quizSet = quiz.getQuizInfo(
		request.GET['quiz_content']
	)
	return HttpResponse(json.dumps(quizSet))

def getSchoolList(request):
	school = School()
	schoolList = school.getSchoolList(
		request.GET['pageSize'],
		request.GET['offset']
	)
	return HttpResponse(json.dumps(schoolList))

def addOrder(request):
	order = Order()
	res = order.addOrder(
		request.GET['school'],
		request.GET['user'],
		request.GET['study'],
		request.GET['exam']
	)
	return HttpResponse(json.dumps({'status':res}))
