from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "quizzes"
urlpatterns = [
    path("", views.home, name="home"),
    path('quiz/<int:id>/', views.quiz, name="quiz"),
    path('create-json-quiz/', views.create_quiz_with_json, name='create-json-quiz'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]