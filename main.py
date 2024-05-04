import mysql.connector
import discord
from discord.ui import Button, View
from discord.ext import commands 
import json

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
prefix = "up!"
bot = commands.Bot(command_prefix = prefix, help_command = None, intents = intents)


with open("config.json", "r", encoding="utf-8") as fh:
    config = json.load(fh)
token = config['token']

@bot.event 
async def on_ready():
    print("Ready")

@bot.command()  
async def hello(ctx):  
    print("Ready")
    
    button1 = Button(label = "Click me!", style = discord.ButtonStyle.green)
    button2 = Button(label = "Click me!", style = discord.ButtonStyle.red)
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.send("Hello, world!", view = view)  

bot.run(token)