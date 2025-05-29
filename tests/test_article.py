import sqlite3
import pytest
from lib.models.article import Article

@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);")
    cursor.execute("CREATE TABLE magazines (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);")
    cursor.execute("CREATE TABLE articles (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER, magazine_id INTEGER);")
    cursor.execute("INSERT INTO authors (name) VALUES ('Alice')")
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Technology')")
    conn.commit()
    return conn

def test_article_creation_and_save(conn):
    article = Article("AI Trends", author_id=1, magazine_id=1)
    article.save(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT title FROM articles WHERE id = ?", (article.id,))
    row = cursor.fetchone()

    assert row[0] == "AI Trends"

def test_find_by_id(conn):
    article = Article("Data Science", 1, 1)
    article.save(conn)
    found = Article.find_by_id(conn, article.id)

    assert found.title == "Data Science"

def test_find_by_title(conn):
    article = Article("Deep Learning", 1, 1)
    article.save(conn)
    found = Article.find_by_title(conn, "Deep Learning")

    assert found.id == article.id

def test_find_by_author(conn):
    article1 = Article("AI Intro", 1, 1)
    article2 = Article("ML Basics", 1, 1)
    article1.save(conn)
    article2.save(conn)

    articles = Article.find_by_author(conn, 1)
    titles = [a.title for a in articles]

    assert "AI Intro" in titles and "ML Basics" in titles

def test_title_validation():
    with pytest.raises(ValueError):
        Article("", 1, 1)  
    with pytest.raises(ValueError):
        Article(123, 1, 1)  
