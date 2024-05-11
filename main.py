import mysql.connector
import discord
from discord.ui import Button, View
from discord.ext import commands 
import json
from datetime import datetime

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

database = mysql.connector.connect(
    host = config['host'],
    user = config['user'],
    password = config['password'],
    database = config['database']
)

cursor = database.cursor(dictionary = True)

@bot.event 
async def on_ready():
    print("Ready")

@bot.command()  
async def hello(ctx, title, description, role: discord.Role, date): 
    """
    -------------------------------------------------------
    Creates a new event
    User: up!hello "Title" "Description" "@<role>" "Date (in format "Month Day Year Time(am/pm)")"
    [Assuming up! is your prefix]
    -------------------------------------------------------
    Parameters:
        title - the title of the role (str)
        description - the discription of the role (str)
        role - appropriate role to send (Discord mention)
        date - in format listed above (e.g. "May 5 2024 1:30pm") (str)
    -------------------------------------------------------
    """
     
    embed = discord.Embed(
        title = (f"{title} - {date}"),                
        description= (f"{description}\n This event is tailored for {role.name}"),  
        color=discord.Color.blue()           
    )
    
    button1 = Button(label = "Click me!", style = discord.ButtonStyle.green)
    button2 = Button(label = "Click me!", style = discord.ButtonStyle.red)
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    date_object = datetime.strptime(date, '%B %d %Y %I:%M%p')
    timestamp = date_object.timestamp()

    authorID = ctx.author.id 

    def rsvp(authorID):
        async def rsvp_auxiliary(interaction):
            """
            rsvp_auxiliary can ONLY have interaction as its parameter. To access additional ones, 
            """
            try:
                sql = "INSERT INTO events (ID, DATE, TITLE, DESCRIPTION, RSVP, HOURS) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (1, timestamp, title, description, authorID, 2)
                cursor.execute(sql, val)
                database.commit()
                print(f"Worked")
            except Exception as error:
                database.rollback() 
                print(f"Transaction failed. Error: {error}")

            await interaction.response.send_message("Added to event list!", ephemeral=True)
        return rsvp_auxiliary

    button1.callback = rsvp(authorID)

    role = discord.utils.get(ctx.guild.roles, name=role.name)
    for member in ctx.guild.members:
        if role in member.roles:
            await member.send(f"**New event!**\nYou are recieving this message because you opted-in for events relating to {role.name}. To stop recieving event information, click the appropriate button", embed=embed, view = view)  

    await ctx.send(embed=embed, view = view)  


bot.run(token)