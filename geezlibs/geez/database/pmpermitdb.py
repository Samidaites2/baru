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


async def is_pmpermit_approved(user_id: int) -> bool:
    user = await pmpermitdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def approve_pmpermit(user_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id)
    if is_pmpermit:
        return
    return await pmpermitdb.insert_one({"user_id": user_id})


async def disapprove_pmpermit(user_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id)
    if not is_pmpermit:
        return
    return await pmpermitdb.delete_one({"user_id": user_id})
