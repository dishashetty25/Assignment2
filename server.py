import socket
import sqlite3

conn = sqlite3.connect("Library.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute('''
               create table if not exists BOOKS(
                   BookID integer primary key,
                   Title text,
                   Author text,
                   Genre text,
                   YearPublished integer
               )''')

cursor.execute('''
               create table if not exists BORROWERS(
                   BorrowerID integer,
                   Name text,
                   Email text,
                   Phone integer,
                   BookID integer,
                   foreign key (BookID) references BOOKS(BookID)
               )''')

def actionSelect(tablename, id):
    try:
        cursor.execute(f"SELECT * FROM {tablename} WHERE BookID = ?", (id,))
        result = cursor.fetchone()
        if result:
            column_names = [description[0] for description in cursor.description]
            record_parts = [f"{col}={val}" for col, val in zip(column_names, result)]
            return f"1|{tablename}|" + ", ".join(record_parts)
        else:
            return "No record found"
    except sqlite3.Error as e:
        return f"FAILURE: {e}"

def actionInsert(tablename, kwargs):
    try:
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        values = tuple(kwargs.values())
        query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        return "SUCCESS"
    except sqlite3.Error as e:
        return f"FAILURE: {e}"
    
def actionDelete(tablename, id):
    try:
        cursor.execute(f"DELETE FROM {tablename} WHERE BookID = ?", (id,))
        conn.commit()
        return "SUCCESS" if cursor.rowcount > 0 else "FAILURE: Record not found."
    except sqlite3.Error as e:
        return f"FAILURE: {e}"
    
server_socket = socket.socket()
server_socket.bind(('localhost',12345))
server_socket.listen(1)
print("Server is waiting for the connection...")

while True:
    client_socket, address = server_socket.accept()
    print("Connected to:",address)
    data = client_socket.recv(1024).decode()
    if not data:
        client_socket.close()
        continue
    print(f"Received:{data}")
    try:
        parts = data.strip().split('|')
        action_number = int(parts[0])
        tablename = parts[1]
        parameters = parts[2]
        
        if action_number == 1:
            result = actionSelect(tablename,int(parameters))
        elif action_number == 2:
            pairs = parameters.split(',')
            kwargs = {kv.split('=')[0].strip(): kv.split('=')[1].strip() for kv in pairs}
            result = actionInsert(tablename,kwargs)
        elif action_number == 3:
            result =  actionDelete(tablename,int(parameters))
        else:
            result = "Invalid Operation"
             
    except Exception as e:
        result = f"FAILURE:{str(e)}"

    client_socket.send(result.encode())
    client_socket.close()