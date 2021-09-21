import os
from dotenv import load_dotenv

# 1
from discord.ext import commands

print(f'Starting bot...')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ping')
async def nine_nine(ctx):
    response = "pong"
    await ctx.send(response)
    print(f'Pinged!')

bot.run(TOKEN)