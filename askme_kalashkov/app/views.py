from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import auth
from django.urls import reverse
from .models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from .forms import LoginForm, SingUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

def question(request):
    question_id=request.GET.get('id')
    question = Question.objects.get(id=question_id)
    answers=question.answers.all()
    content = paginate(answers, request,5)
    context = {
        'question': question,
        'contents':content,
        'answers': content,
        'next': 'question',
        'id': question_id
    }
    return render(request, "question.html", context=context)

@login_required(login_url='login')
def ask(request):
    # if request.method == 'POST':
    #     q_form = QuestionForm(data=request.POST)
    #     if q_form.is_valid():
    #         q = Question(**q_form.cleaned_data)
    #         q = Question.save()
    return render(request, "ask.html", {})


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
    return render(request, "settings.html", {})

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
            'id': profile_id
        }
        return render(request, "profile.html", context=context)
