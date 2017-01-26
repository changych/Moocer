from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addSchool/$', views.addSchool, name='addSchool'),
    url(r'^updateSchool/$', views.updateSchool, name='updateSchool'),
]