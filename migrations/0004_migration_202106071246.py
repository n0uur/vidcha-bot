# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Subscription(peewee.Model):
    channel_id = BigIntegerField()
    youtube_id = CharField(max_length=255)
    subscribed_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "subscription"


@snapshot.append
class YoutubeChannel(peewee.Model):
    youtube_id = CharField(max_length=255, unique=True)
    youtube_name = CharField(max_length=255)
    youtube_image = CharField(max_length=512, null=True)
    youtube_last_notify_vid = CharField(max_length=255, null=True)
    class Meta:
        table_name = "youtubechannel"


def forward(old_orm, new_orm):
    old_subscription = old_orm['subscription']
    subscription = new_orm['subscription']
    return [
        # Convert datatype of the field subscription.channel_id: INT -> BIGINT
        subscription.update({subscription.channel_id: old_subscription.channel_id.cast('SIGNED')}).where(old_subscription.channel_id.is_null(False)),
    ]


def backward(old_orm, new_orm):
    old_subscription = old_orm['subscription']
    subscription = new_orm['subscription']
    return [
        # Convert datatype of the field subscription.channel_id: BIGINT -> INT
        subscription.update({subscription.channel_id: old_subscription.channel_id.cast('SIGNED')}).where(old_subscription.channel_id.is_null(False)),
    ]
