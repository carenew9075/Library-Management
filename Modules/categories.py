from Database.database import connect_database


# ---------------------------------------------------------
# ADD CATEGORY
# ---------------------------------------------------------

def add_category(category_name):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO Categories (Category_Name) VALUES (%s)",
        (category_name.strip(),)
    )
    db.commit()
    db.close()


# ---------------------------------------------------------
# DELETE CATEGORY
# ---------------------------------------------------------

def delete_category(category_id):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM Categories WHERE Category_ID = %s",
        (category_id,)
    )
    deleted = cursor.rowcount
    db.commit()
    db.close()
    return deleted


# ---------------------------------------------------------
# VIEW ALL CATEGORIES
# ---------------------------------------------------------

def view_all_categories():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute(
        "SELECT Category_ID, Category_Name FROM Categories ORDER BY Category_ID"
    )
    rows = cursor.fetchall()
    db.close()
    return rows
