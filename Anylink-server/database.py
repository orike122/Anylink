import sqlite3
import hashlib
import typing

class Database():
    """Database class, to manage users database"""
    #----------magic strings----------
    insert = "INSERT INTO {table} (email,password_hash,email_hash) VALUES (?,?,?)"
    select = "SELECT * FROM {table} WHERE email=?"
    # --------------------------------

    def __init__(self, database_path: str, default_table: str = None):
        """
        C'tor of Database class
        :param database_path: Path where the DB is located
        :param default_table: Optional: Default table for querying
        """
        self.database_path = database_path
        self._default_table = default_table
        self.database = sqlite3.connect(self.database_path,check_same_thread=False)

    def set_default_table(self,default_table: str):
        """
        Sets the default table
        :param default_table: Default table for querying
        """
        self._default_table = default_table

    def add_user(self,email: str,password_hash: str,table: str = None):
        """
        Adds new user to DB
        :param email: user's email
        :param password_hash: user's password hash
        :param table: Optional: Default table for querying
        """
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

    def search_database(self,email: str,table: str = None) -> typing.Dict[str,str]:
        """
        Preform a select query to DB
        :param email: user's email
        :param table: Optional: Default table for querying
        :return: Dict of user details of None if user not found
        """
        if table is not None and isinstance(table, str):
            current_table = table
        else:
            current_table = self._default_table
        cursor = self.database.cursor()
        select = self.select.format(table=current_table)
        cursor.execute(select,(email,))
        user = cursor.fetchone()
        if user is not None:
            res_email = user[0]
            res_passwh = user[1]
            res_emailh = user[2]
            user_dict = {"email":res_email,"password_hash":res_passwh,"email_hash":res_emailh}
            cursor.close()
            return user_dict
        else:
            return user






