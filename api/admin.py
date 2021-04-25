from django.contrib import admin
from .models import Question, Answer, Quiz, Reply, User

admin.site.register((Question, Answer, Quiz, Reply, User))

# Register your models here.
