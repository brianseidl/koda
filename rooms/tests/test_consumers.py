from django.test import TestCase
from rooms.consumers import ChatConsumer
from rooms.models import Message, Room
from django.contrib.auth.models import User
from freezegun import freeze_time


class TestConsumers(TestCase):
    """
    So I haven't figured out how to write unit test for WebsocketConsumer
    classes, so most of the test cases here will be manual testing and
    documented. Here will consist the utility functions in consumers.py.
    """
    def setUp(self):
        self.consumer = ChatConsumer(scope="ligma")

    def test__clean_html(self):
        mean_message = "<script>window.location='https://discordapp.com';</script>"
        big_message = "<big>BIG MESSAGE</big>"

        self.assertEqual(self.consumer._clean_html(mean_message), "window.location='https://discordapp.com';")
        self.assertEqual(self.consumer._clean_html(big_message), "BIG MESSAGE")

    @freeze_time("2019-05-13")
    def test_messages_to_json(self):
        """ Test messages_to_json """
        user = User.objects.create(username="test_user")
        room = Room.objects.create(name="test_room")

        message_list = [
            Message.objects.create(author=user, room=room, content="foo"),
            Message.objects.create(author=user, room=room, content="bar"),
            Message.objects.create(author=user, room=room, content="idk"),
        ]

        expected_list = [
            {'author': 'test_user', 'content': 'idk', 'timestamp': 'Sunday May 12, 2019 at 8:00 PM'},
            {'author': 'test_user', 'content': 'bar', 'timestamp': 'Sunday May 12, 2019 at 8:00 PM'},
            {'author': 'test_user', 'content': 'foo', 'timestamp': 'Sunday May 12, 2019 at 8:00 PM'},
        ]

        self.assertEqual(self.consumer._messages_to_json(message_list), expected_list)

    @freeze_time("2019-05-13")
    def test_message_to_json(self):
        """ Test message_to_json """
        user = User.objects.create(username="test_user")
        room = Room.objects.create(name="test_room")

        message = Message.objects.create(author=user, room=room, content="foo")

        expected = {'author': 'test_user', 'content': 'foo', 'timestamp': 'Sunday May 12, 2019 at 8:00 PM'}

        self.assertEqual(self.consumer._message_to_json(message), expected)
