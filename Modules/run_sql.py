# ---------------------------------------------------------
# RUN SQL
# ---------------------------------------------------------

from Database.database import connect_database


def run_sql(statement):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute(statement)
    if cursor.description is None:
        db.commit()
        count = cursor.rowcount
        db.close()
        return "Done. Rows changed: " + str(count)
    rows = cursor.fetchall()
    db.close()
    if len(rows) == 0:
        return "No rows."
    lines = []
    for row in rows[:20]:
        lines.append(str(row))
    return "\n".join(lines)
