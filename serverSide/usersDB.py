import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Users:

    def __init__(self):
        self.connection = sqlite3.connect("usersDB.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        return

    # def userExists(self, user_id):
    #     data = [user_id]
    #     self.cursor.execute("SELECT * FROM users WHERE ID = ?", data)
    #     boo = False
    #     result = self.cursor.fetchone()
    #     if result:
    #         boo = True

    #     return boo

    def getUserByUsername(self, username):
        data = [username]
        self.cursor.execute("SELECT * FROM users WHERE username = ?", data)
        result = self.cursor.fetchall()
        return result

    def addUser(self, username, website, counter, passwordLength, symbols, uppercase, lowercase, numbers):
        data = [username, website, counter, passwordLength, symbols, uppercase, lowercase, numbers]
        user = self.cursor.execute("INSERT INTO users (username, website, count, length, symbols, uppercase, lowercase, numbers) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        self.connection.commit()
        return

    def getAllUsers(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def createTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, website TEXT, count TEXT, length INTEGER, symbols TEXT, uppercase BOOLEAN, lowercase BOOLEAN, numbers BOOLEAN)")
        self.connection.commit()
        return
