import sqlite3

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    def save(self, conn):
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)",(self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()

    @classmethod
    def find_by_id(cls, conn, author_id):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM authors WHERE id = ?",(author_id,))
        row = cursor.fetchone()
        return cls(id=row[0], name=row[1]) if row else None

    @classmethod
    def find_by_name(cls, conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        return cls(id=row[0], name=row[1]) if row else None

    def articles(self,conn):
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM articles WHERE author_id = ?", (self.id,))
        return cursor.fetchall()

    def magazines(self, conn):
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT magazines.id, magazines.name FROM magazines JOIN articles ON magazines.id = articles.magazine_id WHERE articles.author_id = ?""",(self.id,))
        return cursor.fetchall()
         

#### Author Class
# - Implement an Author class with proper initialization
# - Write SQL methods to:
# - Save an author to the database
# - Find an author by ID or name
# - Properties and validations for name
# - Include methods to work with relationships
