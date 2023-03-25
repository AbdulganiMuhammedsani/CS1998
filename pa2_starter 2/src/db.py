import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Venmo app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Secures a connection with the database and
        stores it in an instance variable
        """

        self.conn = sqlite3.connect(
            "todo.db", check_same_thread=False
        )

        # self.delete_user_table()
        self.create_user_table()

    def create_user_table(self):
        """
        Using SQL, create user table
        """

        try:
            self.conn.execute(
                """
                CREATE TABLE user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance OPTIONAL INTEGER

                );
                """
            )
        except Exception as e:
            print(e)

    def delete_user_table(self):
        """
        Using SQL, deletes a user table
        """

        self.conn.execute("DROP TABLE IF EXISTS task;")

    def get_all_users(self):
        """
        Using SQL, gets all users in the user table
        """

        cursor = self.conn.execute("SELECT * FROM user;")
        users = []

        for row in cursor:
            users.append({"id" : row[0], "name": row[1], "username": row[2]}) 
        return users
    
    def insert_user_table(self, name, username, balance):
        """
        Using SQL, adds a new user in the task table
        """
        cursor = self.conn.execute("INSERT INTO user (name, username, balance) VALUES (?, ?, ?);", (name, username, balance))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, id):
        """
        Using SQL, gets a user by ID
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE ID = ?;", (id,))

        for row in cursor:
            return {"id" : row[0], "name": row[1], "username": row[2], "balance": row[3]}
        return None
    
    def update_user_by_id(self, id, name, username, balance):
        """
        Using SQL, updates a task by ID
        """
        self.conn.execute(
            """
            UPDATE user
            SET name = ?, username = ?, balance = ?
            WHERE id = ?;
            """,
            (name, username, balance, id)
        )
        self.conn.commit()
     
    def delete_user_by_id(self, id):
        """
        Using SQL, deletes a user by id
        """
        self.conn.execute(
            """
            DELETE FROM user
            WHERE id = ?;
            """,
            (id,)
        )

        self.conn.commit()



# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
