from django.urls import path
from django.contrib import admin
from . import views


app_name = "quizzes"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path('quizzes/<int:id>/', views.quiz, name="quiz")
]