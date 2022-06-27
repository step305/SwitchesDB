import sqlite3
import datetime
import Switch
from tkinter import messagebox


class SwitchDB:
    def __init__(self, path_to_base='database.db'):
        try:
            self.base_connection = sqlite3.connect(path_to_base)
            self.cursor = self.base_connection.cursor()
            sql_req = 'select sqlite_version();'
            self.cursor.execute(sql_req)
            record = self.cursor.fetchall()

            # create (if not exists) table for storing test runs ID
            sql_req = 'CREATE TABLE IF NOT EXISTS switches (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT DEFAULT 0,' \
                      'name INTEGER NOT NULL UNIQUE,' \
                      'r_on REAL NOT NULL,' \
                      'r_off REAL NOT NULL,' \
                      'threshold REAL NOT NULL,' \
                      'date TIMESTAMP NOT NULL);'
            self.cursor.execute(sql_req)
            self.base_connection.commit()

            self.cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror('Ошибка!', 'Error during connection to database: {}'.format(str(error)))

    def add(self, switch):
        try:
            self.cursor = self.base_connection.cursor()
            sql_req = 'INSERT OR REPLACE INTO switches (name, r_on, r_off, threshold, date) VALUES (?,?,?,?,?);'
            self.cursor.execute(sql_req, (switch.id,
                                          switch.r_on,
                                          switch.r_off,
                                          switch.threshold,
                                          datetime.datetime.now()))
            self.base_connection.commit()
            self.cursor.close()
        except sqlite3.Error as error:
            messagebox.showerror('Ошибка!', 'Error during storing switch parameters to database: {}'.format(str(error)))

    def get(self, name):
        try:

            self.cursor = self.base_connection.cursor()
            sql_req = 'SELECT r_on, r_off, threshold FROM switches WHERE name=?;'
            self.cursor.execute(sql_req, (name,))
            params = self.cursor.fetchone()
            if params:
                r_on, r_off, threshold = params
                switch = Switch.Switch(switch_id=name,
                                       r_on=r_on,
                                       r_off=r_off,
                                       threshold=threshold)
                return switch
            else:
                return False
        except sqlite3.Error as error:
            messagebox.showerror('Ошибка!', 'Error during fetching switch parameters '
                                            'from database: {}, {}'.format(name, str(error)))

    def get_last(self):
        try:
            self.cursor = self.base_connection.cursor()
            sql_req = 'SELECT name, r_on, r_off, threshold, MAX(date) FROM switches;'
            self.cursor.execute(sql_req)
            params = self.cursor.fetchone()
            if params:
                name, r_on, r_off, threshold, date = params
                switch = Switch.Switch(switch_id=name,
                                       r_on=r_on,
                                       r_off=r_off,
                                       threshold=threshold)
                return switch
            else:
                return False
        except sqlite3.Error as error:
            messagebox.showerror('Ошибка!', 'Error during fetching switch parameters '
                                            'from database: {}, {}'.format(str(error)))


    def __del__(self):
        if self.base_connection:
            self.base_connection.close()
