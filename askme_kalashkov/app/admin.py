from django.contrib import admin

# Register your models here.

from app.models import Question, Answer, Like, Profile, Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Tag)