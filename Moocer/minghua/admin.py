from django.contrib import admin

# Register your models here.
from .models import QuizInfo
from .models import SchoolInfo

admin.site.register(QuizInfo)
admin.site.register(SchoolInfo)