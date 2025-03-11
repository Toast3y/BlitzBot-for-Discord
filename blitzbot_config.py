#Blitzbot Handler, for Blitzbot
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv

import discord

#registerserver command, adds a server to the configuration database for further customization
def registerServer(cursor, guild_id, guild_name):
    query = "INSERT INTO guilds (discord_id, server_name) VALUES (%s, %s)"
        
    #cursor.execute(query, (guild_id, guild_name))
    #return True
    
    try:
        cursor.execute(query, (guild_id, guild_name))
        return True
    except:
        print(f'Error registering server ' + guild_name + ' with id: ' + guild_id)
        return False
    
    
    
#Set a channel and store the data so user queries against Nuffle default to user-friendly options
def setChannelCompetition(cursor, guild_id, discord_id, channel_id, league_id):
    #Guild Validation is done ahead of time, so check if the channel is already registered
    #If it is, update the old record. If it isn't, insert it.
    
    if (getChannelCompetition(cursor, channel_id) != None):
        #Update record
        
        query = "UPDATE channel_leagues SET league_id = %s WHERE channel_id = %s"
        try:
            cursor.execute(query, (league_id, channel_id))
            return True
        except:
            print(f'Error updating channel to league ' + league_id + ' on channel ' + channel_id + ' and guild ' + guild_id)
            return False
    else:
        #Insert record
        
        query = "INSERT INTO channel_leagues (guild_id, discord_id, channel_id, league_id) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (guild_id, discord_id, channel_id, league_id))
            return True
        except:
            print(f'Error registering channel to league ' + league_id + ' on channel ' + channel_id + ' and guild ' + guild_id)
            return False

#Clear a channels competition so it can be set via setChannelCompetition
#def clearChannelCompetition(cursor):
#    return
    
    

#check if a server is registered for error handling. Returns the guild_id if registered, or None if not.
def getRegisterServer(cursor, guild_id):
    query = """SELECT id, discord_id FROM guilds
        WHERE discord_id = %s"""
        
    cursor.execute(query, (guild_id))
    
    if not cursor.rowcount:
        return None
    else:
        results = cursor.fetchall()
        return results [0]
        

    
#Check if a server channel is registered for returning leagues. Returns the associated ID, or None if not registered
def getChannelCompetition(cursor, channel_id):
    query = """SELECT channel_id FROM channel_leagues WHERE channel_id = %s"""
    
    cursor.execute(query, (channel_id))
    
    if not cursor.rowcount:
        return None
    else:
        results = cursor.fetchall()
        return results [0][0]
        
        
#Check on Nuffle if a competition exists. Return the ID if true, None if not.        
def getNuffleCompetition(cursor, name):
    query = """SELECT id FROM competitions WHERE name = %s"""
    
    cursor.execute(query, name)
    
    if not cursor.rowcount:
        return None
    else:
        results = cursor.fetchall()
        return results[0][0]
    