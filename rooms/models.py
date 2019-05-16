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
        """
        Gross hack to determine who from the chat room is online.
        TODO (brian): Eventually convert this feature via WebSocket
            connection via consumers.py.  Don't have time to fix now.

        Precondition:
            Detail Room/Chat view is called

        Postcondition:
            2 tuples will be return containing the status of their
            activity within the last 15 minutes

        Args:
            None

        Returns:
            (list, list): tuple of 2 lists.  The first list will contain
                a list of people in the room active within the last 15
                minutes.  The second list are members in the room who
                were not active within the last 15 minutes.
        """
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
