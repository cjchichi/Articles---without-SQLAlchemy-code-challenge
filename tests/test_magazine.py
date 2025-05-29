import sqlite3
import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article

@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.executescript("""
    CREATE TABLE authors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    CREATE TABLE magazines (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL
    );
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author_id INTEGER,
        magazine_id INTEGER,
        FOREIGN KEY(author_id) REFERENCES authors(id),
        FOREIGN KEY(magazine_id) REFERENCES magazines(id)
    );
    """)
    return connection

def test_magazine_save_and_find(conn):
    mag = Magazine("Tech Weekly", "Technology")
    mag.save(conn)

    found = Magazine.find_by_id(conn, mag.id)
    assert found.name == "Tech Weekly"
    assert found.category == "Technology"

def test_find_by_name(conn):
    mag = Magazine("Health Today", "Health")
    mag.save(conn)
    found = Magazine.find_by_name(conn, "Health Today")
    assert found.category == "Health"

def test_articles_and_authors(conn):
    mag = Magazine("Nature World", "Science")
    mag.save(conn)
    
    author = Author("Alice")
    author.save(conn)

    article1 = Article("Climate Change", author.id, mag.id)
    article2 = Article("Wildlife Conservation", author.id, mag.id)
    article1.save(conn)
    article2.save(conn)

    articles = mag.articles(conn)
    assert len(articles) == 2

    authors = mag.authors(conn)
    assert len(authors) == 1
    assert authors[0][1] == "Alice"
