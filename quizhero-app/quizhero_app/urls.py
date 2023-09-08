from django.urls import include, path

urlpatterns = [
    path('', include("apps.quizzes.urls")),
]
