import os
import sqlite3
import matplotlib.pyplot as plt

# Calculating average number of positions per town
def calculate_police_avg(conn, cur):
    # Declaring variables
    job_list = ["", "Sergeant", "PCSO", "Police Constable", "PC", "Inspector", "SGT", "Other"]
    job_nums = []

    # Grabbing All Sergeants
    for job in job_list:
        cur.execute (
            "SELECT name, rank "
            "FROM Police "
            "WHERE rank LIKE ? ",
            ('%' + job + '%',)
        )
        data = cur.fetchall()
        job_nums.append(len(data))
        
    # Removing PCSO from PC
    job_nums[4] -= job_nums[2]

    # Calculating Other Jobs
    other = job_nums[0] * 2
    for job in job_nums:
        other -= job
    job_nums[7] = other

    # Resetting value for output
    job_list[0] = "Total"

    # Outputting data to file
    with open("police_job_data.txt", "w") as file:
        file.write("Police Job Data (job title - total):\n")
        for job_title, job_count in zip(job_list, job_nums):
            file.write(job_title + " - " + str(job_count) + "\n")

    # Return
    return (job_list[1:], job_nums[1:])

# Creating graph for total police jobs
def create_police_graph(results):
    # Plotting
    plt.figure(figsize=(10, 8))

    # Getting subplots
    fig, ax = plt.subplots()

    # Creating graph
    ax.bar(results[0], results[1], align="center")

    # Other graph settings
    plt.xlabel("Type Of Job")
    plt.ylabel("Total For Job")
    plt.title("Totals For Each Jobs In UK Neighborhoods")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Saving results
    plt.savefig('police_job_data.png')  

# Declaring variables
path = os.path.dirname(os.path.abspath("database.db"))
conn = sqlite3.connect(path + "/" + "database.db")
cur = conn.cursor()

# Call calcuation function
results = calculate_police_avg(conn, cur)

# Call create graph
create_police_graph(results)