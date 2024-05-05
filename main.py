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
async def hello(ctx, title, description, role: discord.Role): 
    """
    -------------------------------------------------------
    Creates a new event
    User: up!hello "Title" "Description" "@<role>"
    [Assuming up! is your prefix]
    -------------------------------------------------------
    Parameters:
        title - the title of the role (str)
        description - the discription of the role (str)
        role - appropriate role to send (Discord mention)
    -------------------------------------------------------
    """
     
    embed = discord.Embed(
        title = title,                
        description= (f"{description} \n This event is tailored for {role.name}"),  
        color=discord.Color.blue()           
    )
    
    button1 = Button(label = "Click me!", style = discord.ButtonStyle.green)
    button2 = Button(label = "Click me!", style = discord.ButtonStyle.red)
    view = View()
    view.add_item(button1)
    view.add_item(button2)

    role = discord.utils.get(ctx.guild.roles, name=role.name)
    for member in ctx.guild.members:
        if role in member.roles:
            await member.send(f"**New event!**\nYou are recieving this message because you opted-in for events relating to {role.name}. To stop recieving event information, click the appropriate button", embed=embed, view = view)  

    await ctx.send(embed=embed, view = view)  

bot.run(token)