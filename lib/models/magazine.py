
import sqlite3
from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
        conn.commit()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,)).fetchone()
        return cls(id=row["id"], name=row["name"], category=row["category"])

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,)).fetchone()
        return cls(id=row["id"], name=row["name"], category=row["category"])

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        return [Author(**row) for row in rows.fetchall()]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        return [row["title"] for row in rows.fetchall()]

    def contributing_authors(self):
        return self.contributors()

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) > 1
        """)
        return [cls(id=row["id"], name=row["name"], category=row["category"]) for row in rows.fetchall()]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT m.*, COUNT(a.id) AS article_count FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """)
        return [cls(id=row["id"], name=row["name"], category=row["category"]) for row in rows.fetchall()]

        
