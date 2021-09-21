import os
from dotenv import load_dotenv
#import web
from discord.ext import commands

# herokuapp mandetory web app
#urls = (
#'/input', 'index'
#)
#class index:
#    def GET(self):
#        i = web.input(name=None)
#        return render.index(i.name)

#if __name__ == "__main__":
#    app = web.application(urls, globals())
#    app.run()
#
#render = web.template.render('templates/')

# discord bot
print(f'Starting bot...')
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
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