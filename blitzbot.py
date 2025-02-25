# BlitzBot 1.0, for Nuffle.xyz
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv

import os
import discord
import textwrap
from discord import app_commands
from discord.ext import commands
import pymysql
from dotenv import load_dotenv
# legacy library, remove when bug fixed
import audioop

#Imports to separate and manage code
import blitzbot_data
import blitzbot_handler
import blitzbot_config


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
LOCALDB_USER = os.getenv('LOCAL_DATABASE_USER')
LOCALDB_PASS = os.getenv('LOCAL_DATABASE_PASS')
LOCALDB_NAME = os.getenv('LOCAL_DATABASE_NAME')
LOCALDB_HOST = os.getenv('LOCAL_DATABASE_HOST')

#Connection to remote database, ran during command parsing.
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
        

        
##Connection to local database. getCursor() and disconnect should work for both.
def localDatabaseConnect():
    try:
        conn = pymysql.connect(
            host = LOCALDB_HOST,
            user = LOCALDB_USER,
            password = LOCALDB_PASS,
            db=LOCALDB_NAME
        )
        
        if (conn != None):
            return conn
        else:
            raise Exception("Unable to establish connection to local database")
            
    except:
        print(f'\nException establish connection to local database! No connection made.')
            
            
#Manage cursor and disconnect from database.
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
    
    
    
    
##Cog for main functionality within Blitzbot, fetching and returning data.
##Many may be made redundant once server configuration commands go live.
class BlitzCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    ##TODO: Set up command structure for server and channel integrated commands
    
    #Standings command
    #Matches command
    
    
    
    #findcoach command
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
            
            
            
    #findteam command
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
            
            
            
    #fetchstandings command
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
            
            
            
    #fetchMatchday command
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
            
            
        
      

##Cog for administration and self-serve commands for Nuffle.xyz      
#class BlitzAdminCog(commands.Cog):
#    def __init__(self, bot: commands.Bot):
#        self.bot = bot
        
    #@app_commands.command(name='admintask', description='Admin test adding a cog', guild_ids = GUILD_ID)
    #async def _adminTask(self, interaction: discord.Interaction):
    #    #await interaction.response.send_message("Admin task run. TEST.")
    #    conn = localDatabaseConnect()
    #    cursor = getCursor(conn)
    #    
    #    if(cursor != None):
    #        await interaction.response.send_message(f"Database Connection Established")
    #    else:
    #        await interaction.response.send_message(f"No connection established.")
   

##Cog for scheduling matches and various commands to assist.
#class BlitzScheduleCog(commands.Cog):
#    def __init__(self, bot: commands.Bot):
#        self.bot = bot
#        
#    @app_commands.command(name='schedulematch', description='Set a reminder for your match, pinging you and your opponent an hour in advance')
#    async def _scheduleMatch(self, interaction: discord.Interaction, opponent: discord.Member):
#        return

    #cancelmatch
    



##Cog for standard help commands, such as a command list and configuration 
class BlitzHelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    #about command
    @app_commands.command(name='about', description='Learn more about BlitzBot')
    async def _about(self, interaction: discord.Interaction):
        response = """
            ================
            Blitzbot for Discord, powered by Nuffle.xyz
            Designed by Christopher Dunne AKA Toast3y
            Nuffle by Galentio, inspired by SpikeBot by Poncho_dlv
            ================
                    
            Blitzbot is an administrative tool to help Blood Bowl league administrators to display vital information for their leagues right in the Discord client.
            Display league standings, provide player and match information, and export plaintext data for external programs.
            Type /commands to see a list of all commands.
            For setup instructions, please see: <insert link here>
                    
            ================
            Help keep Blitzbot and Nuffle running, and consider donating:
                    
            Toast3y (BlitzBot) - https://ko-fi.com/toast3y
            Galentio (Nuffle.xyz) - https://ko-fi.com/galentio
            ================"""
        await interaction.response.send_message(f"```{textwrap.dedent(response)}```", ephemeral=True)
        
        
    #commands command
    @app_commands.command(name='commands', description='See a helpful list of commands for BlitzBot')
    async def _commands(self, interaction: discord.Interaction):
        response = """
            Commands for BlitzBot (note that some commands may be restricted to certain users)
            
            Help commands:
            /about - Learn more about BlitzBot
            /commands - See a helpful list of commands for Blitzbot
            /support - Find links to help support development on Blitzbot and Nuffle
            
            Standard commands:
            /findcoach - Find a Coach profile on Nuffle.xyz
            /findteam - Find a Team on Nuffle.xyz
            /fetchmatchday - Return the current pairings for a given competition
            /fetchstandings - Return a link and top 4 teams in a given competition
            
            Configuration commands:
            /registerserver - Register your server with BlitzBot to enable advanced functionality
            
            Data export commands:
            /fetchmatchdayplain - Return match day pairing as plaintext
            
            """
        await interaction.response.send_message(f"```{textwrap.dedent(response)}```", ephemeral=True)
        
    
    #Support command
    @app_commands.command(name='support', description='Find links to help support development on Blitzbot and Nuffle')
    async def _support(self, interaction: discord.Interaction):
        response = """
            If you want to help support BlitzBot, please find my Ko-Fi link here: https://ko-fi.com/toast3y
        """
        await interaction.response.send_message(f"{textwrap.dedent(response)}")



