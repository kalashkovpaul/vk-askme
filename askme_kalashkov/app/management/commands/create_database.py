from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from app.models import Question, Answer, Tag, LikeQuestion, LikeAnswer, Profile

test_amount = 100

users_to_create = [
    User.objects.create_user(
    username="username_{}".format(i),
    password="{}".format(i),
    email="test_email_{}@mail.ru".format(i),
    first_name="First_{}_name".format(i),
    last_name="Last_{}_name".format(i),
    )
    for i in range(test_amount + 1)
]

profiles_to_create = [
    Profile(
        user=users_to_create[i]
    )
    for i in range(test_amount + 1)
]

questions_to_create = [
    Question(
        question_id=i,
        title=f"Question #{i}",
        text=f"In this question I will ask... {i} times",
        author=profiles_to_create[i],
        carma=test_amount - i,
        answers_number=1
    )
    for i in range(test_amount)
]

answers_to_create = [
    Answer(
        title=f"Answer #{i}",
        text=f"This is text answer #{i}",
        author=profiles_to_create[i + 1],
        related_question=questions_to_create[i],
        carma=(i - 1),
    )
    for i in range(test_amount)
]

tags_to_create = [
    Tag(
        name="Tag_{}".format(i),
        carma=i
    )
    for i in range(test_amount)
]


class Command(BaseCommand):
    
    def handle(self, **kwargs):
        User.objects.all().delete()
        for user in users_to_create:
            user.save()
        for profile in profiles_to_create:
            profile.save()
        for question in questions_to_create:
            question.save()
        for answer in answers_to_create:
            answer.save()
        for i in range(test_amount):
            tags_to_create[i].save()
            tags_to_create[i].questions.add(questions_to_create[i])
            tags_to_create[i].save()
