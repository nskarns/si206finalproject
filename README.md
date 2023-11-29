# SI 206 Final Project
Public API Links: https://github.com/public-apis/public-apis

# API #2 TODO List
1. Create a table in the database.
2. Grab API data and insert more than 100 lines of data into the table.
3. Calculate some data. Output this to text file.
4. Create graph of calculated data.

# API #3 TODO List
1. Create two tables in the database.
2. Grab API data and insert more than 100 lines of data into each table. Each table must have a similiar INT column. 
   If you're confused on this, please refer to Discussion #12.
3. Calculate some data based on their shared INT column. Output this to text file.
4. Create graph of calculated data.

# CREATE YOUR OWN FILES FOR THIS PROJECT
Please create your own files for this project. This is so we don't overlap. I will merge them at the end to condense our project.

# Database Information
We are all saving and grabbing our data to the same database. In order to set up a connection to save and grab data, use the three lines of code below.

path = os.path.dirname(os.path.abspath("database.db"))
conn = sqlite3.connect(path + "/" + "database.db")
cur = conn.cursor()

# grab_api.py
This is the code I used to grab data from an API. Feel free to use it as a guide when creating your own. 
