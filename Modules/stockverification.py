from Database.database import connect_database


# ---------------------------------------------------------
# CHECK BOOK STOCK
# ---------------------------------------------------------

def check_book_stock(book_id):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute(
        "SELECT Book_ID, Title, Copies FROM Book WHERE Book_ID = %s",
        (book_id,)
    )
    row = cursor.fetchone()
    db.close()
    return row


# ---------------------------------------------------------
# VERIFY STOCK
# ---------------------------------------------------------

def verify_stock(book_id, required_copies):
    row = check_book_stock(book_id)

    if row is None:
        return False, "Book not found."

    if row[2] < required_copies:
        return False, "Not enough copies available."

    return True, "Stock available."
