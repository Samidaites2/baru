import os
import sys
from pyrogram import Client

from geezlibs.geez.helper.adminHelpers import *
from geezlibs.geez.helper.aiohttp_helper import*
from geezlibs.geez.helper.basic import *
from geezlibs.geez.helper.constants import *
from geezlibs.geez.helper.data import *
from geezlibs.geez.helper.inline import *
from geezlibs.geez.helper.interval import *
from geezlibs.geez.helper.parser import *
from geezlibs.geez.helper.PyroHelpers import *
from geezlibs.geez.helper.utility import *



def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Geez"])

