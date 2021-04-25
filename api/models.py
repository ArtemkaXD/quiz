from django.db import models


class OfferedAnswer(models.Model):
    '''Модель готовых ответов'''
    offered_answer = models.CharField(max_length=256)

    def __str__(self):
        return self.offered_answer


class User(models.Model):
    '''Модель респондента'''
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    '''Модель опроса'''
    title = models.CharField(max_length=64)
    desc = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class Question(models.Model):
    '''Модель вопроса'''
    QTYPE_TEXT = 'T'
    QTYPE_CHOICE = 'C'
    QTYPE_MCHOICE = 'M'
    QTYPE_CHOICES = (
        (QTYPE_TEXT,'Text Answer'),
        (QTYPE_CHOICE,'One Choice'),
        (QTYPE_MCHOICE,'Multiply Choice'),
    )

    type = models.CharField(max_length=1, choices=QTYPE_CHOICES, default='T')
    text = models.TextField()
    offered_answers = models.ManyToManyField(OfferedAnswer, related_name='question', blank=True)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    '''Модель ответа опроса'''
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.question.text}: {self.answer}'


class Reply(models.Model):
    '''Модель ответа на опрос'''
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answers = models.ManyToManyField(Answer, blank=True)






