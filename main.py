import discord
import random
import data
import bot_key
import sqlite3

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

file = open("demon_list.txt", "r")
content = file.read()
demons = content.splitlines()
demons = [demon[:-1] for demon in demons]
file.close()

db = sqlite3.connect('main.sqlite')
cursor = db.cursor()

def summon(message):
    choice = random.choice(demons)
    return choice

def users():
    member_list = []
    for guild in client.guilds:
        for member in guild.members:
            member_list.append(member.name)
    return member_list


@client.event
async def on_ready():
    user_list = users()
    demons = "None"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
    userID TEXT PRIMARY KEY,
    demons text
    )
    ''')
    for user in user_list:
        cursor.execute('''INSERT OR IGNORE INTO main(userID, demons) VALUES(?, ?)''', (user, demons))
    db.commit()
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    msg = message.content.lower()
    # checks to see if the message was sent by the bot, so it doesn't reply to itself
    if message.author == client.user:
        return

    if msg.startswith('!'):
        command = msg[1:]
        if command.startswith('summon'):
            summoned = summon(message)
            info = data.demon_info[summoned]
            lvl = info[1]
            img = info[0]
            if(str(img) != 'no image found'):
                await message.channel.send(file=discord.File(img))
            await message.channel.send('You Summoned a level ' + str(lvl) + ' ' + summoned + '!')

        elif command.startswith('info'):
            name = (command[5:])
            name = name.title()
            if(data.demon_info.get(name)):
                info = data.demon_info[name]
                if(info[0] != 'no image found'):
                    await message.channel.send(file=discord.File(info[0]))
                await message.channel.send(name + ' is a level ' + str(info[1]) + ' demon of the ' + info[3] + ' race. Resistances -> '+ info[2])
            else:
                await message.channel.send('Demon not found')

        elif command.startswith('test'):
            name = message.author.name
            cursor.execute('''SELECT demons FROM main WHERE userID = ?''', ('kuzunoha bot test',))
            print(cursor.fetchone()[0])
            cursor.execute('''SELECT demons FROM main WHERE userID = ?''', ('Kuzunoha',))
            print(cursor.fetchone()[0])


client.run(bot_key.key)