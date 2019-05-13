from django.test import TestCase
from django.contrib.auth.models import User
from rooms.models import Message, Room, RoomUser
from datetime import datetime, timedelta

class TestRoom(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="test_room")
        self.user_1 = User.objects.create(username="test_user_1")
        self.user_2 = User.objects.create(username="test_user_2")
        self.room.add_user(self.user_1)
        self.room.add_user(self.user_2)

    def test_add_user(self):
        new_user = User.objects.create(username="test_user_3")
        self.room.add_user(new_user)

        self.assertTrue(new_user in self.room.members)

    def test_get_members(self):
        """ Tests for shit and what not """
        test_room = Room.objects.get(name="test_room")
        self.assertEqual(test_room, self.room)

        self.assertTrue(test_room.members, [self.user_1, self.user_2])

    def test_load_messages(self):
        """ Test that all messages are loaded in the correct order """
        now = datetime.now()
        later = now + timedelta(minutes=10)

        message1 = Message.objects.create(author=self.user_1, room=self.room, content="foo", timestamp=now)
        message2 = Message.objects.create(author=self.user_2, room=self.room, content="bar", timestamp=later)

        # messages are loaded in reverse timestamp order
        self.assertEqual(list(self.room.load_messages()), [message2, message1])

    def test_who_is_online(self):
        """ Test who_is_online """
        self.assertEqual(self.room.who_is_online(), ([], [self.user_1, self.user_2]))

    def test__str__(self):
        """ test __str__ """
        self.assertEqual(str(self.room), "test_room")


class TestMessage(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="test_room")
        self.user = User.objects.create(username="test_user")
        self.room.add_user(self.user)
        self.message = Message.objects.create(author=self.user, room=self.room, content="foo")

    def test__str__(self):
        """ test __str__ """
        self.assertEqual(str(self.message), "test_user: foo")


class TestRoomUser(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="test_room")
        self.user = User.objects.create(username="test_user")
        self.room.add_user(self.user)
        self.message = Message.objects.create(author=self.user, room=self.room, content="foo")

    def test__str__(self):
        """ test __str__ """
        room_user = RoomUser.objects.get(id=1)
        self.assertEqual(str(room_user), "test_user-test_room")
