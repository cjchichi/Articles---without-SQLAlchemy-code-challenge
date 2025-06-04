# import sqlite3
# from lib.db.connection import get_connection

# class Author:
#     def __init__(self, name, id=None):
#         self.id = id
#         self.name = name

#     @property
#     def name(self):
#         return self._name

#     @name.setter
#     def name(self, value):
#         if not isinstance(value, str) or len(value.strip()) == 0:
#             raise ValueError("Name must be a non-empty string")
#         self._name = value.strip()

#     def save(self, conn=None):
#         if conn is None:
#             conn = get_connection()
#         cursor = conn.cursor()
#         if self.id is None:
#             cursor.execute("INSERT INTO authors (name) VALUES (?)",(self.name,))
#             self.id = cursor.lastrowid
#         else:
#             cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
#         conn.commit()

#     @classmethod
#     def find_by_id(cls, author_id, conn=None):
#         if conn is None:
#             conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, name FROM authors WHERE id = ?",(author_id,))
#         row = cursor.fetchone()
#         return cls(id=row[0], name=row[1]) if row else None

#     @classmethod
#     def find_by_name(cls, name, conn=None):
#         if conn is None:
#             conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, name FROM authors WHERE name = ?", (name,))
#         row = cursor.fetchone()
#         return cls(id=row[0], name=row[1]) if row else None

#     def articles(self,conn=None):
#         if conn is None:
#             conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, title FROM articles WHERE author_id = ?", (self.id,))
#         return cursor.fetchall()

#     def magazines(self, conn=None):
#         if conn is None:
#             conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("""SELECT DISTINCT magazines.id, magazines.name FROM magazines JOIN articles ON magazines.id = articles.magazine_id WHERE articles.author_id = ?""",(self.id,))
#         return cursor.fetchall()
         

# #### Author Class
# # - Implement an Author class with proper initialization
# # - Write SQL methods to:
# # - Save an author to the database
# # - Find an author by ID or name
# # - Properties and validations for name
# # - Include methods to work with relationships


import sqlite3
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM authors WHERE name = ?", (name,)).fetchone()
        return cls(id=row["id"], name=row["name"])

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        return [Article(**row) for row in rows.fetchall()]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        return [Magazine(**row) for row in rows.fetchall()]

    def add_article(self, magazine, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, self.id, magazine.id)
        )
        conn.commit()

    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("""
            SELECT authors.*, COUNT(articles.id) AS count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            GROUP BY authors.id
            ORDER BY count DESC
            LIMIT 1
        """).fetchone()
        return cls(id=row["id"], name=row["name"])

