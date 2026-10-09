from Database.database import connect_database


# ---------------------------------------------------------
# GET STOCK
# ---------------------------------------------------------

def get_stock():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Book_ID, Title, Author, Education, Copies
    FROM Book ORDER BY Book_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows


# ---------------------------------------------------------
# GET AVAILABLE STOCK
# ---------------------------------------------------------

def get_available_stock():
    return [row for row in get_stock() if row[4] > 0]


# ---------------------------------------------------------
# GET OUT OF STOCK
# ---------------------------------------------------------

def get_out_of_stock():
    return [row for row in get_stock() if row[4] == 0]
