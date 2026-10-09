from datetime import date
from Database.database import connect_database


# ---------------------------------------------------------
# RETURN BOOK
# ---------------------------------------------------------

def return_book(book_id, student_id):

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    SELECT Issue_ID, Issue_Date, Due_Date
    FROM Book_Issued
    WHERE Book_ID = %s AND Student_ID = %s
    ORDER BY Issue_ID DESC
    LIMIT 1
    """, (book_id, student_id))

    issue = cursor.fetchone()

    if issue is None:
        db.close()
        return False, "No active issue found for this book and student."

    issue_id, issue_date, due_date = issue

    cursor.execute("""
    INSERT INTO Book_Returned
    (Book_ID, Student_ID, Issued_On, Due_Date, Returned_On)
    VALUES (%s, %s, %s, %s, %s)
    """, (book_id, student_id, issue_date, due_date, date.today()))

    cursor.execute(
        "UPDATE Book SET Copies = Copies + 1 WHERE Book_ID = %s",
        (book_id,)
    )

    cursor.execute(
        "DELETE FROM Book_Issued WHERE Issue_ID = %s",
        (issue_id,)
    )

    db.commit()
    db.close()
    return True, "Book returned successfully."


# ---------------------------------------------------------
# VIEW RETURNED BOOKS
# ---------------------------------------------------------

def view_returned_books():
    from Database.queries import get_returned_books
    return get_returned_books()
