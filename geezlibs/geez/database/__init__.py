#import motor.motor_asyncio

#from config import MONGO_URL
#cli = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client
from config import MONGO_URL



_mongo_async_ = _mongo_client_(MONGO_URL)
_mongo_sync_ = MongoClient(MONGO_URL)
mongodb = _mongo_async_.Geez
pymongodb = _mongo_sync_.Geez







from geezlibs.geez.database.gbandb import *
from geezlibs.geez.database.gmutedb import *
from geezlibs.geez.database.pmpermitdb import *
from geezlibs.geez.database.onoff import *
from geezlibs.geez.database.rraid import *
