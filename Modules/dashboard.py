from Database import queries


# ---------------------------------------------------------
# GET DASHBOARD DATA
# ---------------------------------------------------------

def get_dashboard_data():
    return (
        queries.count_book_titles(),
        queries.count_students(),
        queries.count_issued_books(),
        queries.count_available_copies()
    )


# ---------------------------------------------------------
# GET RECENT ACTIVITIES
# ---------------------------------------------------------

def get_recent_activities():
    return queries.get_recent_activities()
