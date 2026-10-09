from Database.database import connect_database


# ---------------------------------------------------------
# CREATE LIBRARY CARD
# ---------------------------------------------------------

def create_library_card(student_id, card_number, issue_date):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO Library_Cards (Student_ID, Card_Number, Issue_Date)
    VALUES (%s, %s, %s)
    """, (student_id, card_number, issue_date))
    db.commit()
    db.close()


# ---------------------------------------------------------
# SEARCH LIBRARY CARD
# ---------------------------------------------------------

def search_library_card(student_id):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Card_ID, Student_ID, Card_Number, Issue_Date
    FROM Library_Cards WHERE Student_ID = %s
    """, (student_id,))
    row = cursor.fetchone()
    db.close()
    return row


# ---------------------------------------------------------
# VIEW ALL LIBRARY CARDS
# ---------------------------------------------------------

def view_all_library_cards():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Card_ID, Student_ID, Card_Number, Issue_Date
    FROM Library_Cards ORDER BY Card_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows
