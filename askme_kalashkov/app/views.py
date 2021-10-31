from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.

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

def index(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page) 
    return render(request, "index.html", {'questions': content})

def question(request):
    paginator = Paginator(answers, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "question.html", {'answers': content})

def ask(request):
    return render(request, "ask.html", {})

def login(request):
    return render(request, "login.html", {})

def register(request):
    return render(request, "register.html", {})

def settings(request):
    return render(request, "settings.html", {})

def tagged(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "tagged_questions.html", {'questions': content})

def hot(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page) 
    return render(request, "hot.html", {'questions': content})