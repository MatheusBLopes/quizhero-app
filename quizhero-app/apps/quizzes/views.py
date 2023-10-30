from django.shortcuts import render, get_object_or_404
from utils.factory import make_quiz
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question
from django.core import serializers
import csv
from django.http import HttpResponseBadRequest, HttpResponse


import json

@login_required
def home(request):
    return render(request, 'quizzes/pages/home.html', context={
        'quizzes': [make_quiz() for _ in range(10)],
    })

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
def quiz(request, id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('question_set__questionalternative_set'), id=id)
    quiz_json = serialize_quiz(quiz)

    context = {
        'quiz_json': quiz_json,
        'quiz_name': quiz.name
    }
    return render(request, 'quizzes/pages/quiz-view.html', context=context)



# @login_required
def upload_quiz_csv(request):
    if request.method == 'GET':
        return render(request, 'quizzes/pages/csv-upload.html')
    if request.method == 'POST':
        if 'quiz_csv' not in request.FILES:
            return HttpResponseBadRequest('No file uploaded')

        quiz_csv = request.FILES['quiz_csv']
        reader = csv.reader(quiz_csv)

        num_quizzes = 0
        num_questions = 0
        num_alternatives = 0

        for row in reader:
            quiz_name, quiz_description, question_description, alternative_description, is_correct = row

            quiz = Quiz.objects.create(name=quiz_name, description=quiz_description)
            num_quizzes += 1

            question = Question.objects.create(description=question_description, quiz=quiz)
            num_questions += 1

            alternative = QuestionAlternative.objects.create(description=alternative_description, is_correct=is_correct, question=question)
            num_alternatives += 1

        message = f'Created {num_quizzes} quizzes, {num_questions} questions, and {num_alternatives} alternatives'
        return HttpResponse(message)

    return HttpResponseBadRequest('Invalid request method')


class MyLoginView(LoginView):
    template_name = 'quizzes/pages/login.html'
