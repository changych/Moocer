from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import datetime

# Create your models here.
@python_2_unicode_compatible
class QuizInfo(models.Model):
    course_id = models.IntegerField()
    quiz_id = models.IntegerField()
    answer_id = models.CharField(max_length=256)
    mark_result = models.IntegerField()
    mark_quiz_score = models.IntegerField()
    quiz_content = models.CharField(max_length=2048)
    answer_content = models.CharField(max_length=2048)

    def __str__(self):
        return self.quiz_content


@python_2_unicode_compatible
class SchoolInfo(models.Model):
    key = models.CharField(max_length=64,unique=True)
    ch_name = models.CharField(max_length=256)
    en_name = models.CharField(max_length=512)
    url = models.CharField(max_length=1024)

    def __str__(self):
        return self.ch_name

@python_2_unicode_compatible
class OrderInfo(models.Model):
    user = models.CharField(max_length=64)
    school = models.CharField(max_length=256)
    study = models.CharField(max_length=256)
    exam = models.CharField(max_length=256)
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    def __str__(self):
        return self.user

@python_2_unicode_compatible
class RecordInfo(models.Model):
    school = models.CharField(max_length=256)
    user = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    courseid = models.CharField(max_length=64)
    course_title = models.CharField(max_length=512)
    videoremain = models.IntegerField()
    videocomplete = models.IntegerField()
    testremain = models.IntegerField()
    testcomplete = models.IntegerField()
    score = models.IntegerField()
    exam_start = models.DateTimeField()
    exam_end = models.DateTimeField()
    study_status = models.IntegerField()
    exam_status = models.IntegerField()
    update_time = models.DateTimeField()

    def __str__(self):
        return self.user + '(' + str(self.videoremain + self.videocomplete + self.testremain + self.testcomplete) + '/' + str(self.videocomplete + testcomplete) + ')'

@python_2_unicode_compatible
class QueryInfo(models.Model):
    open_id = models.CharField(max_length=64,unique=True)
    count = models.IntegerField(default=0)
    last_time = models.DateTimeField()

    def __str__(self):
        return self.open_id

@python_2_unicode_compatible
class UserInfo(models.Model):
    open_id = models.CharField(max_length=64,unique=True)
    name = models.CharField(max_length=256)
    school_key = models.CharField(max_length=64)
    school_id = models.CharField(max_length=64)
    school_password = models.CharField(max_length=64)
    create_time = models.DateTimeField()
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.open_id
