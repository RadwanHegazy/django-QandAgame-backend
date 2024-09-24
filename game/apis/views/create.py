from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import RoomSerializer, CreateQuestionSerializer, Room
from rest_framework.permissions import IsAuthenticated

class CreateRoom (CreateAPIView) : 
    """
     Create room by incoming user request as a owner.
    """
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context (self, *args, **kwargs) : 
        return {
            'user' : self.request.user
        }
    
class CreateQuestion (APIView) : 
    """
     Create question by user
    """
    serializer_class = CreateQuestionSerializer
    permission_classes = [IsAuthenticated]

    
    def post(self, request, room_number) : 
        user = request.user

        try :
            room = Room.objects.get(number=room_number)
            if user not in room.users.all() : raise Exception("")
        except Room.DoesNotExist or Exception:
            return Response({
                'message' : 'room not found'
            }, status=status.HTTP_404_NOT_FOUND)


        serializer = self.serializer_class(data=request.data, context={
            'user' : user,
            'room' : room
        })

        if serializer.is_valid() : 
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
