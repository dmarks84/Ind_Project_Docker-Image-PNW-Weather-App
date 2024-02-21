import sqlite3

def create_table(conn, command):
    try:
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()
        cur.close()
    except Exception as error:
        print('Unable to create table:',error)

def get_query(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result
    except Exception as error:
        print('Unable to execute query:',error)

def insert_row(conn, command, data):
    try:
        cur = conn.cursor()
        cur.execute(command, data)
        cur.close()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
    except Exception as error:
        print('Unable to add alert:',error)