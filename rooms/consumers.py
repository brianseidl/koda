from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Room
import re
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        """
        User connected to a room and websocket, load all previous
        messages and sent it to just the user who connected.

        Precondition:
            User loads page

        Postcondition:
            User gets sent all previous messages from the room

        Paremeters:
            data (dict): data sent from client

        Returns:
            None
        """
        room_name = data['room_name']
        room = Room.objects.filter(name=room_name)[0]
        messages = room.load_messages()
        content = {
            'command': 'messages',
            'messages': self._messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        """
        User sends a message to the room.  Save the message to
        the database and send contents of the message to all users
        connected in the room.

        Precondition:
            A message is sent from the client to the server.

        Postcondition:
            The message is saved to the database and sent to
            all users connected on the server.

        Parameters:
            data (dict): data send from client

        Returns:
            None
        """
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        room_name = data['room_name']
        room = Room.objects.filter(name=room_name)[0]
        message = Message.objects.create(
            author=author_user,
            content=self._clean_html(data['message']),
            room=room)
        content = {
            'command': 'new_message',
            'message': self._message_to_json(message)
        }
        self.send_chat_message(content)

    def typing(self, data):
        """
        User is pressing keys.  We want to notify all users
        currently connected to the room that the user is typing

        Precondition:
            User starts typing

        Postcondition:
            Other users are notified that said user is typing.

        Parameters:
            data (dict): data being send from client

        Returns:
            None
        """
        content = {
            'command': 'typing',
            'username': data["from"]
        }
        self.send_chat_message(content)

    def _clean_html(self, raw_html):
        """
        Helpoer function to remove any xss attack attempt

        Parameters:
            raw_html (str): string in which you want html removed

        Returns:
            str: string with removed html tags

        Shout out to Scott Shannon to figure out how to send photos
        before we built the functionality to send phtotos lol.
        """
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def _messages_to_json(self, messages):
        """
        Helper method to convert a group of messages to json

        Parameters:
            messages (list): list of Message objects to be converted to json/dict

        Returns:
            list: list of message objects in json form
        """
        return [self._message_to_json(message) for message in messages][::-1]

    def _message_to_json(self, message):
        """
        Helper function to convert a single message to json

        Parameters:
            message (Message): Message object to be converted to json/dict

        Returns:
            dict: message in json form
        """
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': timezone.localtime(message.timestamp).strftime("%A %B %-d, %Y at %-I:%M %p"),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'typing': typing,
    }

    def connect(self):
        """
        DO NOT TOUCH!
        """
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """
        DO NOT TOUCH!
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """
        DO NOT TOUCH!
        """
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        """
        Send message to everyone currently connected to the room

        Preconditions:
            None

        Postconditions:
            Message sent to everyone connected to room

        Parameters:
            message (dict): message in json form

        Returns:
            None
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        """
        Send message to just single user

        Preconditions:
            None

        Postconditions:
            Message sent to user.

        Parameters:
            message (dict): message to be sent to user

        Returns:
            None
        """
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        """
        DO NOT TOUCH!
        """
        message = event['message']
        self.send(text_data=json.dumps(message))
