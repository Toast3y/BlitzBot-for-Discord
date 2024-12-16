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

class BlitzCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name='ping', description='Test ping pong')
    async def _ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong")
        
    @app_commands.command(name='findcoach', description='Find a Coach on Nuffle.xyz')
    async def _findCoach(self, interaction: discord.Interaction, coach: str):
        await interaction.response.send_message("Finding player. TEST.")
        
    @app_commands.command(name='findteam', description='Find a Team on Nuffle.xyz')
    async def _findTeam(self, interaction: discord.Interaction, team: str):
        await interaction.response.send_message("Finding Team. TEST.")
        
    @app_commands.command(name='schedulematch', description='Set a reminder for your match, pinging you and your specified opponent.')
    async def _scheduleMatch(self, interaction: discord.Interaction, opponent: discord.Member):
        await interaction.response.send_message("Scheduled match. TEST.")
        
        
#class BlitzAdminCog(commands.Cog):
#    def __init__(self, bot: commands.Bot):
#        self.bot = bot
#        
#    @app_commands.command(name='admintask', description='Admin test adding a cog', guild_ids = GUILD_ID)
#    async def _adminTask(self, interaction: discord.Interaction):
#        await interaction.response.send_message("Admin task run. TEST.")
#        

class BlitzBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents(messages=True, message_content=True, members=True, guilds=True))
        #self.tree = discord.app_commands.CommandTree(self)
		
    async def setup_hook(self) -> None:
        await self.add_cog(BlitzCog(self))
        #await self.add_cog(BlitzAdminCog(self))
        self.tree.copy_global_to(guild = discord.Object(id=GUILD_ID))
        await self.tree.sync()
        
        
        
		
client = BlitzBot()
	
client.run(TOKEN)