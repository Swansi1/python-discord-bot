"""
Neptun discord órarend
~~~~~~~~~~~~~~~~~~~

Basic neptun órarend discordhoz


"""

__title__ = 'python_discord_bot'
__author__ = 'Zrinyi Patrik'
__version__ = '1.0.0'

from datetime import *
from .discordbot_main import *
from .dataStruct import *
from .config import *
from .lesson import *
from .neptunAPI import *
from .userManager import *
from .neptunAPI import *

def start_bot():
    'Bot futtatása'
    client.run(config.bot_token)