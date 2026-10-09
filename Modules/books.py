from Database.database import connect_database


# ---------------------------------------------------------
# ADD BOOK
# ---------------------------------------------------------

def add_book(book_code, title, author, education, copies):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO Book (Book_ID, Title, Author, Education, Copies)
    VALUES (%s, %s, %s, %s, %s)
    """, (book_code.strip(), title.strip(), author.strip(), education.strip(), copies))
    db.commit()
    db.close()


# ---------------------------------------------------------
# ADD MANY BOOKS
# ---------------------------------------------------------

def add_many_books(rows):
    saved = 0
    skipped = 0
    db = connect_database()
    cursor = db.cursor()
    for code, title, author, education, copies in rows:
        try:
            cursor.execute("""
            INSERT INTO Book (Book_ID, Title, Author, Education, Copies)
            VALUES (%s, %s, %s, %s, %s)
            """, (code, title, author, education, copies))
            saved = saved + 1
        except Exception:
            skipped = skipped + 1
    db.commit()
    db.close()
    return saved, skipped


# ---------------------------------------------------------
# UPDATE BOOK
# ---------------------------------------------------------

def update_book(book_code, title, author, education, copies):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    UPDATE Book
    SET Title = %s, Author = %s, Education = %s, Copies = %s
    WHERE Book_ID = %s
    """, (title.strip(), author.strip(), education.strip(), copies, book_code))
    db.commit()
    changed = cursor.rowcount
    db.close()
    return changed > 0


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
