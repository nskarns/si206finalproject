import sqlite3
import http.client 
import json
import time
import matplotlib.pyplot as plt

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
        print(california_teams_dict) 

# Print the dictionary of California teams
#print("California Teams:", california_teams_dict)

# Create a dictionary with the number of players on each California team
all_players_data = []
for team_name, team_id in california_teams_dict.items(): 
    path = f"/players?country=USA&season=2021&team={team_id}"
    conn.request("GET", path, headers=headers) 
    res = conn.getresponse() 
    data = res.read()
    decoded_data = json.loads(data.decode('utf-8')) 
    players_data = decoded_data['response']
    #print(f"Team: {team_name}, Players Count: {len(players_data)}") 
    all_players_data.extend(players_data)
    print(all_players_data) 
    time.sleep(5)

# Function to create a dictionary for each player
def create_player_dict(player):
    if 'weight' not in player or 'height' not in player:
        #print(f"Skipping player {player['firstname']} {player['lastname']} (ID: {player['id']}) due to missing weight or height data")
        return None

    
    if player['height']['feets'] is None:
        group = 'None'
    elif int(player['height']['feets']) == 5 or (int(player['height']['feets']) == 6 and int(player['height']['inches']) <= 3):
        group = 'short (5ft9-6ft3)'
    elif int(player['height']['feets']) == 6 and int(player['height']['inches']) > 3 and int(player['height']['inches']) <= 7:
        group = 'medium (6ft4-6ft7)'
    else:
        group = 'tall (6ft7-7ft)'


    player_dict = {
        'id': player['id'],
        'full_name': f"{player['firstname']} {player['lastname']}",
        'team': player['affiliation'],
        'weight_pounds': player['weight']['pounds'],
        'height_feet': player['height']['feets'],
        'height_inches': player['height']['inches'],
        'height_group': group
    }
    return player_dict

# # Print the resulting list of player dictionaries
# for i, player_dict in enumerate(all_players_list):
#     if player_dict is not None:
#         pass
#         #print(f"Player {i + 1}: {player_dict}")

# #print(f"Total players in the list: {len(all_players_list)}")

conn.close() 

def set_up_tables(cursor,conn):
    # Create a table to store player information
    #cursor.execute('''DROP TABLE IF EXISTS weights''')
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weights (
            id INT,
            full_name TEXT,
            weight_pounds INT)
        """
    )  

    #cursor.execute('''DROP TABLE IF EXISTS heights'''
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS heights (
            id INT,
            full_name TEXT,
            height_feet INT,
            height_inches INT,
            height_group TEXT) 
        """
    )  

def fill_database(cursor,conn):
    cursor.execute(
        """
        SELECT id FROM weights
        """
    )
    player_list_length = len(cursor.fetchall()) 
# Insert player data into the weights table 
    for x in range(player_list_length,player_list_length+19):  
        #for player_dict in all_players_list: 
        if all_players_list[x] is not None: 
            cursor.execute(
                """
                INSERT INTO weights (id, full_name, weight_pounds)
                VALUES (?, ?, ?) 
                """,
            (
                all_players_list[x]['id'],
                all_players_list[x]['full_name'],
                all_players_list[x]['weight_pounds'] if all_players_list[x]['weight_pounds'] is not None else 'none',
            )) 
    
    # Insert player data into the heights table
        if all_players_list[x] is not None:
            cursor.execute(
                """
                INSERT INTO heights (id, full_name, height_feet, height_inches,height_group)
                VALUES (?, ?, ?, ?,?) 
                """,
            (
                all_players_list[x]['id'],
                all_players_list[x]['full_name'],
                all_players_list[x]['height_feet'] if all_players_list[x]['height_feet'] is not None else 'none',
                all_players_list[x]['height_inches'] if all_players_list[x]['height_inches'] is not None else 'none',
                all_players_list[x]['height_group'] if all_players_list[x]['height_group'] is not None else 'none' 
            )) 
    conn.commit() 


def visual_inputs(cursor,conn):
    # Group the data from the two charts, finding the average weight per height group, rounding to nearest whole number
    cursor.execute(
        """
        SELECT ROUND(AVG (weights.weight_pounds),0), heights.height_group 
        FROM weights JOIN heights
        ON weights.id = heights.id
        GROUP BY heights.height_group
        """
    )
    grouped_data = cursor.fetchall() 

    # Creating list for average
    height_range = ['short (5ft9-6ft3)', 'medium (6ft4-6ft7)', 'tall (6ft7-7ft)','None']
    another_height_range = ['None','short (5ft9-6ft3)', 'medium (6ft4-6ft7)', 'tall (6ft7-7ft)']

    # Printing results to a file
    with open("nba_weights_heights.txt", "w") as file:
            file.write("Average Weight Data (Height Range (ft. in.) - Average Weight (pds)):\n")
            for height, average_weight in zip(another_height_range, grouped_data):
                file.write(height + " - " + str(average_weight) + "\n")

    # Sort the data by height group
    grouped_data.sort(key=lambda x: height_range.index(x[1])) 

    #sorting data so x values and y values are together
    x_values = [] 
    y_values = [] 
    for w,h in grouped_data:
        if h != 'None':
            x_values.append(h)
            y_values.append(w)

    # Commit the changes and close the database connection
    db_connection.commit()
    db_connection.close()

db_connection = sqlite3.connect('database.db') 
cursor = db_connection.cursor() 
# Create a list of player dictionaries for all players
all_players_list = [create_player_dict(player) for player in all_players_data] 
set_up_tables(cursor,db_connection) 
fill_database(cursor,db_connection) 
#visual_inputs(cursor,conn) 