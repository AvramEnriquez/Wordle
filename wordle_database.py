import psycopg2
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
    print("Database connected successfully!")
    valid_database = True
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
            "win" BOOLEAN
        );
        """)
    print(f"{table_name} Table created successfully.")
except psycopg2.errors.DuplicateTable:
    # State if table already exists
    print(f"{table_name} Table already exists.")

conn.commit()  # Commit the change

"""Functions to play game or see stats"""
def play():
    tries, win = wordle()

    cur.execute(f"""
        INSERT INTO wordle_stats (
            tries, 
            win
        )
        VALUES (
            {tries}, 
            {win}
        );
        """)
    conn.commit()

def stats():
    cur.execute(f"""
        SELECT COUNT (*)
        FROM wordle_stats;
        """)
    played = cur.fetchone()
    print(f'Played {played[0]} games.')

    cur.execute(f"""
        SELECT COUNT (
            CASE 
                WHEN True THEN 1
                ELSE 0 
            END)
        FROM wordle_stats;
        """)
    wins = cur.fetchone()
    win_percent = (wins[0] / played[0]) * 100
    print(f'Win rate: {win_percent}%')

    conn.commit()

def done():
    cur.close()
    conn.close()
    print("Done!")

function_dict = {'play':play, 'stats':stats, 'done':done}
command = ''

while command != 'done':
    print("")
    command = input("What would you like to do?\n"
        "'play' plays a round of Wordle\n"
        "'stats' displays stats\n"
        "'done' ends the program\n"
        "Input: ")
    function_dict[command]()