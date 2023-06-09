from django.urls import path
from tutorial import views

urlpatterns = [
    path('tutorials/', views.TutorialList.as_view()),
]