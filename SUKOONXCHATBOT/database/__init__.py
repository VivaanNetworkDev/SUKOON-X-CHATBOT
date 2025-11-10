from pymongo import MongoClient

import config

sukoondb = MongoClient(config.MONGO_URL)
sukoon = sukoondb["SukoonDb"]["Sukoon"]


from .chats import *
from .users import *
