"""
python script for my Discord bot 'lapz' which allows to retrieve f1 laptimes plots 
after a session using the fastf1 python package 

Entirely for personal use 
"""

import discord 

# importing the token from external file
with open('token.tok', 'r') as f:
    TOKEN = f.readline().strip()

# client obj. (~bot) from discord.py
bot = discord.Client(intents=discord.Intents.default())

# event listener (bot goes online )
@bot.event 
async def on_ready():
    # connected server counter 
    guild_count = 0

    print("SERVERS CONNECTED: ")
    for guild in bot.guilds:
        print(f"server: {guild.id} (name: {guild.name})")

        guild_count += 1


# event listener (message sent to a channel)
@bot.event 
async def on_message(message):
    if message.content == "hello":
        # sending back a message 
        await message.channel.send("Hey YOU")

bot.run(TOKEN)
