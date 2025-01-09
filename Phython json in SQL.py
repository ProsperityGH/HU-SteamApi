import psycopg2
from psycopg2.extras import execute_values
import json

connection = psycopg2.connect(
    user="postgres",*
    password="wachtwoord",
    host="20.229.115.179",
    port="5432",
    database="steamdatabase"
)

cursor = connection.cursor()
cursor.execute("""TRUNCATE TABLE games;""")

with open("games.json", "r") as f:
    push_games = []
    data = json.load(f)
    for games in data:
        values = list(games.values())
        values[0] = int(values[0])
        push_games.append(tuple(values))

insert_query = """
    INSERT INTO games (
        appid, name, release_date, english, developer, publisher, platforms, 
        required_age, categories, genres, steamspy_tags, achievements, 
        positive_ratings, negative_ratings, average_playtime, median_playtime, 
        owners, price
    )
    VALUES %s
    ON CONFLICT (appid) DO NOTHING;
"""

execute_values(cursor, insert_query, push_games, page_size=10000)
connection.commit()

connection.close()
