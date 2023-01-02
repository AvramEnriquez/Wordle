import psycopg2
import plotext as plt
from wordle import wordle

"""CONNECTING TO DATABASE"""
# Insert database name, username, password, server address, and port here
DB_NAME = ('postgres')
DB_USER = ('postgres')
DB_PASS = ('')
DB_HOST = ('localhost')
DB_PORT = ('5432')

table_name = 'wordle_stats'

try:
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT)
    print("\nDatabase connected successfully!")
except:
    print("Database failed to connect.")

try:
    # Create a cursor
    cur = conn.cursor()

    # Execute query to create table
    cur.execute(f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY NOT NULL,
            "tries" INT,
            "win" BOOLEAN,
            "streak" BOOLEAN
        );
        """)
    print(f"Table {table_name} created successfully.")
except psycopg2.errors.DuplicateTable:
    # State if table already exists
    print(f"Table {table_name} already exists.")
conn.commit()  # Commit the change

"""Functions to play game or see stats"""
def play():
    tries, win, streak = wordle()

    cur.execute(f"""
        INSERT INTO wordle_stats (
            tries, 
            win,
            streak
        )
        VALUES (
            {tries}, 
            {win},
            {streak}
        );
        """)

    # If streak is set to False, will clear streak column in database
    if streak == False:
        cur.execute(f"""
            UPDATE 
                wordle_stats
            SET 
                streak = False;
            """)

    conn.commit()

def stats():
    # Pull number of games
    cur.execute("""
        SELECT 
            COUNT (*)
        FROM 
            wordle_stats;
        """)
    played = cur.fetchone()
    print(f'Played {played[0]} games.')

    # Calculate win %
    cur.execute("""
        SELECT 
            COUNT (win)
        FROM 
            wordle_stats
        WHERE
            win = True;
        """)
    wins = cur.fetchone()
    try:
        win_percent = (wins[0] / played[0])
        print(f'Win rate: {win_percent:.0%}')
    except ZeroDivisionError:
        print('No win percentage, no games played.')

    # Count win streak
    cur.execute("""
        SELECT 
            COUNT (streak)
        FROM 
            wordle_stats
        WHERE
            streak = True;
        """)
    streak = cur.fetchone()
    print(f'Streak: {streak[0]}')

    # Calculate guess distribution
    cur.execute("""
        SELECT
            tries,
            COUNT(*) AS num
        FROM
            wordle_stats
        WHERE
            win = True
        GROUP BY
            tries
        ORDER BY
            tries;
        """)
    guess = cur.fetchall()
    dist = [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]

    # If guess list has a tuple pair wherein the first value matches 
    # with another tuple pair in the dist list
    # then substitute dist pair with guess pair
    for guess_num, tries in guess:
        set = (guess_num, tries)
        out = [set if tries[0] == set[0] else tries for tries in dist]
        dist = out

    # Split dist tuple into two lists: 
    # ([1, 3, 6, 8, 5, 2], [1, 2, 3, 4, 5, 6]) -> [1, 3, 6, 8, 5, 2] and [1, 2, 3, 4, 5, 6]
    dist = list(zip(*dist))
    guess_dist = dist[0]
    distribution = dist[1]

    # Plot it
    plt.simple_bar(guess_dist, distribution, width = 100, title = 'Guess Distribution for Wins')
    plt.show()

def clear_stats():
    confirm = input('Enter Y to confirm. Enter N to go back: ').upper()
    if confirm == 'Y':
        cur.execute("""
            DELETE

            FROM
                wordle_stats;
            """)
        conn.commit()

def done():
    cur.close()
    conn.close()
    print("Done!")

function_dict = {'play':play, 'stats':stats, 'clear_stats':clear_stats, 'done':done}
command = ''

while command != 'done':
    command = input("\nWhat would you like to do?\n"
        "'play' plays a round of Wordle\n"
        "'stats' displays stats\n"
        "'clear_stats' clears stats\n"
        "'done' ends the program\n"
        "Input: ")
    print("\n")
    try:
        function_dict[command]()
    except KeyError:
        print('Invalid input')
