from django.db import models
from datetime import datetime

from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.utils import timezone

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.filter(date__lt=timezone.now()).order_by("-date")

    def popular_questions(self):
        return self.filter().order_by("-carma")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatar.jpg')


class Question(models.Model):
    question_id = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=CASCADE, related_name="questions")
    date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    carma = models.IntegerField(default=0)
    is_closed = models.IntegerField(default=0)
    answers_number = models.IntegerField(default=0)
    objects = QuestionManager()

class Answer(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=600)
    author = models.ForeignKey(Profile, on_delete=CASCADE, related_name="created_answers")
    related_question = models.ForeignKey(
        Question, on_delete=CASCADE, related_name="answers"
    )
    carma = models.IntegerField(default=0)
    is_correct = models.IntegerField(default=0)


class Tag(models.Model):
    name = models.CharField(max_length=20)
    carma = models.IntegerField(default=0)
    questions = models.ManyToManyField(Question, related_name="tags")


class LikeAnswer(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name="likes_answer")
    value = models.IntegerField(default=0)
    related_answer = models.ForeignKey(Answer, on_delete=CASCADE, related_name="likes")

    class Meta:
        unique_together = ['user', 'related_answer']

class LikeQuestion(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name="likes_question")
    value = models.IntegerField(default=0)
    related_question = models.ForeignKey(Question, on_delete=CASCADE, related_name="likes")
    unique_together = models.BooleanField(default=0)

    class Meta:
        unique_together = ['user', 'related_question']


