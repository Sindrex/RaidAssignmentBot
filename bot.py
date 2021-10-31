import os
from dotenv import load_dotenv
from discord.ext import commands
from csv_parser import getparsed

# discord bot
print(f'Starting bot...')
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ping')
async def ping(ctx):
    print(f'Pinged!')
    response = 'pong'
    await ctx.send(response)

@bot.command(name='post')
@commands.has_role('Raid Leader')
async def post(ctx, raid):
    print(f'Posting formatted tank and healer assignments for {raid}')
    response = getparsed(raid)
    if response == None:
        response = 'Something went wrong :('
    try:
        for str in response:
            await ctx.send(str)
    except Exception as e:
        response = 'Unable to send message. Too long?'
        await ctx.send(response)
    print(f'Finished posting assignments for {raid}')
    await ctx.message.delete()

bot.run(TOKEN)