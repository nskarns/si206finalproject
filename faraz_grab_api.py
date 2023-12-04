import requests
import sqlite3
import os

def grab_PL_team_data(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    # Drop and recreate the Matches table with the correct structure
    cur.execute('''DROP TABLE IF EXISTS Matches''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Matches
                   (matchday INTEGER, team1_name TEXT, team2_name TEXT, team1_score INTEGER, team2_score INTEGER, winner TEXT)''')

    # URL for Premier League data
    url = "https://heisenbug-premier-league-live-scores-v1.p.rapidapi.com/api/premierleague"
    headers = {
        'X-RapidAPI-Key': 'dbd4417e6cmsh607185ee632316cp187ef6jsn1bee0e0113d0',
        'X-RapidAPI-Host': 'heisenbug-premier-league-live-scores-v1.p.rapidapi.com'
    }

    # Iterate through matchdays 1 to 14
    for matchday in range(1, 15):
        querystring = {"matchday": str(matchday)}
        response = requests.get(url, headers=headers, params=querystring)

        try:
            response.raise_for_status()
            data = response.json()

            for match in data.get('matches', []):
                team1_name = match['team1']['teamName']
                team2_name = match['team2']['teamName']
                team1_score = match['team1'].get('teamScore', None)
                team2_score = match['team2'].get('teamScore', None)

                # Determine the winner or mark as draw
                if team1_score is not None and team2_score is not None:
                    winner = team1_name if team1_score > team2_score else (team2_name if team2_score > team1_score else "Draw")
                else:
                    winner = None

                # Store match information in the Matches table
                cur.execute("INSERT INTO Matches VALUES (?, ?, ?, ?, ?, ?)", (matchday, team1_name, team2_name, team1_score, team2_score, winner))

            # Commit changes to the database after each matchday
            conn.commit()

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'Response text: {response.text}')

        except Exception as e:
            print(f'An error occurred: {e}')

    # Close the database connection
    conn.close()

# Call the function with the desired database path
grab_PL_team_data("premier_league_data.db")
