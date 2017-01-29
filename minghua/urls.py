from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^updateSchool/$', views.updateSchool, name='updateSchool'),
    url(r'^getSchoolList/$', views.getSchoolList, name='getSchoolList'),
    url(r'^getCourse/$', views.getCourse, name='getCourse'),
    url(r'^addOrder/$', views.addOrder, name='addOrder'),
]