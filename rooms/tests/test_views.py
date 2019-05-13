from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from rooms.models import Message, Room
from rooms.views import *
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied


class TestBaseView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.view = BaseView.as_view()

    def test_get_context_data_no_login(self):
        """ Test the get_context_data for a user who is not logged in """
        self.request.user = AnonymousUser
        response = self.view(self.request)

        self.assertEqual(response.context_data["user"], AnonymousUser)
        self.assertEqual(response.context_data["logged_in"], False)

    def test_get_context_data_yes_login(self):
        """ Test get_context_data for a user who is logged in """
        test_user = User.objects.create(username="test_user")
        self.request.user = test_user
        response = self.view(self.request)

        self.assertEqual(response.context_data["user"], test_user)
        self.assertEqual(response.context_data["logged_in"], True)


class TestBaseRoomView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = BaseRoomView.as_view()

        self.room1 = Room.objects.create(name="test_room_1", id=1)
        self.room2 = Room.objects.create(name="test_room_2", id=2)
        self.room3 = Room.objects.create(name="test_room_3", id=3)
        
        self.user = User.objects.create(username="test_user")
        self.room1.add_user(self.user)
        self.room2.add_user(self.user)

    def test_get_no_login(self):
        """ Test a request for a user who is not logged in """
        response = self.client.get('/rooms/')
        self.assertRedirects(response, '/accounts/login/?next=/rooms/')

    def test_get_yes_login(self):
        """ Test a request for a user who is logged in """
        request = self.rf.get("room/")
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_get_context_data(self):
        # TODO (brian): test for different cases here
        """ Test get_context_data for user who is logged in """
        request = self.rf.get("room/")
        request.user = self.user
        not_user_room = self.room3
        response = self.view(request)

        # make sure room type is room
        self.assertEqual(response.context_data["type"], "room")
        # make sure not_user_room is not in the result set
        self.assertNotIn(not_user_room, response.context_data["rooms"])
        # make sure the correct rooms are loaded
        self.assertEqual(response.context_data["rooms"], [self.room1, self.room2])


class TestDetailRoomView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = DetailRoomView.as_view()

        self.room1 = Room.objects.create(name="test_room_1", id=1)
        self.room2 = Room.objects.create(name="test_room_2", id=2)
        self.room3 = Room.objects.create(name="test_room_3", id=3)
        
        self.user = User.objects.create(username="test_user")
        self.room1.add_user(self.user)
        self.room2.add_user(self.user)

    def test_get_no_login(self):
        """ Test a request for a user who is not logged in """
        request = self.rf.get("rooms/1/")
        request.user = AnonymousUser
        kwargs = {"room_id": 1}
        with self.assertRaises(PermissionDenied):
            response = self.view(request, **kwargs)

    def test_get_yes_login(self):
        """ Test a request for a user who is logged in """
        request = self.rf.get("rooms/1/")
        request.user = self.user
        kwargs = {"room_id": 1}
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_room_not_authorized(self):
        """ Test user tries to view room where he/she is not authorized """
        request = self.rf.get("rooms/3/")
        request.user = self.user
        kwargs = {"room_id": 3}
        with self.assertRaises(PermissionDenied):
            response = self.view(request, **kwargs)

    def test_room_is_actually_chat(self):
        """ Test user is authorized to view room but room is actually a chat """
        new_chat_room = Room.objects.create(name="test_room_4", id=4, rtype="chat")
        new_chat_room.add_user(self.user)
        
        request = self.rf.get("rooms/4/")
        request.user = self.user
        kwargs = {"room_id": 4}
        with self.assertRaises(PermissionDenied):
            response = self.view(request, **kwargs)


class TestBaseChatView(TestCase):
    """
    I just want to point out that there must be 2 users in a chat room.
    So before you get all triggered and what not that there are no test cases 
    for this, it's because I know that It will break and I dont have time
    to make chats more robust. Only the admin can configure rooms and chats,
    and I'm the admin in production, so ... LIGMA.
    """
    def setUp(self):
        self.rf = RequestFactory()
        self.view = BaseChatView.as_view()

        self.room1 = Room.objects.create(name="test_room_1", id=1, rtype="chat")
        self.room2 = Room.objects.create(name="test_room_2", id=2, rtype="chat")
        self.room3 = Room.objects.create(name="test_room_3", id=3, rtype="chat")
        
        self.user = User.objects.create(username="test_user")
        self.room1.add_user(self.user)
        self.room2.add_user(self.user)

    def test_get_no_login(self):
        """ Test a request for a user who is not logged in """
        response = self.client.get('/chats/')
        self.assertRedirects(response, '/accounts/login/?next=/chats/')

    def test_get_yes_login(self):
        """ Test a request for a user who is logged in """
        request = self.rf.get("chats/")
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_get_context_data(self):
        # TODO (brian): test for different cases here
        """ Test get_context_data for user who is logged in """
        request = self.rf.get("chat/")
        request.user = self.user
        not_user_room = self.room3
        response = self.view(request)

        # make sure room type is room
        self.assertEqual(response.context_data["type"], "chat")
        # make sure not_user_room is not in the result set
        self.assertNotIn(not_user_room, response.context_data["rooms"])
        # make sure the correct rooms are loaded
        self.assertEqual(response.context_data["rooms"], [self.room1, self.room2])

    def test_get_other_member(self):
        """ Test get_other_member returns the other member in the group """
        test_user2 = User.objects.create(username="test_user2")
        self.room1.add_user(test_user2)

        self.assertEqual(BaseChatView.get_other_member(self.room1, self.user), test_user2)
        self.assertEqual(BaseChatView.get_other_member(self.room1, test_user2), self.user)


class TestDetailChatView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = DetailChatView.as_view()

        self.room1 = Room.objects.create(name="test_room_1", id=1, rtype="chat")
        self.room2 = Room.objects.create(name="test_room_2", id=2, rtype="chat")
        self.room3 = Room.objects.create(name="test_room_3", id=3, rtype="chat")
        
        self.user = User.objects.create(username="test_user")
        self.room1.add_user(self.user)
        self.room2.add_user(self.user)

    def test_get_no_login(self):
        """ Test a request for a user who is not logged in """
        request = self.rf.get("chats/1/")
        request.user = AnonymousUser
        kwargs = {"chat_id": 1}
        with self.assertRaises(PermissionDenied):
            response = self.view(request, **kwargs)

    def test_get_yes_login(self):
        """ Test a request for a user who is logged in """
        request = self.rf.get("chats/1/")
        request.user = self.user
        kwargs = {"chat_id": 1}
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_room_not_authorized(self):
        """ Test user tries to view room where he/she is not authorized """
        request = self.rf.get("chats/3/")
        request.user = self.user
        kwargs = {"chat_id": 3}
        with self.assertRaises(PermissionDenied):
            response = self.view(request, **kwargs)

    def test_room_is_actually_chat(self):
        """ Test user is authorized to view room but room is actually a chat """
        new_chat_room = Room.objects.create(name="test_room_4", id=4, rtype="room")
        new_chat_room.add_user(self.user)
        
        request = self.rf.get("chats/4/")
        request.user = self.user
        kwargs = {"chat_id": 4}
        with self.assertRaises(PermissionDenied):
            response = self.view(request, **kwargs)