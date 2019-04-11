from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# Fun fact. Django creates an id/pk column for every
# model so we don't need to create an id column

class Room(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='RoomUser')

    def add_user(self, user):
        cu = RoomUsers(user=user, room=self)
        cu.save()

    @property
    def members(self):
        return self.users.all()

    def last_10_messages(self):
        return self.message_set.order_by('-timestamp').all()

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + ": " + str(self.content)[0:20]


class RoomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + "-" + str(self.room)
