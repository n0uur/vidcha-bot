# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Subscription(peewee.Model):
    channel_id = IntegerField()
    youtube_id = TextField()
    subscribed_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "subscription"


@snapshot.append
class YoutubeChannel(peewee.Model):
    youtube_id = TextField(unique=True)
    youtube_name = TextField()
    youtube_image = TextField(null=True)
    youtube_last_notify_vid = TextField(null=True)
    class Meta:
        table_name = "youtubechannel"


