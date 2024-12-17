#Blitzbot Handler, for Blitzbot
# Written  by Toast3y, aka Chris Dunne
# Influenced by Spike bot, written by Poncho_dlv


def pingServer(cursor) -> str:
    cursor.execute("DESCRIBE coaches")
    tables = cursor.fetchall()
    #print(tables)
    
    #Parse response as required
    response = tables
    
    return response

def findTeam():
    return response
    
def findCoach(cursor, name):
    query = "SELECT * FROM coaches WHERE name = %s"
    
    cursor.execute(query, name)
    result = cursor.fetchall()
    
    #Massage data and response here
    response = result
    
    return response