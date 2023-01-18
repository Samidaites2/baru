from geezlibs.geez.database import db_x

geez = db_x["Zaid"]["rraid"]


async def rraid_user(chat):
    doc = {"_id": "Rraid", "users": [chat]}
    r = await geez.find_one({"_id": "Rraid"})
    if r:
        await geez.update_one({"_id": "Rraid"}, {"$push": {"users": chat}})
    else:
        await geez.insert_one(doc)


async def get_rraid_users():
    results = await geez.find_one({"_id": "Rraid"})
    if results:
        return results["users"]
    else:
        return []


async def unrraid_user(chat):
    await geez.update_one({"_id": "Rraid"}, {"$pull": {"users": chat}})
