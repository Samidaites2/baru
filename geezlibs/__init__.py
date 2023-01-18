__version__ = "1.2.5"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2017-present Dan <https://github.com/delivrance>"

BL_GCAST = [-1001692751821, -1001473548283, -1001459812644, -1001433238829, -1001476936696, -1001327032795, -1001294181499, -1001419516987, -1001209432070, -1001296934585, -1001481357570, -1001459701099, -1001109837870, -1001485393652, -1001354786862, -1001109500936, -1001387666944, -1001390552926, -1001752592753]
BL_GEEZ = [1245451624]
DEVS = [874946835, 1488093812, 1720836764, 1883494460, 2003295492, 951454060, 1646020461]
BOT_VER = "1.7.3"

async def join(client):
    try:
        await client.join_chat("ramsupportt")
        await client.join_chat("GeezSupport")
    except BaseException:
        pass
