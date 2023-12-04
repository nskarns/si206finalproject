import sqlite3
import http.client 
import json
import time

conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")
headers = {
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
    'x-rapidapi-key': "59046531c4mshc0feae1efa80a4fp127b15jsn761d45cd0f18" 
}

# Get the list of NBA teams
conn.request("GET", "/teams?league=standard", headers=headers)
res = conn.getresponse()
data = res.read()
decoded_data = json.loads(data.decode('utf-8'))
teams = decoded_data['response']

# Create a dictionary with California teams and their team ID
california_teams_dict = {}
for team in teams: 
    if team['nbaFranchise'] and team['id'] in [11, 16, 17, 30]:
        team_id = team['id']
        team_name = team['name'] 
        california_teams_dict[team_name] = team_id

# Print the dictionary of California teams
print("California Teams:", california_teams_dict)

# Create a dictionary with the number of players on each California team
all_players_data = []
for team_name, team_id in california_teams_dict.items(): 
    path = f"/players?country=USA&season=2021&team={team_id}"
    conn.request("GET", path, headers=headers) 
    res = conn.getresponse() 
    data = res.read()
    decoded_data = json.loads(data.decode('utf-8')) 
    players_data = decoded_data['response']
    print(f"Team: {team_name}, Players Count: {len(players_data)}") 
    all_players_data.extend(players_data)
    time.sleep(5)

# Function to create a dictionary for each player
def create_player_dict(player):
    if 'weight' not in player or 'height' not in player:
        print(f"Skipping player {player['firstname']} {player['lastname']} (ID: {player['id']}) due to missing weight or height data")
        return None

    player_dict = {
        'id': player['id'],
        'full_name': f"{player['firstname']} {player['lastname']}",
        'team': player['affiliation'],
        'weight_pounds': player['weight']['pounds'],
        'height_feet': player['height']['feets'],
        'height_inches': player['height']['inches']
    }
    return player_dict

# Create a list of player dictionaries for all players
all_players_list = [create_player_dict(player) for player in all_players_data]

# Print the resulting list of player dictionaries
for i, player_dict in enumerate(all_players_list):
    if player_dict is not None:
        print(f"Player {i + 1}: {player_dict}")

print(f"Total players in the list: {len(all_players_list)}")

conn.close()

# Connect to SQLite database (this will create a new file 'nba_players.db' if it doesn't exist)
db_connection = sqlite3.connect('nba_players.db')
cursor = db_connection.cursor()

# Create a table to store player information
cursor.execute('''DROP TABLE IF EXISTS weights''')
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS weights (
        id INT,
        full_name TEXT,
        weight_pounds INT)
    """
)  

cursor.execute('''DROP TABLE IF EXISTS heights''')
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS heights (
        id INT,
        full_name TEXT,
        height_feet INT,
        height_inches INT)
    """
)  

# Insert player data into the weights table
for player_dict in all_players_list:
    if player_dict is not None:
        cursor.execute(
            """
            INSERT INTO weights (id, full_name, weight_pounds)
            VALUES (?, ?, ?)
            """,
        (
            player_dict['id'],
            player_dict['full_name'],
            player_dict['weight_pounds'] if player_dict['weight_pounds'] is not None else 'none',
        )) 
    
# Insert player data into the heights table
for player_dict in all_players_list:
    if player_dict is not None:
        cursor.execute(
            """
            INSERT INTO heights (id, full_name, height_feet, height_inches)
            VALUES (?, ?, ?, ?)
            """,
        (
            player_dict['id'],
            player_dict['full_name'],
            player_dict['height_feet'] if player_dict['height_feet'] is not None else 'none',
            player_dict['height_inches'] if player_dict['height_inches'] is not None else 'none',
        )) 

# Commit the changes and close the database connection
db_connection.commit()
db_connection.close()

print("Data inserted into the SQLite database.")


#TODO
#create table for players, playerid, weight, team 
#create table for players, playerid, height, team
#calculate average weight per team 
#calculate average hight per team 
#create a bar graph with average weights and heights per team