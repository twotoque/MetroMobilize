import mysql.connector
import discord
from discord.ui import Button, View
from discord.ext import commands 
import json

intents = discord.Intents.default()
intents.members = True 
intents.guilds = True
intents.message_content = True
intents.dm_messages = True 
prefix = "up!"
bot = commands.Bot(command_prefix = prefix, help_command = None, intents = intents)


with open("config.json", "r", encoding="utf-8") as fh:
    config = json.load(fh)
token = config['token']

@bot.event 
async def on_ready():
    print("Ready")

@bot.command()  
async def hello(ctx, title, description, role): 
     
    embed = discord.Embed(
        title = title,                
        description= (f"{description} \n This event is tailored for {role}"),  
        color=discord.Color.blue()           
    )
    
    button1 = Button(label = "Click me!", style = discord.ButtonStyle.green)
    button2 = Button(label = "Click me!", style = discord.ButtonStyle.red)
    view = View()
    view.add_item(button1)
    view.add_item(button2)

    role = discord.utils.get(ctx.guild.roles, name=role)
    for member in ctx.guild.members:
        if role in member.roles:
            await member.send("New event! \n You are recieving this message because you opted-in for events relating to this area. To stop recieving event information, click the appropriate button", embed=embed, view = view)  

    await ctx.send(embed=embed, view = view)  

bot.run(token)