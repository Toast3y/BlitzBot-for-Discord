#Blitzbot Handler, for Blitzbot
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv

import discord


#def pingServer(cursor) -> str:
#    #query = "SELECT * FROM competitions_rounds INNER JOIN competitions ON competitions_rounds.competition_id = competitions.id WHERE competitions.name = %s LIMIT 3"
#    #query = """DESCRIBE competitions_leaderboards"""
#    query = """SELECT * FROM competitions_leaderboards
#        JOIN competitions ON competitions.id = competitions_leaderboards.competition_id
#        WHERE competitions.name = %s
#        LIMIT 2"""
#    leaguename="EireBB C1 S1 Div B"
#    cursor.execute(query, (leaguename))
#    
#    tables = cursor.fetchall()
#    print(tables)
#    
#    #Parse response as required
#    response = tables
#    
#    return response






#findTeam command query
#Finds a team from the provided team name, searches all of Nuffle
def findTeam(cursor, name):
    query = "SELECT name, rerolls, (SELECT name FROM coaches WHERE teams.coach_id = coaches.id), wins, draws, losses, value, cash, assistant_coaches, cheerleaders, IF('Apothecary' = 1, 'Yes', 'No') AS 'Apothecary', popularity, coach_id, id, (SELECT name FROM races WHERE teams.race_id = races.id) FROM teams WHERE name = %s"
    
    cursor.execute(query, name)
    
    if not cursor.rowcount:
        #response = "Error: Team \'" + name + "\' not found"
        
        response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', color =0xFF5733)
        #response.set_thumbnail(url='')
        response.add_field(name='', value="Unable to find team named " + str(name))
        
        response.set_footer(text='Powered by Nuffle.xyz')
        
        return response
    else:
        if cursor.rowcount > 1:
            #If more than one result, handle items
            #response = "Duplicate teams found. Handle it!"
            
            results = cursor.fetchall()
            i = 1
            
            response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', description="Multiple teams found, were you looking for:", color =0xFF5733)
            #response.set_thumbnail(url='')
            
            for result in results:
                coachLink = "http://nuffle.xyz/coaches/" + result[12]
                teamLink = "http://nuffle.xyz/teams/" + result[13]
                response.add_field(name='', value= str(i) + ". [" + str(result[0]) + "](" + teamLink + "), coached by: [" + str(result[2]) + "](" + coachLink + ")")
                i = i+1
                
            
            response.set_footer(text='Powered by Nuffle.xyz')
            
            return response
        else:
            result = cursor.fetchall()
            coachLink = "http://nuffle.xyz/coaches/" + result[0][12]
            teamLink = "http://nuffle.xyz/teams/" + result[0][13]
            
            
            #response = discord.Embed(title=result[0][0], url=teamLink, description=result[0][0] + ", powered by Nuffle.xyz", color =0xFF5733)
            #response.set_author(name='Nuffle.xyz', url='http://nuffle.xyz')
            response = discord.Embed(title=result[0][0], url=teamLink, color =0xFF5733)
            #response.set_thumbnail(url='')
            response.add_field(name='Coach:', value="[" + str(result[0][2]) +"]("+ coachLink + ")", inline=True)
            response.add_field(name='W-D-L:', value=str(result[0][3]) + '-' + str(result[0][4]) + '-' + str(result[0][5]), inline=True)
            response.add_field(name='', value='', inline=False)
            response.add_field(name='Race:', value=result[0][14], inline=True)
            response.add_field(name='Rerolls:', value=result[0][1], inline=True)
            response.add_field(name='--------', value='', inline=False)
            response.add_field(name='Team Value:', value=result[0][6], inline=True)
            response.add_field(name='Treasury:', value=result[0][7], inline=True)
            response.add_field(name='Ass. Coaches:', value=result[0][8], inline=True)
            response.add_field(name='Popularity:', value=result[0][11], inline=True)
            response.add_field(name='Apothecary:', value=result[0][10], inline=True)
            response.add_field(name='Cheerleaders:', value=result[0][9], inline=True)
            
            response.set_footer(text='Powered by Nuffle.xyz')
            
            
            return response
    
    
    
    
    
    

