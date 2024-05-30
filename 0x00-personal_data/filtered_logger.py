#!/usr/bin/env python3
"""
Module that uses regex to replace occurrences of certain
fields
"""

import re
import logging
import mysql.connector
import os
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Function that replaces occurrences of certain fields
    with redaction
    """
    for f in fields:
        message = re.sub(f + "=.*?" + separator,
                         f + "=" + redaction + separator, message)

    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Function that returns a logger
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Function that returns a connector
    """
    db_user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    db_password = os.environ.get('PERSONAL_DATA_DB_PASSWORD')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST')

    # connect to the MySQL server
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_password,
        database=db_name
    )
    return db


def main():
    """Main function getting database connection using get_db()
    and retrieves all the rows from users table then displays
    them under a filtered format"""
    db = get_db()
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    # Retrieve the field names from the cursor's description
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    # Iterate over each row fetched by the cursor
    for row in cursor:
        # Create string representation of the row, \
        # concatenating field name and value pairs
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        # Log the formatted row using the logger
        logger.info(str_row.strip())

    # Close the cursor to release resources
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()