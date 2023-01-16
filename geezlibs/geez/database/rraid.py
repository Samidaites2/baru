from typing import Dict, List, Union
from geezlibs.geez.database import mongodb

geez = geezdb


async def rraid_user(chat):
    doc = {"_id": "Rraid", "users": [chat]}
    r = await geezdb.find_one({"_id": "Rraid"})
    if r:
        await geezdb.update_one({"_id": "Rraid"}, {"$push": {"users": chat}})
    else:
        await geezdb.insert_one(doc)


async def get_rraid_users():
    results = await geezdb.find_one({"_id": "Rraid"})
    if results:
        return results["users"]
    else:
        return []


async def unrraid_user(chat):
    await geezdb.update_one({"_id": "Rraid"}, {"$pull": {"users": chat}})



"""
from geezlibs.geez.database import cli

collection = cli["Geez"]["rraid"]


async def rraid_user(chat):
    doc = {"_id": "Rraid", "users": [chat]}
    r = await geezdb.find_one({"_id": "Rraid"})
    if r:
        await geezdb.update_one({"_id": "Rraid"}, {"$push": {"users": chat}})
    else:
        await geezdb.insert_one(doc)


async def get_rraid_users():
    results = await geezdb.find_one({"_id": "Rraid"})
    if results:
        return results["users"]
    else:
        return []


async def unrraid_user(chat):
    await geezdb.update_one({"_id": "Rraid"}, {"$pull": {"users": chat}})
"""
