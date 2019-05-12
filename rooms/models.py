from django.contrib.auth.models import User
from django.db import models
from online_users.models import OnlineUserActivity


class Room(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='RoomUser')
    rtype = models.CharField(max_length=10, default="room")

    def add_user(self, user):
        cu = RoomUser(user=user, room=self)
        cu.save()

    @property
    def members(self):
        return self.users.all()

    def load_messages(self):
        return self.message_set.order_by('-timestamp').all()

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
        return str(self.author) + ": " + str(self.content)


class RoomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + "-" + str(self.room)
