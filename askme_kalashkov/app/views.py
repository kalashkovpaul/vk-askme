from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Question, Answer, Tag, Like

questions = [
    {
        "title": f"Title {i}",
        "text": f"This is text for {i} question"
    } for i in range (100)
]

answers = [
    {
        "title": f"Answer title {i}",
        "text": f"This is answer. Let me answer question #{i}"
    } for i in range (50)
]

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number=request.GET.get('page')
    content=paginator.get_page(page_number)
    return content

def index(request):
    # num_questions = Question.objects.all().count()
    new_questions = Question.objects.filter(date__lt=timezone.now()).order_by("-date")
    content = paginate(new_questions, request, 5)
    context = {
        'contents': content,
        'questions': new_questions
    }
    return render(request, "index.html", context=context)

def question(request):
    page = paginate(answers, request,5)
    return render(request, "question.html", page)

def ask(request):
    return render(request, "ask.html", {})

def login(request):
    return render(request, "login.html", {})

def register(request):
    return render(request, "register.html", {})

def settings(request):
    return render(request, "settings.html", {})

def tagged(request):
    page = paginate(questions, request, 5)
    return render(request, "tagged_questions.html", page)

def hot(request):
    page = paginate(questions, request, 5) 
    return render(request, "hot.html", page)

def profile(request):
    return render(request, "profile.html", {})