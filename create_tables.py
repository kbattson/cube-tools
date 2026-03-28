import psycopg2
import json
import sys

def init_cubes_table():
    conn = psycopg2.connect(
        dbname="cube_tools",
        user="postgres",
        password=sys.argv[1],
        host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cubes (
            id TEXT PRIMARY KEY,
            cards INTEGER[]
        )
    """)

    with open('data/cubes.json') as f:
        cubes = json.load(f)
        
    for cube in cubes:
        cursor.execute(
            "INSERT INTO cubes (id, cards) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
            (cube['id'], cube['cards'])
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_cubes_table()
