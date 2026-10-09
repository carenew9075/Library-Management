from Database.database import connect_database


# ---------------------------------------------------------
# GET AVAILABLE BOOKS
# ---------------------------------------------------------

def get_available_books():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book WHERE Copies > 0 ORDER BY Book_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# SEARCH BOOK BY TITLE
# ---------------------------------------------------------

def search_book_by_title(title):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book
    WHERE Title LIKE %s AND Copies > 0
    ORDER BY Book_ID
    """, ("%" + title + "%",))
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# SEARCH BOOK BY AUTHOR
# ---------------------------------------------------------

def search_book_by_author(author):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book
    WHERE Author LIKE %s AND Copies > 0
    ORDER BY Book_ID
    """, ("%" + author + "%",))
    rows = cursor.fetchall()
    db.close()
    return rows
