from Database.database import connect_database


# ---------------------------------------------------------
# GET REPORT SUMMARY
# ---------------------------------------------------------

def get_report_summary():
    db = connect_database()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(Copies), 0) FROM Book")
    titles, available = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM Students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Book_Issued")
    issued = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Book_Returned")
    returned = cursor.fetchone()[0]

    total_copies = available + issued

    db.close()

    return titles, total_copies, students, issued, returned, available


# ---------------------------------------------------------
# GET MOST ISSUED BOOKS
# ---------------------------------------------------------

def get_most_issued_books():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT
        b.Book_ID,
        b.Title,
        COUNT(*) AS Issue_Count
    FROM
    (
        SELECT Book_ID FROM Book_Issued
        UNION ALL
        SELECT Book_ID FROM Book_Returned
    ) AS activity
    JOIN Book b ON activity.Book_ID = b.Book_ID
    GROUP BY b.Book_ID, b.Title
    ORDER BY Issue_Count DESC, b.Book_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows
