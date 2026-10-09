# ---------------------------------------------------------
# STUDENTS
# ---------------------------------------------------------

from Database.database import connect_database


# ---------------------------------------------------------
# REGISTER STUDENT
# ---------------------------------------------------------

def register_student(student_code, full_name, class_section, phone):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO Students (Student_ID, Full_Name, Class_Section, Phone)
    VALUES (%s, %s, %s, %s)
    """, (student_code.strip(), full_name.strip(), class_section.strip(), phone.strip()))
    db.commit()
    db.close()
    return True, "Student registered successfully."


# ---------------------------------------------------------
# SEARCH STUDENT
# ---------------------------------------------------------

def search_student(student_id):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Student_ID, Full_Name, Class_Section, Phone
    FROM Students WHERE Student_ID = %s
    """, (student_id,))
    row = cursor.fetchone()
    db.close()
    return row


# ---------------------------------------------------------
# UPDATE STUDENT
# ---------------------------------------------------------

def update_student(student_id, full_name, class_section, phone):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    UPDATE Students
    SET Full_Name = %s, Class_Section = %s, Phone = %s
    WHERE Student_ID = %s
    """, (full_name.strip(), class_section.strip(), phone.strip(), student_id))
    db.commit()
    changed = cursor.rowcount
    db.close()
    return changed > 0


# ---------------------------------------------------------
# DELETE STUDENT
# ---------------------------------------------------------

def delete_student(student_id):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Students WHERE Student_ID = %s", (student_id,))
    db.commit()
    changed = cursor.rowcount
    db.close()
    return changed > 0


# ---------------------------------------------------------
# VIEW ALL STUDENTS
# ---------------------------------------------------------

def view_all_students():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("""
    SELECT Student_ID, Full_Name, Class_Section, Phone
    FROM Students ORDER BY Student_ID
    """)
    rows = cursor.fetchall()
    db.close()
    return rows
