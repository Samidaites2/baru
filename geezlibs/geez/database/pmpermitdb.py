from typing import Dict, List, Union
from geezlibs.geez.database import mongodb

"""
pmpermitdb = cli["geez"]["pmpermit"]
"""
pmpermitdb = mongodb.permit

PMPERMIT_MESSAGE = (
    "**peringatan! tolong baca pesan ini dengan hati-hati..\n\n**"
    "**Saya Geez-Pyro saya di sini untuk melindungi tuanku dari smsm**"
    "**jika Anda bukan spammer, harap tunggu!.\n\n**"
    "**sampai saat itu, jangan spam atau Anda akan diblokir dan dilaporkan bb saya, jadi berhati-hatilah untuk mengirim pesan pesan!**"
)

BLOCKED = "**Spammer, blocked!**"

LIMIT = 5


async def set_pm(value: bool):
    doc = {"_id": 1, "pmpermit": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await pmpermitdb.find_one({"_id": 1})
    r2 = await pmpermitdb.find_one({"_id": "Approved"})
    if r:
        await pmpermitdb.update_one({"_id": 1}, {"$set": {"pmpermit": value}})
    else:
        await pmpermitdb.insert_one(doc)
    if not r2:
        await pmpermitdb.insert_one(doc2)


async def set_permit_message(text):
    await pmpermitdb.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})


async def set_block_message(text):
    await pmpermitdb.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await pmpermitdb.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await pmpermitdb.find_one({"_id": 1})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await pmpermitdb.find_one({"_id": "Approved"})
    if r:
        await pmpermitdb.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await pmpermitdb.insert_one(doc)


async def get_approved_users():
    results = await pmpermitdb.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []


async def deny_user(chat):
    await pmpermitdb.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})


async def pm_guard():
    result = await pmpermitdb.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    else:
        return True
