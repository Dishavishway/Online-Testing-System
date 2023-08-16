from django.contrib import admin
from OTS.models import Candidate
from OTS.models import Question
from OTS.models import Result
# Register your models here.

admin.site.register(Candidate)
admin.site.register(Question)
admin.site.register(Result)