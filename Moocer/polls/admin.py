from django.contrib import admin

# Register your models here.
from .models import MinghuaQuizInfo
from .models import MinghuaSchoolInfo

admin.site.register(MinghuaQuizInfo)
admin.site.register(MinghuaSchoolInfo)