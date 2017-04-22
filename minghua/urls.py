from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wechatValid/$', views.wechatValid, name='wechatValid'),
    url(r'^updateSchool/$', views.updateSchool, name='updateSchool'),
    url(r'^getSchoolList/$', views.getSchoolList, name='getSchoolList'),
    url(r'^getCourse/$', views.getCourse, name='getCourse'),
    url(r'^getQuiz/$', views.getQuiz, name='getQuiz'),
    url(r'^addQuiz/$', views.addQuiz, name='addQuiz'),
    url(r'^addOrder/$', views.addOrder, name='addOrder'),
    url(r'^addRecord/$', views.addRecord, name='addRecord'),
    url(r'^updateRecordScore/$', views.updateRecordScore, name='updateRecordScore'),
    url(r'^getUndoStudy/$', views.getUndoStudy, name='getUndoStudy'),
    url(r'^updateRecordExam/$', views.updateRecordExam, name='updateRecordExam'),
    url(r'^getOpenId/$', views.getOpenId, name='getOpenId'),
    url(r'^getAnswer/$', views.getAnswer, name='getAnswer'),
]