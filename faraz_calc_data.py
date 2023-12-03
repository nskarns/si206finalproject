import sqlite3
import matplotlib.pyplot as plt

def calculate_average_goals(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    try:
        # Create a dictionary to store total goals and match counts for each team
        team_stats = {}

        # Query to get total goals and match counts for each team
        query = '''
                SELECT team_name, 
                       SUM(total_goals) AS total_goals, 
                       COUNT(*) AS match_count
                FROM (
                    SELECT team1_name AS team_name, team1_score AS total_goals FROM Matches
                    UNION ALL
                    SELECT team2_name AS team_name, team2_score AS total_goals FROM Matches
                )
                GROUP BY team_name
                '''

        cur.execute(query)
        rows = cur.fetchall()

        # Populate the team_stats dictionary with team_name as key
        # and total goals, match count as values
        for row in rows:
            team_name, total_goals, match_count = row
            team_stats[team_name] = {'total_goals': total_goals, 'match_count': match_count}

        return team_stats

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        # Close the database connection
        conn.close()


#####################################################################################################################################

# Function to create a bar chart
def create_average_goals_chart(database_path):
    # Call the calculate_average_goals function
    team_stats = calculate_average_goals(database_path)

    try:
        # Check if team_stats is not empty before creating the chart
        if team_stats:
            # Create a bar chart
            plt.bar(team_stats.keys(), [stats['total_goals'] / stats['match_count'] for stats in team_stats.values()])
            plt.xlabel('Team')
            plt.ylabel('Average Goals')
            plt.title('Average Goals per Team')
            plt.xticks(rotation=45, ha='right')
            plt.show()

        else:
            print("No data available for the chart.")

    except Exception as e:
        print(f'An error occurred: {e}')

# Example usage
create_average_goals_chart("premier_league_data.db")
