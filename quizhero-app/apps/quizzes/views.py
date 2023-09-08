from django.shortcuts import render
from utils.factory import make_quiz
import json


def home(request):
    return render(request, 'quizzes/pages/home.html', context={
        'quizzes': [make_quiz() for _ in range(10)],
    })

def quiz(request, id):
    return render(request, 'quizzes/pages/quiz-view.html', context={
        'quiz': make_quiz(),
    })