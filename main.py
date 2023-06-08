"""
python script for my Discord bot 'lapz' which allows to retrieve f1 laptimes plots 
after a session using the fastf1 python package 

Entirely for personal use 
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv 

import sessions

# loading environment
load_dotenv()

# loading token and bot 
TOKEN=os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.command(
    brief="Plots race information for given drivers",
    help="Displays an image containing two plots describing race pace for given drivers: One boxplot showing average pace and One curve plot showing lap-by-lap times. If no drivers given, all drivers' laps will be plotted."
)
async def plot(ctx, *args):
    print("Generating file...")
    if len(args) == 0:
        params = ()
    else:
        params = [arg.upper() for arg in args]
    filename = sessions.generate_file(params)
    print("File generated, sending in progress...")
    with open(filename, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

bot.run(TOKEN)
