import sqlite3 as db

connection = db.connect('database.db')
connection.execute('create table users (id integer primary key autoincrement, name str not null, password str not null);')
connection.commit()
connection.close()



def login(user, name) -> bool:
    connection = db.connect('database.db')
    cursor = connection.execute("select * from users where name = '?'", (user,))
    users = cursor.fetchall()
    if len(users) != 1:

def register(name, password) -> (bool, str):
    connection = db.connect('database.db')
    cursor = connection.execute('select * from users where name = ?', (name,))
    users = cursor.fetchall()
    if len(users) != 0:
        return False, 'username taken'
    cursor = connection.execute('select * from users where password = ?', (password,))
    passwords = cursor.fetchall()
    if len(passwords)!=0:
        return False, 'password taken'
    cursor = connection.execute("INSERT INTO users VALUES ('?', '?')", (name, password))
    connection.commit()
    connection.close()
