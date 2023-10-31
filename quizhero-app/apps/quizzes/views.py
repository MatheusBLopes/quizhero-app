import csv
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from utils.factory import make_quiz

from .models import Question, Quiz, QuestionAlternative

def serialize_quiz(quiz):
    quiz_data = {
        'id': quiz.id,
        'name': quiz.name,
        'description': quiz.description,
        'questions': [],
    }
    
    questions = quiz.question_set.all()
    for question in questions:
        question_data = {
            'id': question.id,
            'description': question.description,
            'alternatives': [],
        }
        
        alternatives = question.questionalternative_set.all()
        for alternative in alternatives:
            alternative_data = {
                'id': alternative.id,
                'description': alternative.description,
                'is_correct': alternative.is_correct,
            }
            question_data['alternatives'].append(alternative_data)
        
        quiz_data['questions'].append(question_data)
    
    return json.dumps(quiz_data)

@login_required
def home(request):
    quizzes = Quiz.objects.filter(user=request.user)
    return render(request, 'quizzes/pages/home.html', context={
        'quizzes': quizzes,
    })


@login_required
def quiz(request, id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('question_set__questionalternative_set'), id=id)
    quiz_json = serialize_quiz(quiz)

    context = {
        'quiz_json': quiz_json,
        'quiz_name': quiz.name
    }
    return render(request, 'quizzes/pages/quiz-view.html', context=context)


class MyLoginView(LoginView):
    template_name = 'quizzes/pages/login.html'
