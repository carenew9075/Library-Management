# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

import re
import mysql.connector

from Config import config


# ---------------------------------------------------------
# VALIDATE DATABASE NAME
# ---------------------------------------------------------

def _validate_database_name():

    if not re.fullmatch(r"[A-Za-z0-9_]+", config.DB_NAME):
        raise ValueError("Database name contains invalid characters.")


# ---------------------------------------------------------
# CREATE DATABASE IF NEEDED
# ---------------------------------------------------------

def create_database_if_needed():

    _validate_database_name()

    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

    cursor = connection.cursor()
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS `" + config.DB_NAME + "`"
    )

    connection.close()


# ---------------------------------------------------------
# CONNECT DATABASE
# ---------------------------------------------------------

def connect_database():

    create_database_if_needed()

    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

    return connection


# ---------------------------------------------------------
# TEST CONNECTION
# ---------------------------------------------------------

def test_connection():

    connection = None

    try:
        connection = connect_database()
        return True, "Database connection successful."

    except Exception:
        return False, (
            "Unable to connect to MySQL.\n\n"
            "Check that MySQL Server is running and that your "
            "database settings in .env are correct."
        )

    finally:
        if connection is not None:
            connection.close()
