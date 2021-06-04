"""
Model for working with database
"""

from peewee import *
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = SqliteDatabase(os.environ.get("DATABASE_SQL_FILE")) # you can change to (real)SQL like MySQL or PostgreSQL, If you want to :)

class BaseModel(Model):
    class Meta:
        database = DATABASE

class Subscription(BaseModel):
    channel_id = IntegerField(null=False)
    youtube_id = TextField(null=False)    
    subscribed_at = DateTimeField(default=datetime.datetime.now)

class YoutubeChannel(BaseModel):
    # I will not using any relationship
    # It's just not necessary :)
    youtube_id = TextField(unique=True, null=False)
    youtube_name = TextField(null=False)
    youtube_image = TextField(null=True)
    youtube_last_notify_vid = TextField(null=True)
