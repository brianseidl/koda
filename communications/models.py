from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# Fun fact. Django creates an id/pk column for every
# model so we don't need to create an id column

class Channel(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='ChannelUsers')

    def add_user(self, user):
        cu = ChannelUsers(user=user, channel=self)
        cu.save()

    @property
    def members(self):
        return self.users.all()
    
    def __str__(self):
        return self.name

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.author + '-' + self.content

class ChannelUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
