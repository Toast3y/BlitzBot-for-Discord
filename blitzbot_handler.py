#Blitzbot Handler, for Blitzbot
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv

import discord


def pingServer(cursor) -> str:
    cursor.execute("DESCRIBE races")
    tables = cursor.fetchall()
    #print(tables)
    
    #Parse response as required
    response = tables
    
    return response




def findTeam(cursor, name):
    query = "SELECT name, rerolls, (SELECT name FROM coaches WHERE teams.coach_id = coaches.id), wins, draws, losses, value, cash, assistant_coaches, cheerleaders, IF('Apothecary' = 1, 'Yes', 'No') AS 'Apothecary', popularity, coach_id, id, (SELECT name FROM races WHERE teams.race_id = races.id) FROM teams WHERE name = %s"
    
    cursor.execute(query, name)
    
    if not cursor.rowcount:
        response = "Error: Team \'" + name + "\' not found"
        return response
    else:
        if cursor.rowcount > 1:
            #If more than one result, handle items
            response = "Duplicate teams found. Handle it!"
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
            
            #Massage data and response here
            #response = result
            
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
    
    


def findCoach(cursor, name) -> str:
    query = "SELECT * FROM coaches WHERE name = %s"
    
    cursor.execute(query, name)
    
    if not cursor.rowcount:
        response = "Error: Coach \'" + name + "\' not found"
        return response
    else:
        result = cursor.fetchall()
        
        
        #Massage data and response here
        response = result
        
        return response
    
    