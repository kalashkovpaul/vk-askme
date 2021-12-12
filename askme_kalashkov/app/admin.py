from django.contrib import admin

# Register your models here.

from app.models import LikeAnswer, Question, Answer, LikeQuestion, Profile, Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(LikeAnswer)
admin.site.register(Tag)
admin.site.register(LikeQuestion)