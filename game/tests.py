from django.test import TestCase
from django.urls import reverse
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken
from game.models import Room, Question

class TestGameApp (TestCase) : 

    def create_user(self) : 
        user = User.objects.create_user(
            email='test@gmail.com',
            password='123',
            full_name='test User'
        )
        return user

    def create_headers(self, user) : 
        return {'Authorization' : f"Bearer {AccessToken.for_user(user)}"}
    
    def setUp(self) -> None:
        self.create_game_endpoint = reverse('create_room')

    def test_create_game_endpoint_invalid(self) : 
        response = self.client.post(
            self.create_game_endpoint
        )

        self.assertNotEqual(response.status_code, 200)

    def test_create_game_endpoint_valid(self) : 
        user = self.create_user()
        response = self.client.post(
            self.create_game_endpoint,
            headers=self.create_headers(user)
        )
        
        self.assertEqual(type(response.json()['room_number']), int)
        self.assertEqual(response.status_code, 201)

    def test_get_room_unauthorized_user (self) : 
        user = self.create_user()
        response = self.client.get(
            reverse('get_room',args=[1]),
        )
        
        self.assertNotEqual(response.status_code, 200)
    
    def test_get_undefined_room (self) : 
        user = self.create_user()
        response = self.client.get(
            reverse('get_room',args=[1]),
            headers=self.create_headers(user)
        )
        
        self.assertNotEqual(response.status_code, 200)
    
    def test_get_room_success (self) :
        user = self.create_user()
        room = Room.objects.create(
            owner=user,
            number=123
        )
        room.users.add(user)
        room.save()

        response = self.client.get(
            reverse('get_room',args=[123]),
            headers=self.create_headers(user)
        )
        
        self.assertEqual(response.status_code, 200)
    
    def test_create_q_unauthorized_user (self):
        response = self.client.post(
            reverse('create_question', args=[1])
        )
        self.assertNotEqual(response.status_code, 200)
    
    def test_create_q_undefined_room (self):
        response = self.client.post(
            reverse('create_question', args=[1]),
            headers=self.create_headers(self.create_user())
        )
        self.assertNotEqual(response.status_code, 200)
    
    def test_create_q_success (self) :
        user = self.create_user()
        headers = self.create_headers(user)
        room = Room.objects.create(
            owner=user,
            number=1,
        )
        room.users.add(user)
        room.save()
        response = self.client.post(
            reverse('create_question', args=[1]),
            headers=headers,
            data={
                'text' : "test text"
            }
        )

        self.assertEqual(response.status_code, 201)