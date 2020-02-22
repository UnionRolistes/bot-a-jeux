#!/bin/python3.8
import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print("yay un message : {0.author} : {0.content}".format(message))

client = MyClient()
client.run("NDU2ODUzMjAzNzY2NjA3ODgz.XlBtHA.q6nazRMwZaoipkn16hL88-rWa10")