#FindCoach - Find a coach searching all of nuffle by name
def findCoach(cursor, name):
    query = "SELECT name, id, wins, draws, losses FROM coaches WHERE name = %s"
    
    cursor.execute(query, name)
    
    if not cursor.rowcount:
        #response = "Error: Coach \'" + name + "\' not found"
        
        response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', color =0xFF5733)
        response.add_field(name='', value="Unable to find Coach with name " + str(name))
        
        response.set_footer(text='Powered by Nuffle.xyz')
        
        return response
    else:
        if cursor.rowcount > 1:
            results = cursor.fetchall()
            i = 1
            
            ##TODO: Add more fields to help filter results in case of duplicate player names
            response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', description="Multiple coaches found, were you looking for:", color =0xFF5733)
            
            for result in results:
                coachLink = "http://nuffle.xyz/coaches/" + result[1]
                response.add_field(name='', value= str(i) + ". [" + str(result[0]) + "](" + teamLink + ")", inline = False)
                #response.add_field(name='W-D-L', value= str(result[2]) + "-" + str(result[3]) + "-" + str(result[4]), inline = True)
                i = i+1
            
            response.set_footer(text='Powered by Nuffle.xyz')
            
            return response
            
        else:
            result = cursor.fetchall()
            coachLink = "http://nuffle.xyz/coaches/" + result[0][1]
            
            response = discord.Embed(title= str(result[0][0]) + ", on Nuffle.xyz", url=coachLink, color =0xFF5733)
            #response.add_field(name='W-D-L', value= str(result[0][2]) + "-" + str(result[0][3]) + "-" + str(result[0][4]))
            response.add_field(name='', value="See the profile for " + str(result[0][0]) + " on Nuffle.xyz")
            response.set_footer(text='Powered by Nuffle.xyz')
            
            return response
        
    
    
    
    
    
#Fetch Matchday Fetch specific pairings from a given league    
def fetchMatchday(cursor, name, matchday):
    query = """SELECT competition_id, round, competitions.name, home_team_id, home_score, away_team_id, away_score, competitions_rounds.status, 
        hometeam.name, awayteam.name, homecoach.id, homecoach.name, awaycoach.id, awaycoach.name, competitions.created_at
        FROM competitions_rounds 
        JOIN competitions ON competitions_rounds.competition_id = competitions.id
        JOIN teams AS hometeam ON competitions_rounds.home_team_id = hometeam.id
        JOIN teams AS awayteam ON competitions_rounds.away_team_id = awayteam.id
        JOIN coaches AS homecoach ON hometeam.coach_id = homecoach.id
        JOIN coaches AS awaycoach ON awayteam.coach_id = awaycoach.id
        WHERE competitions.name = %s AND round = %s"""
    
    cursor.execute(query, (name, matchday))
    
    if not cursor.rowcount:
        response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', color =0xFF5733)
        #response.set_thumbnail(url='')
        response.add_field(name='', value="Unable to find matchday pairings for competition named " + str(name), inline= False)
        response.add_field(name='', value="Please ensure the spelling of the name is correct.", inline = False)
        response.set_footer(text='Powered by Nuffle.xyz')
        
        return response
    else:
        results = cursor.fetchall()
        #i = 1
        
        leagueLink = "http://nuffle.xyz/competition/" + results[0][0]
        
        response = discord.Embed(title="Round " + str(results[0][1]) + " pairings for " + str(results[0][2]), url=leagueLink, color=0xFF5733)
        response.add_field(name='', value="Pairings for round " + str(results[0][1]) + ":", inline = False)
        
        for result in results:
            hometeam_link = "http://nuffle.xyz/teams/" + result[3]
            awayteam_link = "http://nuffle.xyz/teams/" + result[5]
            homecoach_link = "http://nuffle.xyz/coaches/" + result[10]
            awaycoach_link = "http://nuffle.xyz/coaches/" + result[12]
            
            #Home team
            response.add_field(name=str(result[8]), value="[" + str(result[11]) + "](" + homecoach_link + ")", inline = True)
            
            #Spacer
            #if match hasn't been played or scores aren't up to date, display VS instead
            
            if (result[7] != 'validated'):
                #docombo
                response.add_field(name="VS", value="", inline = True)
            else:
                #docombo
                response.add_field(name= str(result[4]) +  " - " + str(result[6]), value="", inline = True)
                
            
            #AwayTeam
            response.add_field(name=str(result[9]), value="[" + str(result[13]) + "](" + awaycoach_link + ")", inline = True)
        
        response.set_footer(text='Powered by Nuffle.xyz')
            
        return response
        
        
        
        
