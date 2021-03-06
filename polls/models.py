from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class MinghuaQuizInfo(models.Model):
    quiz_id = models.IntegerField(unique=True)
    answer_id = models.CharField(max_length=256)
    mark_result = models.IntegerField()
    mark_quiz_score = models.IntegerField()
    quiz_content = models.CharField(max_length=2048)
    answer_content = models.CharField(max_length=2048)

    def __str__(self):
        return self.quiz_content


@python_2_unicode_compatible
class MinghuaSchoolInfo(models.Model):
    key = models.CharField(max_length=64)
    ch_name = models.CharField(max_length=256)
    en_name = models.CharField(max_length=512)
    url = models.CharField(max_length=1024)

    def __str__(self):
        return self.en_name