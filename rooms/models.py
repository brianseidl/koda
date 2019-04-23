from django.contrib.auth.models import User
from django.db import models
from online_users.models import OnlineUserActivity

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

    # TODO (brian): change name for method to get_all_messages
    def last_10_messages(self):
        return self.message_set.order_by('-timestamp').all()

    def last_2_messages(self):
        return self.message_set.order_by('-timestamp').all()[:2]

    def who_is_online(self):
        # TODO (brian): This is so disgusting but it works I guess
        weird_user_objects = OnlineUserActivity.get_user_activities()
        all_online_users = [item.user for item in weird_user_objects]
        online_users = []
        offline_users = []
        for user in self.members:
            if user in all_online_users:
                online_users.append(user)
            else:
                offline_users.append(user)
        return online_users, offline_users

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
