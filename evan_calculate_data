import sqlite3
import http.client 
import json
import time
import matplotlib.pyplot as plt

def calculate_and_graph(cursor,conn):
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
    conn.commit()
    conn.close() 

    #Create graph to find avergae weight from (5'9-6'3)(6'3-6'7)(6'7-7'0) 
    #Y axis is weight and x axis is height
    # Plotting
    plt.figure(figsize=(10, 8))
    # Getting subplots
    fig, ax = plt.subplots()
    # Creating graph
    ax.bar(x_values, y_values, align="center") 
    # Other graph settings
    plt.xlabel("Player Height Group")
    plt.ylabel("Average Weight")
    plt.ylim(150,250) 
    plt.title("Average Weight Per Height Group For California NBA Teams 2021 Season") 
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Saving results
    plt.savefig('nba_weights_heights.png') 
    plt.show() 

db_connection = sqlite3.connect('nba_players.db') 
cursor = db_connection.cursor() 
calculate_and_graph(cursor,db_connection) 