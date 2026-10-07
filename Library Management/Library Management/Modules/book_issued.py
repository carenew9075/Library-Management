from datetime import date
from Database.database import connect_database


# ---------------------------------------------------------
# ISSUE BOOK
# ---------------------------------------------------------

def issue_book(book_id, student_id, due_date):

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("SELECT Copies FROM Book WHERE Book_ID = %s", (book_id,))
    book = cursor.fetchone()

    if book is None:
        db.close()
        return False, "Book not found."

    if book[0] <= 0:
        db.close()
        return False, "No available copies of this book."

    cursor.execute(
        "SELECT Student_ID FROM Students WHERE Student_ID = %s",
        (student_id,)
    )
    student = cursor.fetchone()

    if student is None:
        db.close()
        return False, "Student not found."

    cursor.execute("""
    SELECT Issue_ID
    FROM Book_Issued
    WHERE Book_ID = %s AND Student_ID = %s
    """, (book_id, student_id))

    if cursor.fetchone() is not None:
        db.close()
        return False, "This student already has an active issue for this book."

    if due_date < date.today():
        db.close()
        return False, "Due date cannot be in the past."

    cursor.execute("""
    INSERT INTO Book_Issued
    (Book_ID, Student_ID, Issue_Date, Due_Date)
    VALUES (%s, %s, %s, %s)
    """, (book_id, student_id, date.today(), due_date))

    cursor.execute(
        "UPDATE Book SET Copies = Copies - 1 WHERE Book_ID = %s",
        (book_id,)
    )

    db.commit()
    db.close()
    return True, "Book issued successfully."


# ---------------------------------------------------------
# VIEW ISSUED BOOKS
# ---------------------------------------------------------

def view_issued_books():
    from Database.queries import get_issued_books
    return get_issued_books()
