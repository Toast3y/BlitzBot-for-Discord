#Blitzbot Handler, for Blitzbot
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv


def pingServer(cursor) -> str:
    cursor.execute("DESCRIBE teams")
    tables = cursor.fetchall()
    #print(tables)
    
    #Parse response as required
    response = tables
    
    return response




def findTeam(cursor, name) -> str:
    query = "SELECT name, rerolls, (SELECT name FROM coaches WHERE teams.coach_id = coaches.id), wins, draws, losses, value, cash, assistant_coaches, cheerleaders, IF('Apothecary' = 1, 'Yes', 'No') AS 'Apothecary', popularity, coach_id, id FROM teams WHERE name = %s"
    
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
            coachLink = "nuffle.xyz/coaches/" + result[0][12]
            teamLink = "nuffle.xyz/teams/" + result[0][13]
            
            response = "Team Name: {} \t\t\t\tRerolls: {}" \
                    "\nCoach: [{}]({}) \t\t\t\tW-D-L: {}-{}-{}" \
                    "\n\nTeam Value: {} \t\t\t\tTreasury: {}" \
                    "\nAss. Coaches: {} \t\t\t\tCheerleaders: {}" \
                    "\nApothecary: {} \t\t\t\tPopularity: {}" \
                    "\n\nLink: [{}]({})".format(result[0][0], result[0][1], result[0][2], coachLink, result[0][3], result[0][4], result[0][5], result[0][6], result[0][7], result[0][8], result[0][9], result[0][10], result[0][11], result[0][0], teamLink)
            
            #Massage data and response here
            #response = result
            
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
    
    