#fetchStandings - Return a standings table for any league by name.
def fetchStandings(cursor, name):
    query = """SELECT competition_id, team_id, points, competitions_leaderboards.wins, competitions_leaderboards.draws, competitions_leaderboards.losses, teams.name, teams.coach_id, coaches.name FROM competitions_leaderboards
        JOIN competitions ON competitions.id = competitions_leaderboards.competition_id
        JOIN teams ON competitions_leaderboards.team_id = teams.id
        JOIN coaches ON teams.coach_id = coaches.id
        WHERE competitions.name = %s
        ORDER BY points DESC
        LIMIT 4"""
    cursor.execute(query, name)
    
    if not cursor.rowcount:
        response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', color =0xFF5733)
        #response.set_thumbnail(url='')
        response.add_field(name='', value="Unable to find standings for competition named " + str(name), inline= False)
        response.add_field(name='', value="Please ensure the spelling of the name is correct.", inline = False)
        response.set_footer(text='Powered by Nuffle.xyz')
        return response
    else:
        results = cursor.fetchall()
        i = 1
        
        leagueLink = "http://nuffle.xyz/competition/" + results[0][0]
        
        response = discord.Embed(title= str(name) + " Standings", url=leagueLink, color=0xFF5733)
        response.add_field(name='', value="Current Top 4 Standings for " + str(name) + ":", inline = False)
        
        for result in results:
            coachlink = "http://nuffle.xyz/coaches/" + result[7]
            teamlink = "http://nuffle.xyz/teams/" + result[1]
            
            response.add_field(name= str(i) + ". " + result[6], value = "[" + str(result[8]) + "](" + coachlink + ")", inline = True)
            response.add_field(name= "POINTS", value=str(result[2]), inline = True)
            response.add_field(name= "W-D-L", value=str(result[3]) + "-" + str(result[4]) + "-" + str(result[5]), inline = True)
            
            i = i+1
            
        response.set_footer(text='See the full table at Nuffle.xyz')
        
        return response
        
        
        
        
        
######## USER FRIENDLY QUERIES ########
#Most are copied and adapted from above code.



#Standings - Fetch standings using the paired channel and league IDs
def standings(cursor, league_id):
    query = """SELECT competition_id, team_id, points, competitions_leaderboards.wins, competitions_leaderboards.draws, competitions_leaderboards.losses, teams.name, teams.coach_id, coaches.name, competitions.name FROM competitions_leaderboards
        JOIN competitions ON competitions.id = competitions_leaderboards.competition_id
        JOIN teams ON competitions_leaderboards.team_id = teams.id
        JOIN coaches ON teams.coach_id = coaches.id
        WHERE competition_id = %s
        ORDER BY points DESC
        LIMIT 4"""
    cursor.execute(query, league_id)
    
    if not cursor.rowcount:
        response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', color =0xFF5733)
        #response.set_thumbnail(url='')
        response.add_field(name='', value="Unable to find standings for competition paired in this channel.", inline= False)
        response.add_field(name='', value="Please contact a league administrator.", inline = False)
        response.set_footer(text='Powered by Nuffle.xyz')
        return response
    else:
        results = cursor.fetchall()
        i = 1
        
        leagueLink = "http://nuffle.xyz/competition/" + results[0][0]
        
        response = discord.Embed(title= str(results[0][9]) + " Standings", url=leagueLink, color=0xFF5733)
        response.add_field(name='', value="Current Top 4 Standings for " + str(results[0][9]) + ":", inline = False)
        
        for result in results:
            coachlink = "http://nuffle.xyz/coaches/" + result[7]
            teamlink = "http://nuffle.xyz/teams/" + result[1]
            
            response.add_field(name= str(i) + ". " + result[6], value = "[" + str(result[8]) + "](" + coachlink + ")", inline = True)
            response.add_field(name= "POINTS", value=str(result[2]), inline = True)
            response.add_field(name= "W-D-L", value=str(result[3]) + "-" + str(result[4]) + "-" + str(result[5]), inline = True)
            
            i = i+1
            
        response.set_footer(text='See the full table at Nuffle.xyz')
        
        return response
        
        
        
        
        
