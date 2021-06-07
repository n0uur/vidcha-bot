# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Subscription(peewee.Model):
    channel_id = IntegerField()
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
    old_youtubechannel = old_orm['youtubechannel']
    youtubechannel = new_orm['youtubechannel']
    return [
        # Convert datatype of the field subscription.youtube_id: TEXT -> VARCHAR(255)
        subscription.update({subscription.youtube_id: old_subscription.youtube_id.cast('CHAR')}).where(old_subscription.youtube_id.is_null(False)),
        # Convert datatype of the field youtubechannel.youtube_last_notify_vid: TEXT -> VARCHAR(255)
        youtubechannel.update({youtubechannel.youtube_last_notify_vid: old_youtubechannel.youtube_last_notify_vid.cast('CHAR')}).where(old_youtubechannel.youtube_last_notify_vid.is_null(False)),
        # Convert datatype of the field youtubechannel.youtube_image: TEXT -> VARCHAR(512)
        youtubechannel.update({youtubechannel.youtube_image: old_youtubechannel.youtube_image.cast('CHAR')}).where(old_youtubechannel.youtube_image.is_null(False)),
        # Convert datatype of the field youtubechannel.youtube_id: TEXT -> VARCHAR(255)
        youtubechannel.update({youtubechannel.youtube_id: old_youtubechannel.youtube_id.cast('CHAR')}).where(old_youtubechannel.youtube_id.is_null(False)),
        # Convert datatype of the field youtubechannel.youtube_name: TEXT -> VARCHAR(255)
        youtubechannel.update({youtubechannel.youtube_name: old_youtubechannel.youtube_name.cast('CHAR')}).where(old_youtubechannel.youtube_name.is_null(False)),
    ]


def backward(old_orm, new_orm):
    old_subscription = old_orm['subscription']
    subscription = new_orm['subscription']
    old_youtubechannel = old_orm['youtubechannel']
    youtubechannel = new_orm['youtubechannel']
    return [
        # Don't know how to do the conversion correctly, use the naive
        subscription.update({subscription.youtube_id: old_subscription.youtube_id}).where(old_subscription.youtube_id.is_null(False)),
        # Don't know how to do the conversion correctly, use the naive
        youtubechannel.update({youtubechannel.youtube_last_notify_vid: old_youtubechannel.youtube_last_notify_vid}).where(old_youtubechannel.youtube_last_notify_vid.is_null(False)),
        # Don't know how to do the conversion correctly, use the naive
        youtubechannel.update({youtubechannel.youtube_image: old_youtubechannel.youtube_image}).where(old_youtubechannel.youtube_image.is_null(False)),
        # Don't know how to do the conversion correctly, use the naive
        youtubechannel.update({youtubechannel.youtube_id: old_youtubechannel.youtube_id}).where(old_youtubechannel.youtube_id.is_null(False)),
        # Don't know how to do the conversion correctly, use the naive
        youtubechannel.update({youtubechannel.youtube_name: old_youtubechannel.youtube_name}).where(old_youtubechannel.youtube_name.is_null(False)),
    ]
