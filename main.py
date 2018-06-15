#Imports
import discord
import ConfigParser

#Config file
config = configparser.ConfigParser()
config.read('config.ini')
bot_key = config.get("Bot", "key") #bot's key

#bot client
Client = discord.Client()

Client.start(bot_key)
