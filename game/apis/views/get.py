from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ..serializers import GetRoomSerializer, Room


class GetRoom (APIView) :
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_number) :
        try : 
            room = Room.objects.get(number=room_number)
        except Room.DoesNotExist:
            return Response({
                'message' : 'room not found'
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user not in room.users.all() : 
            room.users.add(user)
            room.save()

        serializer = GetRoomSerializer(room, context={'user':user})
        return Response(serializer.data, status=status.HTTP_200_OK)


