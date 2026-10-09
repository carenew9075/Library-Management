# ---------------------------------------------------------
# DATABASE QUERIES
# ---------------------------------------------------------

import hashlib
import os

from Database.database import connect_database


# ---------------------------------------------------------
# HASH PASSWORD
# ---------------------------------------------------------

def _hash_password(password, salt):

    password_bytes = password.encode("utf-8")

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt,
        200000
    )

    return password_hash.hex()


# ---------------------------------------------------------
# CREATE USER
# ---------------------------------------------------------

def create_user(user_name, email, password):

    salt = os.urandom(32)
    password_hash = _hash_password(password, salt)
    clean_email = email.strip().lower()

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SHOW COLUMNS FROM Users")
    columns = [row[0].lower() for row in cursor.fetchall()]

    cursor.execute("SELECT User_ID FROM Users WHERE Email = %s", (clean_email,))
    existing = cursor.fetchone()

    if existing is None:
        fields = ["User_Name", "Email", "Password_Hash", "Password_Salt"]
        values = [user_name.strip(), clean_email, password_hash, salt.hex()]
        if "password" in columns:
            fields.append("Password")
            values.append(password)
        cursor.execute(
            "INSERT INTO Users (" + ", ".join(fields) + ") VALUES (" + ", ".join(["%s"] * len(fields)) + ")",
            values
        )
    else:
        cursor.execute(
            "UPDATE Users SET Password_Hash = %s, Password_Salt = %s WHERE Email = %s",
            (password_hash, salt.hex(), clean_email)
        )
        if "password" in columns:
            cursor.execute(
                "UPDATE Users SET Password = %s WHERE Email = %s",
                (password, clean_email)
            )

    db.commit()
    db.close()
    return True


# ---------------------------------------------------------
# USER COUNT
# ---------------------------------------------------------

def user_count():

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users")
    result = cursor.fetchone()[0]
    db.close()
    return result


# ---------------------------------------------------------
# CHECK USER
# ---------------------------------------------------------

def check_user(email, password):

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    SELECT User_ID, User_Name, Email, Password_Hash, Password_Salt
    FROM Users
    WHERE Email = %s
    """, (email.strip().lower(),))

    result = cursor.fetchone()
    db.close()

    if result is None:
        return None

    user_id, user_name, user_email, stored_hash, stored_salt = result
    salt = bytes.fromhex(stored_salt)
    password_hash = _hash_password(password, salt)

    if password_hash != stored_hash:
        return None

    return user_id, user_name, user_email


# ---------------------------------------------------------
# BOOK QUERIES
# ---------------------------------------------------------

def get_all_books():

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book
    ORDER BY Book_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# GET BOOK
# ---------------------------------------------------------

def get_book(book_id):

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book
    WHERE Book_ID = %s
    """, (book_id,))
    row = cursor.fetchone()
    db.close()
    return row


# ---------------------------------------------------------
# STUDENT QUERIES
# ---------------------------------------------------------

def get_all_students():

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Student_ID, Full_Name, Class_Section, Phone
    FROM Students
    ORDER BY Student_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# GET STUDENT
# ---------------------------------------------------------

def get_student(student_id):

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Student_ID, Full_Name, Class_Section, Phone
    FROM Students
    WHERE Student_ID = %s
    """, (student_id,))
    row = cursor.fetchone()
    db.close()
    return row


# ---------------------------------------------------------
# ISSUE / RETURN RECORDS
# ---------------------------------------------------------

def get_issued_books():

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT
        i.Issue_ID,
        i.Book_ID,
        b.Title,
        i.Student_ID,
        s.Full_Name,
        i.Issue_Date,
        i.Due_Date
    FROM Book_Issued i
    JOIN Book b ON i.Book_ID = b.Book_ID
    JOIN Students s ON i.Student_ID = s.Student_ID
    ORDER BY i.Issue_ID DESC
    """)
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# GET RETURNED BOOKS
# ---------------------------------------------------------

def get_returned_books():

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT
        r.Return_ID,
        r.Book_ID,
        b.Title,
        r.Student_ID,
        s.Full_Name,
        r.Issued_On,
        r.Due_Date,
        r.Returned_On
    FROM Book_Returned r
    JOIN Book b ON r.Book_ID = b.Book_ID
    JOIN Students s ON r.Student_ID = s.Student_ID
    ORDER BY r.Return_ID DESC
    """)
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# GET ALL RECORDS
# ---------------------------------------------------------

def get_all_records():

    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT
        CONCAT('I-', i.Issue_ID) AS Record_ID,
        i.Book_ID,
        b.Title,
        i.Student_ID,
        s.Full_Name,
        i.Issue_Date,
        i.Due_Date,
        NULL AS Returned_On,
        'Issued' AS Status
    FROM Book_Issued i
    JOIN Book b ON i.Book_ID = b.Book_ID
    JOIN Students s ON i.Student_ID = s.Student_ID

    UNION ALL

    SELECT
        CONCAT('R-', r.Return_ID) AS Record_ID,
        r.Book_ID,
        b.Title,
        r.Student_ID,
        s.Full_Name,
        r.Issued_On,
        r.Due_Date,
        r.Returned_On,
        'Returned' AS Status
    FROM Book_Returned r
    JOIN Book b ON r.Book_ID = b.Book_ID
    JOIN Students s ON r.Student_ID = s.Student_ID

    ORDER BY Record_ID DESC
    """)
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# GET ISSUED RECORDS
# ---------------------------------------------------------

def get_issued_records():
    return [
        (
            "I-" + str(row[0]),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            None,
            "Issued"
        )
        for row in get_issued_books()
    ]


# ---------------------------------------------------------
# GET RETURNED RECORDS
# ---------------------------------------------------------

def get_returned_records():
    return [
        (
            "R-" + str(row[0]),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            "Returned"
        )
        for row in get_returned_books()
    ]


# ---------------------------------------------------------
# DASHBOARD / REPORTS
# ---------------------------------------------------------

def count_book_titles():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM Book")
    result = cursor.fetchone()[0]
    db.close()
    return result


# ---------------------------------------------------------
# COUNT STUDENTS
# ---------------------------------------------------------

def count_students():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM Students")
    result = cursor.fetchone()[0]
    db.close()
    return result


# ---------------------------------------------------------
# COUNT ISSUED BOOKS
# ---------------------------------------------------------

def count_issued_books():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM Book_Issued")
    result = cursor.fetchone()[0]
    db.close()
    return result


# ---------------------------------------------------------
# COUNT AVAILABLE COPIES
# ---------------------------------------------------------

def count_available_copies():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(SUM(Copies), 0) FROM Book")
    result = cursor.fetchone()[0]
    db.close()
    return result


# ---------------------------------------------------------
# COUNT TOTAL COPIES
# ---------------------------------------------------------

def count_total_copies():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT COALESCE(SUM(Copies), 0) +
           (SELECT COUNT(*) FROM Book_Issued)
    FROM Book
    """)
    result = cursor.fetchone()[0]
    db.close()
    return result


# ---------------------------------------------------------
# GET RECENT ACTIVITIES
# ---------------------------------------------------------

def get_recent_activities(limit=10):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT
        i.Book_ID,
        b.Title,
        s.Full_Name,
        i.Issue_Date
    FROM Book_Issued i
    JOIN Book b ON i.Book_ID = b.Book_ID
    JOIN Students s ON i.Student_ID = s.Student_ID
    ORDER BY i.Issue_ID DESC
    LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    db.close()
    return rows
