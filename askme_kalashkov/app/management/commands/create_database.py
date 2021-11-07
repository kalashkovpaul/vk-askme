from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, Like, Profile

test_amount = 10

users_to_create = [
    User(
        username="username_{}".format(i),
        password="0",
        email="test_email_{}@mail.ru".format(i),
        first_name="First_{}_name".format(i),
        last_name="Last_{}_name".format(i),
    )
    for i in range(test_amount + 1)
]

profiles_to_create = [Profile(user=users_to_create[i]) for i in range(test_amount + 1)]

questions_to_create = [
    Question(
        question_id=i,
        title=f"Question #{i}",
        text=f"In this question I will ask... {i} times",
        author=profiles_to_create[i],
        carma=i,
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
        name="Tag_{i}",
        carma=i
        # questions=questions_to_create[i]
    )
    for i in range(test_amount)
]


class Command(BaseCommand):
    
    def handle(self, **kwargs):
        User.objects.all().delete()
        # Profile.objects.all().delete()
        # Question.objects.all().delete()
        # Answer.objects.all().delete()
        # Tag.objects.all().delete()
        for user in users_to_create:
            user.save()
        for profile in profiles_to_create:
            profile.save()
        for question in questions_to_create:
            question.save()
        for answer in answers_to_create:
            answer.save()
        for tag in tags_to_create:
            tag.save()
