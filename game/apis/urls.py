from django.urls import path
from .views import create, get

urlpatterns = [
    path('room/create/', create.CreateRoom.as_view(),name='create_room'),
    path('room/get/<int:room_number>', get.GetRoom.as_view(),name='get_room'),
    path('question/create/<int:room_number>', create.CreateQuestion.as_view(),name='create_question'),
]