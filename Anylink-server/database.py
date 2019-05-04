import sqlite3
import hashlib


class Database():
    #magic strings
    insert = "INSERT INTO {table} (email,password_hash,email_hash) VALUES (?,?,?)"
    select = "SELECT * FROM {table} WHERE email=?"

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
        insert = self.insert.format(table=current_table)

        email_hash = hashlib.sha256(email.encode("utf-8")).hexdigest()
        cursor.execute(insert,(email,password_hash,email_hash))
        self.database.commit()
        cursor.close()
    def search_database(self,email,table = None):
        if table is not None and isinstance(table, str):
            current_table = table
        else:
            current_table = self._default_table
        cursor = self.database.cursor()
        select = self.select.format(table=current_table)
        cursor.execute(select,(email,))
        user = cursor.fetchone()
        res_email = user[0]
        res_passwh = user[1]
        res_emailh = user[2]
        user_dict = {"email":res_email,"password_hash":res_passwh,"email_hash":res_emailh}
        cursor.close()
        return user_dict






