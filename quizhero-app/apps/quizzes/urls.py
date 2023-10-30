from django.urls import path
from . import views


app_name = "quizzes"
urlpatterns = [
    path("", views.home, name="home"),
    path('quiz/<int:id>/', views.quiz, name="quiz"),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('create-quiz/', views.upload_quiz_csv, name='create-quiz'),
]