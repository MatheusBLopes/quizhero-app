import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers

from .models import Question, QuestionAlternative, Quiz, QuizFolder

class QuestionAlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAlternative
        fields = ['id', 'description', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    alternatives = QuestionAlternativeSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'description', 'alternatives']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['alternatives'] = QuestionAlternativeSerializer(instance.questionalternative_set.all(), many=True).data
        return representation

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'questions']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['questions'] = QuestionSerializer(instance.question_set.all(), many=True).data
        return representation

@login_required
def home(request):
    folders_with_quizzes = QuizFolder.objects.filter(quizzes__user=request.user).distinct().prefetch_related('quizzes')
    return render(request, 'quizzes/pages/home.html', context={'folders_with_quizzes': folders_with_quizzes})

@login_required
def quiz(request, id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('question_set__questionalternative_set'), id=id)
    quiz_serializer = QuizSerializer(quiz)
    return render(request, 'quizzes/pages/quiz-view.html', context={'quiz_json': json.dumps(quiz_serializer.data), 'quiz_name': quiz.name})

class MyLoginView(LoginView):
    template_name = 'quizzes/pages/login.html'

@login_required
def create_quiz_with_json(request):
    if request.method == 'GET':
        return render(request, 'quizzes/pages/create-json-quiz.html')
    elif request.method == 'POST':
        quiz_json = request.POST.get('quiz_json')
        if not quiz_json:
            messages.error(request, 'Missing quiz_json parameter')
            return render(request, 'quizzes/pages/create-json-quiz.html')

        try:
            quiz_data = json.loads(quiz_json)
            quiz_serializer = QuizSerializer(data=quiz_data)
            quiz_serializer.is_valid(raise_exception=True)
            quiz_serializer.save(user=request.user)
        except (KeyError, json.JSONDecodeError, serializers.ValidationError):
            messages.error(request, 'Invalid JSON payload')
            return render(request, 'quizzes/pages/create-json-quiz.html')

        messages.success(request, 'Quiz created successfully')
        return render(request, 'quizzes/pages/create-json-quiz.html')
    else:
        return HttpResponseBadRequest('Invalid request method')
