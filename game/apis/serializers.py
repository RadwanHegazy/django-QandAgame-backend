from rest_framework import serializers
from ..models import Question, Room
from users.models import User

class RoomUserSerializer (serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = ['full_name','email','picture']

class GetRoomSerializer (serializers.ModelSerializer) : 
    users = RoomUserSerializer(many=True)
    owner = RoomUserSerializer()

    class Meta:
        model = Room
        fields = ['number','users','owner']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_questions'] = Question.objects.filter(room=instance).count()
        user = self.context.get('user')
        data['me_questions'] = Question.objects.filter(room=instance, user=user).count()
        return data
    
class RoomSerializer (serializers.Serializer) :

    def validate(self, attrs):
        return {}

    def create (self, validated_data=None) : 

        user = self.context.get('user')
        self.model = Room.objects.create(
            owner=user
        )
        self.model.users.add(user)
        self.model.generate_and_set_number()
        self.model.save()

        return self.model
    
    
    def to_representation(self, *args):
        return {
            'room_number' : self.model.number
        }
    

class CreateQuestionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text']
    
    def validate(self, attrs):
        attrs['user'] = self.context.get('user')
        attrs['room'] = self.context.get('room')
    
        return attrs