from datetime import date

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.http import Http404
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Quiz, Question, Reply, User
from .serializers import QuizSerializer, QuestionSerializer, ReplySerializer, UserSerializer, \
    ReplyListSerializer


@receiver(pre_delete, sender=Question)
def pre_delete_question(sender, instance, **kwargs):
    '''Удаление готового ответа при отсутвии вопроса ссылающегося на него'''
    for offered_answer in instance.offered_answers.all():
        if offered_answer.question.count() == 1:
            offered_answer.delete()


class QuizViewSet(ModelViewSet):
    '''Контроллер администрирования опросов'''
    permission_classes = [permissions.IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizQuestionView(APIView):
    '''Контроллер администрирования вопросов опросов'''
    permission_classes = [permissions.IsAuthenticated]

    def get_questions(self, pk):
        '''Получение сета вопросов опроса по идентификатору'''
        try:
            return Question.objects.filter(quiz=pk)
        except Question.DoesNotExist:
            raise Http404

    def get_question(self, quiz, pk):
        '''Получение объекта вопроса опроса по идентификатору'''
        try:
            return Question.objects.get(quiz=quiz, pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, q_pk = None):
        '''Получение воросов опроса'''
        questions = self.get_questions(pk)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, pk, q_pk = None):
        '''Создание воросов опроса'''
        data = request.data.copy()
        for item in data:
            item.update({'quiz': pk})
        serializer = QuestionSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, q_pk = None):
        '''Изменение вопроса опроса по идентификатору'''
        question = self.get_question(pk, q_pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, q_pk = None):
        '''Удаление вороса опроса по идентификатору'''
        question = self.get_question(pk, q_pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActiveQuizList(APIView):
    '''Контроллер активных опросов'''
    def get_active_quiz(self):
        '''Получение сета активных опросов на текущую дату'''
        try:
            return Quiz.objects.filter(
                start_date__lte=date.today()).filter(
                end_date__gte=date.today()
            )
        except Question.DoesNotExist:
            raise Http404

    def get(self, request):
        '''Получение сета активных опросов на текущую дату'''
        quizzes = self.get_active_quiz()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class ActiveQuizQuestion(APIView):
    '''Контоллер вопросов активных опросов'''
    def get_active_questions(self, pk):
        '''Получение вопросов активных опросов на текущую дату'''
        try:
            active_quiz = Quiz.objects.filter(
                start_date__lte=date.today()).filter(
                end_date__gte=date.today()
            )
            return Question.objects.filter(quiz__in=active_quiz).filter(quiz=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''Получение вопросов активных опросов на текущую дату'''
        questions = self.get_active_questions(pk)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class ReplyQuiz(APIView):
    '''Контоллер ответа на опрос'''
    def post(self, request, pk, u_pk):
        '''Создание ответа на опрос'''
        data = request.data.copy()
        data.update({'quiz': pk, 'user': u_pk})
        serializer = ReplySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewUser(CreateAPIView):
    '''Контоллер создания респондента'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserReply(APIView):
    '''Контоллер детализации отвтетов по респонденту'''
    def get_replys(self, pk):
        '''Получение сета ответов на опрос по идентификатору респондента'''
        try:
            return Reply.objects.filter(user=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''Получение ответов на опрос по идентификатору респондента'''
        replys = self.get_replys(pk)
        serializer = ReplyListSerializer(replys, many=True)
        return Response(serializer.data)