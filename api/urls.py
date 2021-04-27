from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuizQuestionView, QuizViewSet, ActiveQuizList, ActiveQuizQuestion, ReplyQuiz, NewUser, UserReply

urlpatterns = [
    path('quizzes/<int:pk>/questions/<int:q_pk>/', QuizQuestionView.as_view()),
    path('quizzes/<int:pk>/questions/', QuizQuestionView.as_view()),
    path('quizzes/active/', ActiveQuizList.as_view()),
    path('quizzes/active/<int:pk>/questions/', ActiveQuizQuestion.as_view()),
    path('newuser/', NewUser.as_view()),
    path('quizzes/active/<int:pk>/reply/<int:u_pk>/', ReplyQuiz.as_view()),
    path('quizzes/user/<int:pk>/replys/', UserReply.as_view()),
]

router = DefaultRouter()
router.register('quizzes', QuizViewSet)

urlpatterns += router.urls