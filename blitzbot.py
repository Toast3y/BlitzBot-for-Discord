# BlitzBot 1.0, for Nuffle.xyz
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by 

import os
import discord
from discord import app_commands
from discord.ext import commands
import pymysql
from dotenv import load_dotenv
# legacy library, remove when bug fixed
import audioop

#Imports to separate and manage code
import blitzbot_data
import blitzbot_handler


# Initialize variables, define discord intents

#intents = discord.Intents(messages=True, message_content=True, members=True, guilds=True)
#client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(client)


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

def databaseConnect():
    try:
        #Add connection here
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME
            )
            
        if (conn != None):
            return conn
        else:
            raise Exception("Unable to establish connection to server")
        
    except:
        print(f'\nException establishing connection to database! No connection made.')
        
def getCursor(conn):
    if (conn != None):
        cur = conn.cursor()
        return cur
    else:
        raise Exception("Unable to establish connection to server")
        
    
def databaseDisconnect(cur, conn):
    #Disconnect here
    cur.close()
    conn.close()
    
    

class BlitzCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    #@app_commands.command(name='ping', description='Test ping pong')
    #async def _ping(self, interaction: discord.Interaction):
    #    #testing method for connections and database interactions
    #    conn = databaseConnect()
    #    cursor = getCursor(conn)
    #    
    #    if (cursor != None):
    #        response = blitzbot_handler.pingServer(cursor)
    #        databaseDisconnect(cursor, conn)
    #        await interaction.response.send_message(f"```{response}```")
    #    else:
    #        await interaction.response.send_message(f"A database connection could not be established. Please try again later.")
    #        
            
            
        
    @app_commands.command(name='findcoach', description='Find a Coach profile on Nuffle.xyz')
    async def _findCoach(self, interaction: discord.Interaction, coach: str):
        #Open database connection
        if (coach != ""):
            conn = databaseConnect()
            cursor = getCursor(conn)
            
            if (cursor != None):
                response = blitzbot_handler.findCoach(cursor, coach)
                databaseDisconnect(cursor, conn)
                await interaction.response.send_message(embed=response)
            else:
                await interaction.response.send_message(f"A database connection could not be established. Please try again later.")
        else:
            await interaction.response.send_message("findcoach command requires a valid coach name.")
            
            
            
        
    @app_commands.command(name='findteam', description='Find a Team on Nuffle.xyz')
    async def _findTeam(self, interaction: discord.Interaction, team: str):
        #Open database connection
        if (team != ""):
            conn = databaseConnect()
            cursor = getCursor(conn)
            
            if (cursor != None):
                response = blitzbot_handler.findTeam(cursor, team)
                databaseDisconnect(cursor, conn)
                await interaction.response.send_message(embed=response)
            else:
                await interaction.response.send_message(f"A database connection could not be established. Please try again later.")
        else:
            await interaction.response.send_message("findteam command requires a valid team name.")
            
            
            
    @app_commands.command(name='fetchstandings', description='Return a link and top 4 teams in a given competition')
    async def _fetchstandings(self, interaction: discord.Interaction, league: str):
        if (league != ""):
            conn = databaseConnect()
            cursor = getCursor(conn)
            
            if (cursor != None):
                response = blitzbot_handler.fetchStandings(cursor, league)
                databaseDisconnect(cursor, conn)
                await interaction.response.send_message(embed=response)
            else:
                await interaction.response.send_message(f"A database connection could not be established. Please try again later.")
        else:
            await interaction.response.send_message(f"fetchstandings command requires a valid competition name")
            
            
            
            
    @app_commands.command(name='fetchmatchday', description='Return the current pairings for a given competition')
    @app_commands.rename(matchday='round')
    async def _fetchmatchday(self, interaction: discord.Interaction, league: str, matchday: int):
        if (league != "" and matchday > 0):
            conn = databaseConnect()
            cursor = getCursor(conn)
            
            if (cursor != None):
                response = blitzbot_handler.fetchMatchday(cursor, league, matchday)
                databaseDisconnect(cursor, conn)
                await interaction.response.send_message(embed=response)
            else:
                await interaction.response.send_message(f"A database connection could not be established. Please try again later.")
        else:
            await interaction.response.send_message(f"fetchmatchday command requires a valid competition name and round")
            
            
            
            
    #@app_commands.command(name='schedulematch', description='Set a reminder for your match, pinging you and your specified opponent.')
    #async def _scheduleMatch(self, interaction: discord.Interaction, opponent: discord.Member):
    #    await interaction.response.send_message("Scheduled match. TEST.")
        
      

      
#class BlitzAdminCog(commands.Cog):
#    def __init__(self, bot: commands.Bot):
#        self.bot = bot
#        
#    @app_commands.command(name='admintask', description='Admin test adding a cog', guild_ids = GUILD_ID)
#    async def _adminTask(self, interaction: discord.Interaction):
#        await interaction.response.send_message("Admin task run. TEST.")
#   

     


class BlitzDataCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name='fetchmatchdayplain', description='Return match day pairing as plaintext')
    @app_commands.rename(matchday='round')
    async def _fetchmatchdayplain(self, interaction: discord.Interaction, league: str, matchday: int):
        if (league != "" and matchday > 0):
            conn = databaseConnect()
            cursor = getCursor(conn)
            
            if (cursor != None):
                response = blitzbot_data.fetchMatchday_data(cursor, league, matchday)
                databaseDisconnect(cursor, conn)
                await interaction.response.send_message(f"```{response}```")
            else:
                await interaction.response.send_message(f"A database connection could not be established. Please try again later.")
        else:
            await interaction.response.send_message(f"fetchmatchdayplain command requires a valid competition name and round")
            
            


class BlitzBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents(messages=True, message_content=True, members=True, guilds=True))
        #self.tree = discord.app_commands.CommandTree(self)
		
    async def setup_hook(self) -> None:
        await self.add_cog(BlitzCog(self))
        await self.add_cog(BlitzDataCog(self))
        #await self.add_cog(BlitzAdminCog(self))
        self.tree.copy_global_to(guild = discord.Object(id=GUILD_ID))
        await self.tree.sync()
        
        
        
		
client = BlitzBot()
	
client.run(TOKEN)