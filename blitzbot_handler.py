#Blitzbot Handler, for Blitzbot
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv

import discord


def pingServer(cursor) -> str:
    #query = "SELECT * FROM competitions_rounds INNER JOIN competitions ON competitions_rounds.competition_id = competitions.id WHERE competitions.name = %s LIMIT 3"
    query = """SELECT competition_id, round, home_team_id, home_score, away_team_id, away_score, competitions_rounds.status, 
        hometeam.name, awayteam.name, homecoach.id, homecoach.name, awaycoach.id, awaycoach.name
        FROM competitions_rounds 
        JOIN competitions ON competitions_rounds.competition_id = competitions.id
        JOIN teams AS hometeam ON competitions_rounds.home_team_id = hometeam.id
        JOIN teams AS awayteam ON competitions_rounds.away_team_id = awayteam.id
        JOIN coaches AS homecoach ON hometeam.coach_id = homecoach.id
        JOIN coaches AS awaycoach ON awayteam.coach_id = awaycoach.id
        WHERE competitions.name = %s AND round = %s"""
    leaguename="EireBB C1 S1 Div B"
    cursor.execute(query, (leaguename, 4))
    
    tables = cursor.fetchall()
    print(tables)
    
    #Parse response as required
    response = tables
    
    return response







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
            
            #response = "Team Name: {} \t\t\t\tRerolls: {}" \
            #        "\nCoach: [{}]({}) \t\t\t\tW-D-L: {}-{}-{}" \
            #        "\n\nTeam Value: {} \t\t\t\tTreasury: {}" \
            #        "\nAss. Coaches: {} \t\t\t\tCheerleaders: {}" \
            #        "\nApothecary: {} \t\t\t\tPopularity: {}" \
            #        "\n\nLink: [{}]({})".format(result[0][0], result[0][1], result[0][2], coachLink, result[0][3], result[0][4], result[0][5], result[0][6], result[0][7], result[0][8], result[0][9], result[0][10], result[0][11], result[0][0], teamLink)
            
            
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
    
    
    
    
    
    


def findCoach(cursor, name, matchday):
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
            response.add_field(name='', value="See the profile for" + str(result[0][0]) + " on Nuffle.xyz")
            response.set_footer(text='Powered by Nuffle.xyz')
            
            return response
        
    
    
    
    
    
    
def fetchMatchday(cursor, name, matchday):
    query = """SELECT competition_id, round, competitions.name, home_team_id, home_score, away_team_id, away_score, competitions_rounds.status, 
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
        response = discord.Embed(title='Nuffle.xyz', url='http://nuffle.xyz', color =0xFF5733)
        #response.set_thumbnail(url='')
        response.add_field(name='', value="Unable to find matchday pairings for competition named " + str(name), inline= False)
        response.add_field(name='', value="Please ensure the spelling of the name is correct.", inline = False)
        response.set_footer(text='Powered by Nuffle.xyz')
        
        return response
    else:
        results = cursor.fetchall()
        i = 1
        
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
        
        
        
        
    
def fetchStandings(cursor, name):
    query = "WHERE name = %s"
    cursor.execute(query, name)
    
    if not cursor.rowcount:
        return response
    else:
        if cursor.rowcount > 1:
            return response
        else:
            return response