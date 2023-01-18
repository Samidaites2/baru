from geezlibs.geez.database import db_x

db_y = db_x["PMPERMIT"]

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
    r = await db_y.find_one({"_id": 1})
    r2 = await db_y.find_one({"_id": "Approved"})
    if r:
        await db_y.update_one({"_id": 1}, {"$set": {"pmpermit": value}})
    else:
        await db_y.insert_one(doc)
    if not r2:
        await db_y.insert_one(doc2)


async def set_permit_message(text):
    await db_y.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})


async def set_block_message(text):
    await db_y.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await db_y.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await db_y.find_one({"_id": 1})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await db_y.find_one({"_id": "Approved"})
    if r:
        await db_y.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await db_y.insert_one(doc)


async def get_approved_users():
    results = await db_y.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []


async def deny_user(chat):
    await db_y.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})


async def pm_guard():
    result = await db_y.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    else:
        return True
