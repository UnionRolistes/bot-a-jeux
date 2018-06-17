import discord
from discord.ext import commands 
import asyncio
import main

Client = main.Client
print(Client.user.id)

@Client.command()
async def test():
    await Client.say("it work!")
