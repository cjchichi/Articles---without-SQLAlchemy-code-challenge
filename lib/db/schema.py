
from .connection import get_connection

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    with open("lib/db/schema.sql") as f:
        sql = f.read()
        cursor.executescript(sql)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
