import sqlite3
import hashlib


class Database():
    #magic strings
    insert = "INSERT INTO ? (email,password_hash,email_hash) VALUES (?,?,?)"
    select = "SELECT * FROM ? WHERE email=?"

    def __init__(self, database_path, default_table = None):
        self.database_path = database_path
        self._default_table = default_table
        self.database = sqlite3.connect(self.database_path)

    def set_default_table(self,default_table):
        self._default_table = default_table

    def add_user(self,email,password_hash,table = None):
        if table is not None and isinstance(table,str):
            current_table = table
        else:
            current_table = self._default_table
        cursor = self.database.cursor()

        email_hash = hashlib.sha256(email).hexdigest()
        cursor.execute(self.insert,current_table,(email,password_hash,email_hash))
        cursor.close()
    def search_database(self,email,table = None):
        if table is not None and isinstance(table, str):
            current_table = table
        else:
            current_table = self._default_table
        cursor = self.database.cursor()
        cursor.execute(self.select,current_table,email)
        user = cursor.fetchall()
        cursor.close()
        return user






