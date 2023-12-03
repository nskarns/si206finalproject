import requests
import sqlite3

url = "https://heisenbug-premier-league-live-scores-v1.p.rapidapi.com/api/premierleague"
headers = {
    'X-RapidAPI-Key': 'dbd4417e6cmsh607185ee632316cp187ef6jsn1bee0e0113d0',
    'X-RapidAPI-Host': 'heisenbug-premier-league-live-scores-v1.p.rapidapi.com'
}

# Connect to the SQLite database
conn = sqlite3.connect("premier_league_data.db")
cur = conn.cursor()

# Create a table for match information
cur.execute('''CREATE TABLE IF NOT EXISTS Matches
               (matchday INTEGER, team1_name TEXT, team2_name TEXT, team1_score INTEGER, team2_score INTEGER)''')

# Create a table for team wins
cur.execute('''CREATE TABLE IF NOT EXISTS TeamWins
               (team_name TEXT, wins INTEGER)''')

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

            # Check if 'teamScore' key exists for both teams
            if 'teamScore' in match['team1']:
                team1_score = match['team1']['teamScore']
            else:
                team1_score = None

            if 'teamScore' in match['team2']:
                team2_score = match['team2']['teamScore']
            else:
                team2_score = None

            # Store match information in the Matches table
            cur.execute("INSERT INTO Matches VALUES (?, ?, ?, ?, ?)", (matchday, team1_name, team2_name, team1_score, team2_score))

            # Update team wins in the TeamWins table
            if team1_score is not None and team2_score is not None:
                if team1_score > team2_score:
                    cur.execute("INSERT OR IGNORE INTO TeamWins VALUES (?, 0)", (team1_name,))
                    cur.execute("UPDATE TeamWins SET wins = wins + 1 WHERE team_name = ?", (team1_name,))
                elif team2_score > team1_score:
                    cur.execute("INSERT OR IGNORE INTO TeamWins VALUES (?, 0)", (team2_name,))
                    cur.execute("UPDATE TeamWins SET wins = wins + 1 WHERE team_name = ?", (team2_name,))

        # Commit changes to the database after each matchday
        conn.commit()

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(f'Response text: {response.text}')

    except Exception as e:
        print(f'An error occurred: {e}')

# Close the database connection
conn.close()
