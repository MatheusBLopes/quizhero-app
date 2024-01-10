import csv
import json
from urllib.parse import parse_qs

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import Question, QuestionAlternative, Quiz, QuizFolder


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
    folders_with_quizzes = QuizFolder.objects.filter(quizzes__user=request.user).prefetch_related('quizzes')

    return render(request, 'quizzes/pages/home.html', context={
        'folders_with_quizzes': folders_with_quizzes,
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


@login_required
def create_quiz_with_json(request):
    if request.method == 'GET':
        return render(request, 'quizzes/pages/create-json-quiz.html')
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = parse_qs(body_unicode)
        
        quiz_json = body.get('quiz_json')
        if not quiz_json:
            messages.error(request, 'Missing quiz_json parameter')
            return render(request, 'quizzes/pages/create-json-quiz.html')
        
        try:
            quiz_data = json.loads(quiz_json[0])
            quiz_name = quiz_data['name']
            quiz_description = quiz_data['description']
            questions_data = quiz_data['questions']
        except (KeyError, json.JSONDecodeError):
            messages.error(request, 'Invalid JSON payload')
            return render(request, 'quizzes/pages/create-json-quiz.html')
        
        # Create the quiz
        quiz = Quiz.objects.create(name=quiz_name, description=quiz_description, user=request.user)
        
        # Create the questions and alternatives
        for question_data in questions_data:
            question_description = question_data['description']
            alternatives_data = question_data['alternatives']
            
            question = Question.objects.create(description=question_description, quiz=quiz)
            
            for alternative_data in alternatives_data:
                alternative_description = alternative_data['description']
                is_correct = alternative_data['is_correct']
                
                QuestionAlternative.objects.create(description=alternative_description, is_correct=is_correct, question=question)
        
        messages.success(request, 'Quiz created successfully')
        return render(request, 'quizzes/pages/create-json-quiz.html')
    else:
        return HttpResponseBadRequest('Invalid request method')
