# Generated by Django 2.1.5 on 2019-04-10 15:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0002_message_timestamp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RoomUsers',
            new_name='RoomUser',
        ),
    ]