#Matches - Return the pairings that aren't predictions, fetch the most recent matchday, and return them as the match fixings        
def matches(cursor, league_id):
    query = """SELECT competition_id, round, competitions.name, home_team_id, home_score, away_team_id, away_score, competitions_rounds.status, 
        hometeam.name, awayteam.name, homecoach.id, homecoach.name, awaycoach.id, awaycoach.name, competitions.created_at
        FROM competitions_rounds 
        JOIN competitions ON competitions_rounds.competition_id = competitions.id
        JOIN teams AS hometeam ON competitions_rounds.home_team_id = hometeam.id
        JOIN teams AS awayteam ON competitions_rounds.away_team_id = awayteam.id
        JOIN coaches AS homecoach ON hometeam.coach_id = homecoach.id
        JOIN coaches AS awaycoach ON awayteam.coach_id = awaycoach.id
        WHERE competition_id = %s AND is_prediction = false"""
    
    cursor.execute(query, league_id)
    
    #Iterate through results if they're returned
    if not cursor.rowcount:
        response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', color =0xFF5733)
        #response.set_thumbnail(url='')
        response.add_field(name='', value="Unable to find matchday pairings for paired competition in this channel.", inline= False)
        response.add_field(name='', value="Please contact an admin if this issue persists.", inline = False)
        response.set_footer(text='Powered by Nuffle.xyz')
        
        return response
    else:
        
        results = cursor.fetchall()
        
        matchday = 0
        
        #figure out the current pairings based on is_prediction flag
        for result in results:
            if result[1] > matchday:
                matchday = result[1]
                
        pairings = []
        
        #Build list of results to append to embed
        for result in results:
            if result[1] == matchday:
                pairings.append(result)
            
        
        #i = 1
        
        leagueLink = "http://nuffle.xyz/competition/" + pairings[0][0]
        
        response = discord.Embed(title="Round " + str(pairings[0][1]) + " pairings for " + str(pairings[0][2]), url=leagueLink, color=0xFF5733)
        response.add_field(name='', value="Pairings for round " + str(pairings[0][1]) + ":", inline = False)
        
        for result in pairings:
            hometeam_link = "http://nuffle.xyz/teams/" + result[3]
            awayteam_link = "http://nuffle.xyz/teams/" + result[5]
            homecoach_link = "http://nuffle.xyz/coaches/" + result[10]
            awaycoach_link = "http://nuffle.xyz/coaches/" + result[12]
            
            #Home team
            response.add_field(name=str(result[8]), value="[" + str(result[11]) + "](" + homecoach_link + ")", inline = True)
            
            #Spacer
            #if match hasn't been played or scores aren't up to date, display VS instead
            
            if (result[7] != 'validated'):
                #docombo
                response.add_field(name="VS", value="", inline = True)
            else:
                #docombo
                response.add_field(name= str(result[4]) +  " - " + str(result[6]), value="", inline = True)
                
            
            #AwayTeam
            response.add_field(name=str(result[9]), value="[" + str(result[13]) + "](" + awaycoach_link + ")", inline = True)
        
        response.set_footer(text='Powered by Nuffle.xyz')
            
        return response