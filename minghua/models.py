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
class QueryInfo(models.Model):
    open_id = models.CharField(max_length=64,unique=True)
    count = models.CharField(max_length=256)
    last_time = models.DateTimeField()

    def __str__(self):
        return self.open_id
