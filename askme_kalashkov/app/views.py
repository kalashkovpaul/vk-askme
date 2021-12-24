from typing import Set
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import auth
from django.urls import reverse

from .models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from .forms import AnswerForm, LoginForm, SettingsForm, SingUpForm, QuestionForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number=request.GET.get('page')
    content=paginator.get_page(page_number)
    return content

def index(request):
    new_questions = Question.objects.new_questions()
    content = paginate(new_questions, request, 5)
    context = {
        'contents': content,
        'new_questions': content,
        'next': 'index'
    }
    return render(request, "index.html", context=context)


q_id = 0
def question(request):
    global q_id
    if request.method == 'GET':
        question_id=request.GET.get('id')
        q_id = question_id
        question = Question.objects.get(id=question_id)
        answers=question.answers.all()
        form = AnswerForm()
        content = paginate(answers, request,5)
        context = {
            'question': question,
            'contents':content,
            'answers': content,
            'next': 'question',
            'id': question_id,
            'form': form
        }
        print("OOOOOO")
        print(question.answers.all())
        return render(request, "question.html", context=context)
    if request.method == 'POST':
        form = AnswerForm(data=request.POST)
        print(form.data)
        print(q_id)
        question = Question.objects.get(id=q_id)
        print(question)
        print(question.title)
        question.answers.create(
            title=form.data['title'],
            text=form.data['answer'],
            author=Profile.objects.get(user=request.user),
            related_question=question,
            id=len(Answer.objects.all()) + 1
        )
        question.answers_number += 1
        question.save()
        print("OOOOOO")
        print(question.answers.all())
        return redirect("{}?id={}".format(reverse("question"), q_id))


@login_required(login_url='login')
def ask(request):
    if request.method == 'GET':
        form = QuestionForm()
    elif request.method == 'POST':
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            new_question = Question(
                title=form.cleaned_data['title'],
                question_id=len(Question.objects.all()),
                text=form.cleaned_data['text'],
                author=Profile.objects.get(user=request.user),
                carma=0
            )
            print(new_question)
            new_question.save()
            print(form.cleaned_data)
            tag_names = form.cleaned_data['tags'].split()
            first_tag = Tag.objects.filter(name=tag_names[0])
            if not first_tag:
                first_tag = Tag(name=tag_names[0], id=len(Tag.objects.all()))
            else:
                first_tag = Tag.objects.get(name=tag_names[0])
                first_tag.carma += 1
            first_tag.save()
            first_tag.questions.add(new_question)
            if len(tag_names) > 1:
                second_tag = Tag.objects.filter(name=tag_names[1])
                if not first_tag:
                    second_tag = Tag(name=tag_names[1])
                else:
                    second_tag = Tag.objects.get(name=tag_names[1])
                    second_tag.carma += 1
                second_tag.save()
                second_tag.questions.add(new_question)
            if len(tag_names) > 2:
                third_tag = Tag.objects.filter(name=tag_names[2])
                if not first_tag:
                    third_tag = Tag(name=tag_names[2])
                else:
                    third_tag = Tag.objects.get(name=tag_names[2])
                    third_tag.carma += 1
                third_tag.save()
                third_tag.questions.add(new_question)
            return redirect("{}?id={}".format(reverse("question"), new_question.id))
    return render(request, "ask.html", {'form': form})


result_page = 'index'
result_id = 0

def login(request):
    global result_page
    global result_id
    if request.method == 'GET':
        result_page = request.GET.get('next')
        result_page.replace("/", "")
        if not result_page:
            result_page = 'index'
        result_id = request.GET.get('id')
        form = LoginForm()
        print(result_page)
        print(result_id)
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, "User not found!")
            else:
                auth.login(request, user)
                print(result_page)
                print(result_id)
                if result_id:
                    return redirect("{}?id={}".format(reverse(result_page), result_id))
                return redirect(reverse(result_page))

    return render(request, "login.html", {'form': form})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    if (request.method == 'GET'):
        print(request.GET)
        return_page = request.GET.get('next')
        return_id = request.GET.get('id')
        if not return_page:
            return_page = 'index'
        print(return_page)
        print(return_id)
        if return_page and return_id:
            return redirect("{}?id={}".format(reverse(return_page), return_id))
        if return_page:
            return redirect(reverse(return_page))
    return redirect(reverse('index'))

def register(request):
    if request.method == 'GET':
        form = SingUpForm()
    elif request.method == 'POST':
        form = SingUpForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.save()
            profile = Profile(user=user)
            profile.save()
            new_user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth.login(request, new_user)
            return redirect(reverse('index'))
    return render(request, "register.html", {'form': form})

@login_required(login_url='login')
def settings(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        user = request.user
        name = user.username
        email= user.email
        profile = Profile.objects.get(user=user)
        form = SettingsForm(initial=initial_data,
            data={
            'username': name,
            'email': email,
            'profile': profile,
            'avatar': request.user.profile.avatar
            })
    elif request.method == 'POST':
        form = SettingsForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            return redirect(reverse('edit'))
    return render(request, "settings.html", {'form': form, 'username': user.get_username()})

def tagged(request):
    id = request.GET.get('id')
    searched_tag = Tag.objects.get(id=id)
    tag_id = searched_tag.id
    questions = Question.objects.all()
    tagged_questions = []
    for question in questions:
        for tag in question.tags.all():
            if (tag.id == tag_id):
                tagged_questions.append(question)
    content = paginate(tagged_questions, request, 5)
    context = {
        'tag': searched_tag,
        'tagged_questions': content,
        'contents': content,
        'next': 'tag',
        'id': id
    }
    return render(request, "tagged_questions.html", context=context)

def hot(request):
    popular_questions = Question.objects.popular_questions()
    content = paginate(popular_questions, request, 5)
    context = {
        'contents': content,
        'new_questions': content,
        'next': 'hot'
    }
    return render(request, "hot.html", context=context)

def profile(request):
    profile_id = request.GET.get('id')
    profiles = Profile.objects.all()
    user = profiles[0].user
    for profile in profiles:
        user = profile.user
        print('id: {}'.format(user.id))
        if user.id == int(profile_id):
            break
        
    if (profile):
        print(user.get_email_field_name())
        print(user.get_username())
        context = {
            'email': user.get_email_field_name(),
            'username': user.get_username(),
            'next': 'profile',
            'id': profile_id,
            'user': user
        }
        return render(request, "profile.html", context=context)

@login_required(login_url='login')
@require_POST
def question_vote(request):
    question_id = request.POST['id']
    question = Question.objects.get(question_id=question_id)
    like_up = (request.POST['up'] == "yes")
    like_value = 0
    if like_up:
        like_value = 1
    else:
        like_value = -1
    new_like = LikeQuestion(
        user=Profile.objects.get(user=request.user),
        value=like_value,
        related_question=question,
    )
    question.carma += like_value
    new_like.save()
    question.save()
    return JsonResponse({'carma': question.carma})

@login_required(login_url='login')
@require_POST
def answer_vote(request):
    answer_id = request.POST['id']
    answer = Answer.objects.get(id=answer_id)
    like_up = (request.POST['up'] == "yes")
    like_value = 0
    if like_up:
        like_value = 1
    else:
        like_value = -1
    new_like = LikeAnswer.objects.get(related_answer=answer, user=Profile.objects.get(user=request.user))
    new_like = LikeAnswer(
        user=Profile.objects.get(user=request.user),
        value=like_value,
        related_answer=answer,
    )
    answer.carma += like_value
    new_like.save()
    answer.save()
    return JsonResponse({'carma': answer.carma})