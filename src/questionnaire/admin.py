from django.contrib import admin
from .models import Questionnaire, Choice, Answer

admin.site.register(Questionnaire)
admin.site.register(Choice)
admin.site.register(Answer)
