# chat/consumers.py
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Room
import re
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room_name = data['room_name']
        room = Room.objects.filter(name=room_name)[0]
        messages = room.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        room_name = data['room_name']
        room = Room.objects.filter(name=room_name)[0]
        message = Message.objects.create(
            author=author_user,
            content=self.cleanhtml(data['message']),
            room=room)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def typing(self, data):
        content = {
            'command': 'typing',
            'username': data["from"]
        }
        self.send_chat_message(content)

    def cleanhtml(self, raw_html):
        """ remove any xss attack attempt """
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages][::-1]

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': timezone.localtime(message.timestamp).strftime("%A %B %-d, %Y at %-I:%M %p"),
            'doWeAppendBoss': self.append_or_nah(message)
        }

    def append_or_nah(self, message):
        # TODO (brian): fix this, THEN push to prod
        return False
        """
        room = message.room
        try:
            last_message = room.last_2_messages()[1]
        except:
            print("Hey look, we made it here!")
            return False
        diff = last_message.timestamp - message.timestamp
        # print((last_message.timestamp, message.timestamp, diff.total_seconds()))
        # return ((diff.total_seconds() < 60) and (message.author == last_message.author))
        return (message.author == last_message.author)
        """

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'typing': typing,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
