from django.contrib import admin
from .models import Question, Room

@admin.register(Room)
class RoomPanel (admin.ModelAdmin) : 
    list_display = ['number','owner']

@admin.register(Question)
class QuestionPanel (admin.ModelAdmin) : 
    list_display = ['user','room']
