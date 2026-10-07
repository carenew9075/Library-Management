# ---------------------------------------------------------
# DATABASE TABLES
# ---------------------------------------------------------

from Database.database import connect_database


# ---------------------------------------------------------
# CREATE USERS TABLE
# ---------------------------------------------------------

def create_users_table():

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users
    (
        User_ID INT PRIMARY KEY AUTO_INCREMENT,
        User_Name VARCHAR(100) NOT NULL,
        Email VARCHAR(150) NOT NULL UNIQUE,
        Password_Hash VARCHAR(128) NOT NULL,
        Password_Salt VARCHAR(64) NOT NULL,
        Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()
    db.close()


# ---------------------------------------------------------
# CREATE BOOKS TABLE
# ---------------------------------------------------------

def create_books_table():

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Book
    (
        Book_ID INT PRIMARY KEY AUTO_INCREMENT,
        Title VARCHAR(150) NOT NULL,
        Author VARCHAR(150) NOT NULL,
        Education VARCHAR(50) NOT NULL,
        Copies INT NOT NULL DEFAULT 0
    )
    """)

    db.commit()
    db.close()


# ---------------------------------------------------------
# CREATE STUDENTS TABLE
# ---------------------------------------------------------

def create_students_table():

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students
    (
        Student_ID INT PRIMARY KEY AUTO_INCREMENT,
        Full_Name VARCHAR(100) NOT NULL,
        Class_Section VARCHAR(20) NOT NULL,
        Phone VARCHAR(10) NOT NULL,
        Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()
    db.close()


# ---------------------------------------------------------
# CREATE ISSUED TABLE
# ---------------------------------------------------------

def create_issued_table():

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Book_Issued
    (
        Issue_ID INT PRIMARY KEY AUTO_INCREMENT,
        Book_ID INT NOT NULL,
        Student_ID INT NOT NULL,
        Issue_Date DATE NOT NULL,
        Due_Date DATE NOT NULL
    )
    """)

    db.commit()
    db.close()


# ---------------------------------------------------------
# CREATE RETURNED TABLE
# ---------------------------------------------------------

def create_returned_table():

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Book_Returned
    (
        Return_ID INT PRIMARY KEY AUTO_INCREMENT,
        Book_ID INT NOT NULL,
        Student_ID INT NOT NULL,
        Issued_On DATE NOT NULL,
        Due_Date DATE NOT NULL,
        Returned_On DATE NOT NULL
    )
    """)

    db.commit()
    db.close()


# ---------------------------------------------------------
# CREATE CATEGORIES TABLE
# ---------------------------------------------------------

def create_categories_table():

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories
    (
        Category_ID INT PRIMARY KEY AUTO_INCREMENT,
        Category_Name VARCHAR(100) NOT NULL UNIQUE
    )
    """)

    db.commit()
    db.close()


# ---------------------------------------------------------
# CREATE LIBRARY CARDS TABLE
# ---------------------------------------------------------

def create_library_cards_table():

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Library_Cards
    (
        Card_ID INT PRIMARY KEY AUTO_INCREMENT,
        Student_ID INT NOT NULL,
        Card_Number VARCHAR(50) NOT NULL,
        Issue_Date DATE NOT NULL
    )
    """)

    db.commit()
    db.close()


# ---------------------------------------------------------
# COLUMN NAMES
# ---------------------------------------------------------

def column_names(cursor, table):

    cursor.execute("SHOW COLUMNS FROM " + table)
    names = {}
    for row in cursor.fetchall():
        names[row[0].lower()] = row[0]
    return names


# ---------------------------------------------------------
# REPAIR OLD TABLES
# ---------------------------------------------------------

def repair_old_tables():

    db = connect_database()
    cursor = db.cursor()

    students = column_names(cursor, "Students")

    if "full_name" not in students and "name" in students:
        cursor.execute(
            "ALTER TABLE Students CHANGE `" + students["name"] + "` Full_Name VARCHAR(100) NOT NULL"
        )

    if "class_section" not in students and "class_name" in students:
        cursor.execute(
            "ALTER TABLE Students CHANGE `" + students["class_name"] + "` Class_Section VARCHAR(20) NOT NULL"
        )

    users = column_names(cursor, "Users")

    if "password_hash" not in users:
        cursor.execute("ALTER TABLE Users ADD Password_Hash VARCHAR(128) NOT NULL DEFAULT ''")

    if "password_salt" not in users:
        cursor.execute("ALTER TABLE Users ADD Password_Salt VARCHAR(64) NOT NULL DEFAULT ''")

    db.commit()
    db.close()


# ---------------------------------------------------------
# CREATE ALL TABLES
# ---------------------------------------------------------

def create_all_tables():

    create_users_table()
    create_books_table()
    create_students_table()
    create_issued_table()
    create_returned_table()
    create_categories_table()
    create_library_cards_table()
    repair_old_tables()
