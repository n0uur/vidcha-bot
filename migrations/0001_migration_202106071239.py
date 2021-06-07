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


