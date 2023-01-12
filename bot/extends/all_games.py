from dotenv import load_dotenv
from discord.ext import commands
import os
import importlib
import asyncio
import sys


# import for folder games p4.py

from .game.P4 import P4



load_dotenv()
print('coucou from games')


class Game(P4, commands.Cog, name='Game'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None


    async def cog_load(self):  # called when the cog is loaded
        print(self.__class__.__name__ + " is loaded")

    # @commands.command(name="tttt", help='tttt', aliases=['tt'], )
    # async def _ttttt(self, event):  # called when the cog is loaded
    #     await event.send('game')



async def setup(bot):
    await bot.add_cog(Game(bot))
