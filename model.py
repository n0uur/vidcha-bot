"""
Model for working with database
"""

from peewee import *
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_DB = os.environ.get("DATABASE")

if CONFIG_DB == "sqlite":

    DATABASE = SqliteDatabase(os.environ.get("DATABASE_SQL_FILE"))

elif CONFIG_DB == "mysql":

    DB_HOST = os.environ.get("DATABASE_MYSQL_HOST")
    DB_NAME = os.environ.get("DATABASE_MYSQL_NAME")
    DB_USERNAME = os.environ.get("DATABASE_MYSQL_USERNAME")
    DB_PASSWORD = os.environ.get("DATABASE_MYSQL_PASSWORD")
    DB_PORT = int(os.environ.get("DATABASE_MYSQL_PORT", 3306))

    DATABASE = MySQLDatabase(
        database=DB_NAME, 
        host=DB_HOST, 
        user=DB_USERNAME, 
        password=DB_PASSWORD,
        port=DB_PORT
    )

else:
    print("not supported database type..")
    exit(1)

class BaseModel(Model):
    class Meta:
        database = DATABASE

class Subscription(BaseModel):
    channel_id = BigIntegerField(null=False)  # can't set default int length in MySQL, use Big int instead
    youtube_id = CharField(null=False)
    subscribed_at = DateTimeField(default=datetime.datetime.now)

class YoutubeChannel(BaseModel):
    # I will not using any relationship
    # It's just not necessary :)
    youtube_id = CharField(unique=True, null=False)
    youtube_name = CharField(null=False)
    youtube_image = CharField(null=True, max_length=512)
    youtube_last_notify_vid = CharField(null=True)
