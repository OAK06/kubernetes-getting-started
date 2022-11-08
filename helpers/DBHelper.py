import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor


def getConn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def fetchone(conn, query, params=None):
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result


def fetchall(conn, query, params=None):
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


def fetchoneAssoc(conn, query, params=None):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result


def fetchallAssoc(conn, query, params=None):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


def insert(conn, query, params=None, fetchRecord=False):
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    if fetchRecord:
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    else:
        count = cursor.rowcount
        cursor.close()
        return count


def update(conn, query, params=None, fetchRecord=None):
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    if fetchRecord is not None:
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    else:
        count = cursor.rowcount
        cursor.close()
        return count


def delete(conn, query, params=None):
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    count = cursor.rowcount
    cursor.close()
    return count


def execute(conn, query, params=None):
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    count = cursor.rowcount
    cursor.close()
    return count


def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occured
    line_num = traceback.tb_lineno
    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")
