"""
Migrating bot databases
Run this script only when setting-up Bot or Resetting bot data
"""

from model import *

DATABASE.connect()
DATABASE.drop_tables([Subscription, YoutubeChannel])
DATABASE.create_tables([Subscription, YoutubeChannel])
DATABASE.close()
