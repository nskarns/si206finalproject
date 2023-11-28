import requests
import os
import sqlite3

# Grabbing data
def grab_police_data(conn, cur):
    # Declaring variables
    city_ids = []

    # Deleting database
    cur.execute(
        "DROP TABLE IF EXISTS Police"
    )

    # Creating database
    cur.execute(
            "CREATE TABLE Police (city_id, name, rank)"
    )

    # Getting city ids
    response = requests.get("https://data.police.uk/api/leicestershire/neighbourhoods")
    data = response.json()
    for city in data:
        city_ids.append(city['id'])

    # Grabbing people for each city
    for city_id in city_ids:
        response = requests.get("https://data.police.uk/api/leicestershire/" + city_id + "/people")
        data = response.json()

        for people in data:
            cur.execute(
                "INSERT OR IGNORE INTO Police (city_id, name, rank) VALUES (?,?,?)", (city_id, people["name"], people["rank"])
            )
        
        conn.commit()

# Declaring variables
path = os.path.dirname(os.path.abspath("database.db"))
conn = sqlite3.connect(path + "/" + "database.db")
cur = conn.cursor()

# Call function
grab_police_data(conn, cur)