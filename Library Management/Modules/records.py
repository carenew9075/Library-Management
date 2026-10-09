from Database import queries


# ---------------------------------------------------------
# GET ALL RECORDS
# ---------------------------------------------------------

def get_all_records():
    return queries.get_all_records()


# ---------------------------------------------------------
# GET ISSUED RECORDS
# ---------------------------------------------------------

def get_issued_records():
    return queries.get_issued_records()


# ---------------------------------------------------------
# GET RETURNED RECORDS
# ---------------------------------------------------------

def get_returned_records():
    return queries.get_returned_records()
