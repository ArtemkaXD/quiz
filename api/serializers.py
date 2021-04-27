from rest_framework import serializers
from .models import Quiz, Question, OfferedAnswer, User, Answer, Reply


class QuizSerializer(serializers.ModelSerializer):
    '''Сериализатор опросов'''
    class Meta:
        model = Quiz
        fields = '__all__'

    def validate(self, data):
        '''Проверка даты опроса'''
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must occur after start date")
        return data

    def update(self, instance, validated_data):
        '''Исключения поля начала опроса при обновлении опроса'''
        validated_data.pop('start_date')
        return super().update(instance, validated_data)


class OfferedAnswerSerializer(serializers.ModelSerializer):
    '''Сериализатор готовых ответов'''
    class Meta:
        model = OfferedAnswer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    '''Сериализатор вопросов опроса'''
    offered_answers = OfferedAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        '''Создание списка вопросов со списком готовых ответов'''
        offered_answers_data = validated_data.pop('offered_answers')
        question = Question.objects.create(**validated_data)
        for offered_answer_data in offered_answers_data:
            answer, create = OfferedAnswer.objects.get_or_create(**offered_answer_data)
            question.offered_answers.add(answer)
        return question

    def update(self, instance, validated_data):
        '''Измение списка вопросов со списком готовых ответов'''
        offered_answers_data = validated_data.pop('offered_answers')
        instance.type = validated_data['type']
        instance.text = validated_data['text']
        offered_answers = list(instance.offered_answers.all())
        instance.offered_answers.clear()
        instance.save()

        for offered_answer_data in offered_answers_data:
            answer, create = OfferedAnswer.objects.get_or_create(**offered_answer_data)
            instance.offered_answers.add(answer)
        for offered_answer in offered_answers:
            if not offered_answer.question.count():
                offered_answer.delete()
        return instance

    def validate(self, data):
        '''Провервка типа вопроса'''
        if data['type'] == 'T' and data['offered_answers']:
            raise serializers.ValidationError("Wrong question type, set One or Multiply Choice")
        elif data['type'] != 'T' and not data['offered_answers']:
            raise serializers.ValidationError("Wrong question type, set Text Answer")
        return data


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор пользователя'''
    class Meta:
        model = User
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    '''Сериализатор ответа'''
    class Meta:
        model = Answer
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    '''Сериализатор ответа на опрос'''
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        '''Создание отвтета на опрос'''
        answers_data = validated_data.pop('answers')
        reply = Reply.objects.create(**validated_data)
        for answer_data in answers_data:
            answer = Answer.objects.create(**answer_data)
            reply.answers.add(answer)
        return reply

    def validate(self, data):
        '''Проверка на соответсвие вопроса опросу и проверка на уникальность ответа на опрос'''
        for answer in data['answers']:
            if answer['question_id'].quiz != data['quiz']:
                raise serializers.ValidationError("Wrong question id")
        try:
            Reply.objects.get(quiz=data['quiz'], user=data['user'])
        except Reply.DoesNotExist:
            return data
        raise serializers.ValidationError("User can post only one reply for the quiz")


class ReplyListSerializer(serializers.ModelSerializer):
    '''Сериализатор детализации отвтетов по респонденту'''
    answers = serializers.StringRelatedField(many=True)
    quiz = serializers.StringRelatedField()

    class Meta:
        model = Reply
        fields = '__all__'