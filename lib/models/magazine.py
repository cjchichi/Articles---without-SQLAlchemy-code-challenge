import sqlite3

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value,str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string")
        self._category = value.strip()

    def save(self, conn):
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
        conn.commit()

    @classmethod
    def find_by_id(cls, conn, magazine_id):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?",(magazine_id,))
        row = cursor.fetchone()
        return cls(id=row[0], name=row[1], category=row[2]) if row else None

    @classmethod
    def find_by_name(cls, conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category FROM magazines WHERE name = ?",(name,))
        row = cursor.fetchone()
        return cls(id=row[0], name=row[1], category=row[2]) if row else None

    @classmethod
    def find_by_category(cls, conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category FROM magazines WHERE category = ?",(category,))
        row = cursor.fetchall()
        return [cls(id=row[0], name=row[1], category=row[2]) for row in row]

    def articles(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM articles WHERE magazine_id = ?",(self.id,))
        return cursor.fetchall()

    def authors(self,conn):
        cursor= conn.cursor()
        cursor.execute("""SELECT DISTINCT authors.id, authors.name FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id = ?""", (self.id,))
        return cursor.fetchall()

