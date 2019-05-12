from django.test import TestCase
from django.contrib.auth.models import User
from rooms.models import Message, Room, RoomUser

class TestRoom(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="test_room")
        self.user_1 = User.objects.create(username="test_user_1")
        self.user_2 = User.objects.create(username="test_user_2")
        # add users to room
        self.room.add_user(self.user_1)
        self.room.add_user(self.user_2)
        self.messages = [
            Message.objects.create(author=self.user_1, room=self.room, content="foo"),
            Message.objects.create(author=self.user_2, room=self.room, content="bar"),
        ]

    def test_add_user(self):
        #new_user = User.objects.
        self.assertTrue(True)

    def test_get_members(self):
        """ Tests for shit and what not """
        test_room = Room.objects.get(name="test_room")
        self.assertEqual(test_room, self.room)

        test_room_members = test_room.members
        self.assertTrue(test_room_members, [self.user_1, self.user_2])