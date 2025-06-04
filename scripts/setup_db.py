import sqlite3
import os


DB_PATH = "lib/db/database.db"


SCHEMA_PATH = "lib/db/schema.sql"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, 'r') as schema_file:
        schema_sql = schema_file.read()
        cursor.executescript(schema_sql)

    cursor.executescript("""
        INSERT INTO authors (name) VALUES ('Alice'), ('Bob');
        INSERT INTO magazines (name, category) VALUES ('Tech Weekly', 'Technology'), ('Health Today', 'Health');
        INSERT INTO articles (title, author_id, magazine_id) VALUES 
            ('AI and the Future', 1, 1),
            ('Healthy Living', 2, 2),
            ('Quantum Computing', 1, 1);
    """)

    conn.commit()
    conn.close()
    print("Database setup complete")

if __name__ == "__main__":
    setup_database()