##Cog for defining raw data exports, for use with Excel and other external programs.
class BlitzDataCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #fetchmatchdayplain command
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
                await interaction.response.send_message(f"A database connection could not be established. Please try again later.", ephemeral = True)
        else:
            await interaction.response.send_message(f"fetchmatchdayplain command requires a valid competition name and round", ephemeral = True)
            
            
    #matchdayplain command
    #@app_commands.command(name='matchdayplain', description='Return competition pairings in Plaintext for this channels registered league')
    #async def _matchdayplain(self, interaction: discord.Interaction):
    #    #TODO: Add functionality using server DB to specify data to return
    #    return


##Cog for configuring server settings and enabling functions on a per-guild basis    
class BlitzConfigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    #registerserver
    @app_commands.command(name='registerserver', description='Register your server with BlitzBot to enable advanced functionality')
    async def _registerserver(self, interaction: discord.Interaction):
        #await interaction.response.send_message("Admin task run. TEST.")
        conn = localDatabaseConnect()
        cursor = getCursor(conn)
        
        if(cursor != None):
            #await interaction.response.send_message(f"Database Connection Established")
            
            #Get details from the interaction
            discord_id = str(interaction.guild_id)
            server_name = interaction.guild.name
            #channel_id = interaction.channel_id
            #user_id = interaction.user.id
            
            #Check if the record exists, add it if not:
            if (blitzbot_config.getRegisterServer(cursor, discord_id) != None):
                await interaction.response.send_message(f"Error: This server is already registered with BlitzBot!")
            else:
                if (blitzbot_config.registerServer(cursor, discord_id, server_name) == True):
                    await interaction.response.send_message(f"Thanks for registering! Channel settings can now be configured.")
                    conn.commit()
                else:
                    await interaction.response.send_message(f"Error registering server at this time. Please try again later.")
                    conn.rollback()
            
            databaseDisconnect(cursor, conn)
            
        else:
            await interaction.response.send_message(f"Unable to contact BlitzBot Database. Please try again later.")
    
    
    
    
    #setchannelcomp
    @app_commands.command(name='setcompetition', description='Register this channel to a specific competition on Nuffle.xyz')
    async def _setcompetition(self, interaction: discord.Interaction, competition: str):
        if (competition != ""):
            #Check if competition is valid on Nuffle
            conn = databaseConnect()
            cursor = getCursor(conn)
            
            if(cursor != None):
                comp = blitzbot_config.getNuffleCompetition(cursor, competition)
                databaseDisconnect(cursor, conn)
                
                #Local database add if results are good.
                if(comp != None):
                    #Open connection, pass it to function, close connection
                    #localconn = localDatabaseConnect()
                    #localcursor = getCursor(localConn)
                    
                    #channel_id = interaction.channel_id
                    
                    #blitzbot_config.setChannelCompetition(localcursor, )
                    
                    #databaseDisconnect(localcursor, localconn)
                    
                    await interaction.response.send_message(comp)
                    
                    ##Validation
                else:
                    await interaction.response.send_message(f"Unable to find competition with associated name for pairing. Please check spelling of league and try again.")
            else:
                await interaction.response.send_message(f"Unable to contact Nuffle Database. Please try again later.")
        else:
            await interaction.response.send_message(f"setcompetition requires a valid Nuffle.xyz registered league")
    
    #removechannelcomp
    
    #settimezone
    
    
    



##Main class definition for Blitzbot, asynchronously adds cogs to expose slash commands
class BlitzBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents(messages=True, message_content=True, members=True, guilds=True))
        #self.tree = discord.app_commands.CommandTree(self)
		
    async def setup_hook(self) -> None:
        await self.add_cog(BlitzCog(self))
        await self.add_cog(BlitzDataCog(self))
        await self.add_cog(BlitzConfigCog(self))
        #await self.add_cog(BlitzScheduleCog(self))
        await self.add_cog(BlitzHelpCog(self))
        #await self.add_cog(BlitzAdminCog(self))
        
        ##Copy commands to development server first
        self.tree.copy_global_to(guild = discord.Object(id=GUILD_ID))
        await self.tree.sync()
        
        
        
		
client = BlitzBot()
	
client.run(TOKEN)