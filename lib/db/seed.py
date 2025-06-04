from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def reset_db():
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
    """)
    conn.commit()
    conn.close()

def seed():
    reset_db()

    a1 = Author(name="Alice")
    a1.save()
    a2 = Author(name="Bob")
    a2.save()

    m1 = Magazine(name="Tech Times", category="Technology")
    m1.save()
    m2 = Magazine(name="Science Daily", category="Science")
    m2.save()

    Article(title="AI Revolution", author_id=a1.id, magazine_id=m1.id).save()
    Article(title="Cybersecurity Tips", author_id=a2.id, magazine_id=m1.id).save()
    Article(title="SpaceX Update", author_id=a1.id, magazine_id=m2.id).save()

if __name__ == "__main__":
    seed()
