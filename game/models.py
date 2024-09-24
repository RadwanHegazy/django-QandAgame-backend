from django.db import models
from users.models import User
from random import randrange

class Room (models.Model) :
    number = models.PositiveIntegerField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='room_users')
    owner = models.ForeignKey(User, related_name='user_owner', on_delete=models.CASCADE)

    def generate_and_set_number(self) :
        num = ""
        for i in range(0,7):
            num += str(randrange(0,9))
        num = int(num)
        self.number = num
        return num 

class Question (models.Model) : 
    user = models.ForeignKey(User, related_name='user_q', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room_q', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self) -> str:
        return str(self.room.number) + " | " + self.user.full_name