"""
python script for my Discord bot 'lapz' which allows to retrieve f1 laptimes plots 
after a session using the fastf1 python package 

Entirely for personal use 
"""

import os
import discord
from dotenv import load_dotenv

# loading environment
load_dotenv()

# loading token 
TOKEN=os.getenv("DISCORD_TOKEN")

# client obj. (~bot) from discord.py
bot = discord.Client(intents=discord.Intents.default())


# event listener (message sent to a channel)
@bot.event 
async def on_message(message):
    if message.author.bot:      # ensures message has not been sent by bot
        return

bot.run(TOKEN)
