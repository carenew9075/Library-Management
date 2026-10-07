# ---------------------------------------------------------
# REQUIRED
# ---------------------------------------------------------

def required(value):
    return str(value).strip() != ""


# ---------------------------------------------------------
# INTEGER
# ---------------------------------------------------------

def integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------
# NON NEGATIVE INTEGER
# ---------------------------------------------------------

def non_negative_integer(value):
    try:
        return int(value) >= 0
    except ValueError:
        return False


# ---------------------------------------------------------
# POSITIVE INTEGER
# ---------------------------------------------------------

def positive_integer(value):
    try:
        return int(value) > 0
    except ValueError:
        return False


# ---------------------------------------------------------
# PHONE
# ---------------------------------------------------------

def phone(value):
    value = str(value).strip()
    return len(value) == 10 and value.isdigit()


# ---------------------------------------------------------
# EMAIL
# ---------------------------------------------------------

def email(value):
    value = str(value).strip()
    return "@" in value and "." in value.split("@")[-1]


# ---------------------------------------------------------
# PASSWORD
# ---------------------------------------------------------

def password(value):
    return len(value) >= 4
