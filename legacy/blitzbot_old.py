# BlitzBot 1.0, for Nuffle.xyz
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by poncho_dlv

#### DEPRECATED ####
#This version is outdated and is superceded by blitzbot, and is kept for legacy reasons.

import os
import discord
from discord import app_commands
import pymysql
from dotenv import load_dotenv
import blitzbot_parser
# legacy library, remove when bug fixed
import audioop


# Initialize variables, define discord intents

intents = discord.Intents(messages=True, message_content=True, members=True, guilds=True)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


load_dotenv(dotenv_path='blitzbot.env')


conn = None
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILDID')
DB_USER = os.getenv('DATABASE_USER')
DB_PASS = os.getenv('DATABASE_PASS')
DB_NAME = os.getenv('DATABASE_NAME')
DB_HOST = os.getenv('DATABASE_HOST')
DB_PORT = os.getenv('DATABASE_PORT')






#First test slash command
@tree.command(
    name='searchcoach',
    description="Find a player by their name. TEST"
)
async def findCoach(interaction, playerName: str):
    response = "Hey, thanks for pinging me! Attempting query"
    await message.channel.send(response)
    
    
@tree.command(
    name='searchteam',
    description="Find a team based on their team name. TEST"
)
async def findTeam(interaction, teamName: str):
    response = "Hey, thanks for pinging me! Attempting to find team"
    await message.channel.send(response)






def databaseConnect():
    try:
        #Add connection here
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME
            )
            
        cur = conn.cursor()
        return cur
    except:
        print(f'\nException establishing connection to database!')
    
def databaseDisconnect():
    #Disconnect here
    conn.close()
    







@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    #for guild in client.guilds:
    #    if guild.name == GUILD:
    #        break
    #        
    #print({guild.name})
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    #await tree.sync(guild=
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    #print(f'{client.user} has connected to Discord!')
    
    
@client.event
async def on_message(message):
    #print(f'on message event {message}')
    if message.author == client.user:
        return
        
    if message.content.upper().startswith('!BLITZ'):
        #print(f'\nBlitz command!')
        
        #Process command as needed so appropriate action can be taken.
        words = message.content.upper().split()
        #Slice off the !blitz command
        words = words[1:]
        
        #If there's no command, post back the help command, otherwise continue
        if not words:
            ##TODO ADD HELP CALL HERE
            print('No commands')
        else:
            response = blitzbot_parser.ParseCommand(words)
            await message.channel.send(response)
        
        #Call to parser and handle request
        
        
        
    else:
        #print(f'\nNot a blitz command.')
        return
        
    #print(message.content.upper())
    #if message.content.upper() == '!BLITZ':
    #    response = "Hey, thanks for pinging me! Attempting query"
    #    await message.channel.send(response)
        
        #Test code to see if connection established
        #cur = databaseConnect()
        
        #cur.execute("SHOW TABLES")
        #tables = cur.fetchall()
        #print(tables)
        
        #databaseDisconnect()
        
    
client.run(TOKEN)