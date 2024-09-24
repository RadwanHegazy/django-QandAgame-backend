from channels.generic.websocket import WebsocketConsumer
from game.models import Room, Question
from asgiref.sync import async_to_sync
import json, random


class RoomConsumer (WebsocketConsumer) : 

    def close_room (self) : 
        data = {
            'type' : 'close',
        }

        async_to_sync(self.channel_layer.group_send)(
            self.GROUP,
            {
                'type' : 'sendq',
                'data' : {**data}
            }
        )

        self.room.delete()
        return

    def generate_and_send_random_question(self) :
        # pick up random question in the room
    
        question = Question.objects.filter(
            room=self.room
        ).order_by("?").first()
    
        if question == None:
            self.close_room()
            return
    

        users = []
        for i in self.room.users.all() : 
            if i != question.user:
                users.append(i)

        random_user = random.choice(users)
        
        data = {
            'type' : 'question',
            'question' : question.text,
            'user' : random_user.full_name,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.GROUP,
            {
                'type' : 'sendq',
                'data' : {**data}
            }
        )
        question.delete()

    def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            self.close()
            return
        room_number = self.scope['url_route']['kwargs']['room_number']
        try :
            self.room = Room.objects.get(number=room_number)
        except Room.DoesNotExist:
            self.close()
            return
        
        if self.user not in self.room.users.all() : 
            self.close()
            return
        
        self.accept()
        self.GROUP = f"room_{self.room.number}"

        async_to_sync(self.channel_layer.group_add)(
            self.GROUP,
            self.channel_name,
        )

        self.generate_and_send_random_question()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        recived_data = json.loads(text_data)
        try : 
            if recived_data['next'] == True:
                self.generate_and_send_random_question()
        except Exception as error:
            print(error)
            self.close()
            return
        
        print("Recived : ", recived_data)


    def sendq (self, data) : 
        self.send(text_data=json.dumps(data['data']))