#-*- coding: utf-8 -*-  
import json

from django.shortcuts import render
from django.http import HttpResponse
from minghua.models import SchoolInfo, QuizInfo
from minghua.school.school import School
from minghua.course.Business import Business

def index(request):
	return HttpResponse("Hello, world. You're at the minghua index.")

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

def getSchoolList(request):
	school = School()
	schoolList = school.getSchoolList(
		request.GET['pageSize'],
		request.GET['offset']
	)
	return HttpResponse(json.dumps(schoolList))
