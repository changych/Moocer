#-*- coding: utf-8 -*-  
import json
import time
import datetime
from pyquery import PyQuery as pq
from lxml import etree
import traceback
import pytz

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from minghua.models import SchoolInfo, QuizInfo
from minghua.school.school import School
from minghua.order.order import Order
from minghua.record.record import Record
from minghua.quiz.quiz import Quiz
from minghua.course.Business import Business
from minghua.wechat.Validate import Validate
from minghua.xiaochengxu.XcxValidate import XcxValidate

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


def xcxValid(request):
	wechatValid = XcxValidate()

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
		res = XcxValidate.subscribe(data)
		event = xml.find('Event').text
		if event == 'subscribe':
			res = XcxValidate.subscribe(data)
		elif event == 'unsubscribe':
			res = XcxValidate.subscribe(data)
	elif msgType == 'text':
		res = XcxValidate.subscribe(data)

	return HttpResponse(res)

	

def updateSchool(request):
	school = School()
	school.updateSchool()
	return HttpResponse('success')

def getCourse(request):
	business = Business()
	try:
		courseSet = business.run(
			request.GET['school_id'], 
			request.GET['user_id'], 
			request.GET['password']
		)
		return HttpResponse(json.dumps(courseSet))
	except: 
		traceback.print_exc()
		return HttpResponse('error')

def updateCourse(request):
	business = Business()
	try:
		courseSet = business.update()
		return HttpResponse(json.dumps(courseSet))
	except: 
		traceback.print_exc()
		return HttpResponse('error')


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
	now = datetime.datetime.now()
	res = order.addOrder(
		request.GET['open_id'],
		request.GET['school'],
		request.GET['user'],
		request.GET['password'],
		request.GET['recordIds'],
		1,
		now.strftime('%Y-%m-%d %H:%M:%S') 
	)
	return HttpResponse(json.dumps({'res':res}))


def addBatchRecord(request):
	now = datetime.datetime.now()
	record = Record()
	recordContent = request.GET['recordContent']
	recordList = json.loads(recordContent)
	recordIds = []
	for item in recordList:
		res = record.addRecord(
			item['school'],
			item['user'],
			item['password'],
			item['courseid'],
			item['course_title'],
			item['videoremain'],
			item['videocomplete'],
			item['testremain'],
			item['testcomplete'],
			item['score'],
			item['exam_start'],
			item['exam_end'],
			item['study_status'],
			item['exam_status'],
			#datetime.datetime.now().strftime("YYYY-MM-DD HH:MM")
			now.strftime('%Y-%m-%d %H:%M:%S') 
		)
		recordIds.append(res)
	return HttpResponse(json.dumps({'res':recordIds}))


def addRecord(request):
	now = datetime.datetime.now()
	record = Record()
	res = record.addRecord(
		request.POST['school'],
		request.POST['user'],
		request.POST['password'],
		request.POST['courseid'],
		request.POST['course_title'],
		request.POST['videoremain'],
		request.POST['videocomplete'],
		request.POST['testremain'],
		request.POST['testcomplete'],
		request.POST['score'],
		request.POST['exam_start'],
		request.POST['exam_end'],
		request.POST['study_status'],
		request.POST['exam_status'],
		#datetime.datetime.now().strftime("YYYY-MM-DD HH:MM")
		now.strftime('%Y-%m-%d %H:%M:%S') 
	)
	return HttpResponse(json.dumps({'status':res}))

def updateRecordScore(request):
	now = datetime.datetime.now()
	record = Record()
	res = record.updateScore(
		request.POST['user'],
		request.POST['courseid'],
		request.POST['score'],
		#datetime.datetime.now().strftime("YYYY-MM-DD HH:MM")
		now.strftime('%Y-%m-%d %H:%M:%S') 
	)
	return HttpResponse(json.dumps({'status':res}))

def updateRecordExam(request):
	now = datetime.datetime.now()
	record = Record()
	res = record.updateExam(
		request.POST['school'],
		request.POST['user'],
		request.POST['password'],
		request.POST['courseid'],
		request.POST['course_title'],
		request.POST['exam_start'],
		request.POST['exam_end'],
		#datetime.datetime.now().strftime("YYYY-MM-DD HH:MM")
		#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		now.strftime('%Y-%m-%d %H:%M:%S') 
	)
	return HttpResponse(json.dumps({'status':res}))

def getUndoStudy(request):
	record = Record()
	recordList = record.getUndoStudy()
	return HttpResponse(json.dumps(recordList))

def getReadyExam(request):
	record = Record()
	recordList = record.getReadyExam()
	return HttpResponse(json.dumps(recordList))

def getOneReadyExam(request):
	record = Record()
	recordList = record.getOneReadyExam()
	return HttpResponse(json.dumps(recordList))

def getEmptyExam(request):
	record = Record()
	recordList = record.getEmptyExam()
	return HttpResponse(json.dumps(recordList))

def getOpenId(request):
	wechatValid = Validate()
	res = wechatValid.getOpenId(request.GET['code'])
	return HttpResponse(json.dumps({'open_id':res}))

def getAnswer(request):
	wechatValid = Validate()
	res = wechatValid.query(
		request.GET['openId'],
		request.GET['quizContent']
	)
	return HttpResponse(json.dumps({'answer':res}))