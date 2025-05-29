import sqlite3
import pytest
from lib.models.author import Author
from lib.models.article import Article

@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);")
    cursor.execute("CREATE TABLE magazines (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);")
    cursor.execute("CREATE TABLE articles (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER, magazine_id INTEGER);")
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Tech')")
    conn.commit()
    return conn

def test_author_creation_and_save(conn):
    author = Author("Alice")
    author.save(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM authors WHERE id = ?", (author.id,))
    row = cursor.fetchone()
    assert row[0] == "Alice"

def test_find_by_name(conn):
    author = Author("Bob")
    author.save(conn)
    found = Author.find_by_name(conn, "Bob")
    assert found.name == "Bob"

def test_find_by_id(conn):
    author = Author("Charlie")
    author.save(conn)
    found = Author.find_by_id(conn, author.id)
    assert found.name == "Charlie"

def test_articles_and_magazines(conn):
    author = Author("Dana")
    author.save(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("AI News", author.id, 1))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("ML Weekly", author.id, 1))
    conn.commit()

    articles = author.articles(conn)
    magazines = author.magazines(conn)

    assert len(articles) == 2
    assert magazines[0][1] == "Tech Today"
