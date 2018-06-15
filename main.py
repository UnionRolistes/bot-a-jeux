#Imports
import discord
import asyncio
import configparser

#Config file
config = configparser.ConfigParser()
config.read('config.ini')
bot_key = config.get("Bot", "key") #bot's key

#bot client
Client = discord.Client()

@Client.event
async def on_ready():
    print('Starting Bot!')

Client.run(bot_key)
