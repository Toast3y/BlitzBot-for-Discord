#Blitzbot Data, for Blitzbot
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv

#Data only returns for easy parsing with external programs, such as Excel

import discord

def fetchMatchday_data(cursor, name, matchday):
    
    query = """SELECT competition_id, round, competitions.name, home_team_id, away_team_id, 
        hometeam.name, awayteam.name, homecoach.id, homecoach.name, awaycoach.id, awaycoach.name
        FROM competitions_rounds 
        JOIN competitions ON competitions_rounds.competition_id = competitions.id
        JOIN teams AS hometeam ON competitions_rounds.home_team_id = hometeam.id
        JOIN teams AS awayteam ON competitions_rounds.away_team_id = awayteam.id
        JOIN coaches AS homecoach ON hometeam.coach_id = homecoach.id
        JOIN coaches AS awaycoach ON awayteam.coach_id = awaycoach.id
        WHERE competitions.name = %s AND round = %s"""
    
    cursor.execute(query, (name, matchday))
    
    if not cursor.rowcount:
        #No results found, return that to the end user
        response = "No results were returned for league " + name + ".\nDouble check details are correct and try again."
        return response
    else:
        #Iterate over results and add data to response
        results = cursor.fetchall()
        i = 1
        response = "Matchday " + str(matchday) + " for league " + name + ":\n\n"
        
        for result in results:
            response = response + (str("MD" + str(matchday) + "/" + str(i) + ": " + result[8] + " vs " + result[10] + "\n"))
            i=i+1
        
        return response