import discord
import requests
import json
import test
import random
import data
import bot_key

client = discord.Client()

file = open("demon_list.txt", "r")
content = file.read()
demons = content.splitlines()
demons = [demon[:-1] for demon in demons]
file.close()


def summon(message):
    choice = random.choice(demons)
    return choice


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content.lower()
    # checks to see if the message was sent by the bot, so it doesn't reply to itself
    if message.author == client.user:
        return

    if msg.startswith('!summon'):
        summoned = summon(message)
        info = data.demon_info[summoned]
        lvl = info[1]
        await message.channel.send('You Summoned a level ' + str(lvl) + ' ' + summoned + '!')


client.run(bot_key.key)
