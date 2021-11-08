from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Question, Answer, Tag, Like

# questions = [
#     {
#         "title": f"Title {i}",
#         "text": f"This is text for {i} question"
#     } for i in range (100)
# ]

# answers = [
#     {
#         "title": f"Answer title {i}",
#         "text": f"This is answer. Let me answer question #{i}"
#     } for i in range (50)
# ]

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
        'new_questions': content
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
        'answers': content
    }
    return render(request, "question.html", context=context)

def ask(request):
    return render(request, "ask.html", {})

def login(request):
    return render(request, "login.html", {})

def register(request):
    return render(request, "register.html", {})

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
        'contents': content
    }
    return render(request, "tagged_questions.html", context=context)

def hot(request):
    popular_questions = Question.objects.popular_questions()
    content = paginate(popular_questions, request, 5)
    context = {
        'contents': content,
        'new_questions': content
    }
    return render(request, "hot.html", context=context)

def profile(request):
    return render(request, "profile.html", {})