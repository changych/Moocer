#-*- coding: utf-8 -*-  
import json
import time
import datetime
from pyquery import PyQuery as pq
from lxml import etree

from django.shortcuts import render
from django.http import HttpResponse
from minghua.models import SchoolInfo, QuizInfo
from minghua.school.school import School
from minghua.order.order import Order
from minghua.record.record import Record
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
	xml = etree.fromstring(data)
	msgType = xml.find('MsgType').text

	# for key in request.GET:
	# 	#rec = request.stream.read()
	# 	print(key)
	# 	print(request.GET[key])
	#if res == True:
	#	return HttpResponse(echoStr)
	#else:
	#	return HttpResponse('error')

	res = 'end'
	if msgType == 'event':
		res = wechatValid.subscribe(data)
		event = xml.find('Event').text
		if event == 'subscribe':
			res = wechatValid.subscribe(data)
		elif event == 'unsubscribe':
			res = wechatValid.subscribe(data)
	elif msgType == 'text':
		res = wechatValid.msg(data)

	return HttpResponse(res)

	

def updateSchool(request):
	school = School()
	school.updateSchool()
	return HttpResponse('success')

def getCourse(request):
	school = School()
	schoolList = school.getSchool(request.GET['school'])
	for schoolInfo in schoolList:
		print(schoolInfo.key)
		business = Business()
		try:
			courseSet = business.run(
				schoolInfo.key, 
				'1334421', 
				'123456'
			)
			return HttpResponse(json.dumps(courseSet))
		except: 
			continue


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

def addRecord(request):
	record = Record()
	res = record.addRecord(
		request.POST['school'],
		request.POST['user'],
		request.POST['password'],
		request.POST['courseid'],
		request.POST['videoremain'],
		request.POST['videocomplete'],
		request.POST['testremain'],
		request.POST['testcomplete'],
		request.POST['score'],
		time.strptime(request.POST['exam_start'], "%Y-%m-%d %H:%M"),
		time.strptime(request.POST['exam_end'], "%Y-%m-%d %H:%M"),
		time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	)
	return HttpResponse(json.dumps({'status':res}))
