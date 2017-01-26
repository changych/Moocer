from django.shortcuts import render
from django.http import HttpResponse
from minghua.models import SchoolInfo, QuizInfo
from minghua.school.school import School

def index(request):
	return HttpResponse("Hello, world. You're at the minghua index.")

def updateSchool(request):
	school = School()
	school.updateSchool()
	return HttpResponse('success')


def addSchool(request):
	try:
		s = SchoolInfo.objects.filter(key=request.GET['key'])
		if(len(s) == 0):
			s = SchoolInfo(
				key=request.GET['key'], 
				ch_name=request.GET['ch_name'], 
				en_name=request.GET['en_name'], 
				url=request.GET['url']
			)
			s.save()
		else:
			s.update(
				ch_name=request.GET['ch_name'],
				en_name=request.GET['en_name'],
				url=request.GET['url']
			)
		return HttpResponse(request.GET['ch_name'])
	except (KeyError, SchoolInfo.DoesNotExist):
		s = SchoolInfo(
			key=request.GET['key'], 
			ch_name=request.GET['ch_name'], 
			en_name=request.GET['en_name'], 
			url=request.GET['url']
		)
		s.save()
		return HttpResponse(request.GET['ch_name'])
	
	#return HttpResponse('success')
