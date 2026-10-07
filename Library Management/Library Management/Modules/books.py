from Database.database import connect_database


# ---------------------------------------------------------
# ADD BOOK
# ---------------------------------------------------------

def add_book(title, author, education, copies):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO Book (Title, Author, Education, Copies)
    VALUES (%s, %s, %s, %s)
    """, (title.strip(), author.strip(), education.strip(), copies))
    db.commit()
    db.close()


# ---------------------------------------------------------
# DELETE BOOK
# ---------------------------------------------------------

def delete_book(book_id):
    db = connect_database()
    cursor = db.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM Book_Issued WHERE Book_ID = %s",
        (book_id,)
    )

    active_issues = cursor.fetchone()[0]

    if active_issues > 0:
        db.close()
        return False, "This book is currently issued and cannot be deleted."

    cursor.execute(
        "DELETE FROM Book WHERE Book_ID = %s",
        (book_id,)
    )

    deleted = cursor.rowcount
    db.commit()
    db.close()

    if deleted == 0:
        return False, "Book not found."

    return True, "Book deleted successfully."


# ---------------------------------------------------------
# SEARCH BOOK
# ---------------------------------------------------------

def search_book(book_id):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book WHERE Book_ID = %s
    """, (book_id,))
    row = cursor.fetchone()
    db.close()
    return row


# ---------------------------------------------------------
# VIEW ALL BOOKS
# ---------------------------------------------------------

def view_all_books():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book ORDER BY Book_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows
