import sqlite3
import csv
import urllib.request
import os
from datetime import date
from tkinter import *


today = str(date.today())


class Updating:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def update(self):
        # Download CSV file
        url = "http://ec.europa.eu/growth/tools-databases/cosing/pdf/COSING_Ingredients-Fragrance%20Inventory_v2.csv"
        urllib.request.urlretrieve(url, "db_update.csv")

        # Drop and create the table
        self.cur.execute('DROP TABLE IF EXISTS cosing')
        self.cur.execute(
            'CREATE TABLE cosing (Ref_No, INCI_name, INN, PhEur, CAS_No, EC_No, Chem_Name, Restriction, Function, Update_Date)')
        self.conn.commit()

        # Load the CSV file into CSV reader
        with open('db_update.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            all(next(csv_file) for i in range(9))
            for t in csv_reader:
                try:
                    self.cur.execute('INSERT INTO cosing VALUES (?,?,?,?,?,?,?,?,?,?)', t)
                except sqlite3.ProgrammingError as e:
                    pass

        with open('db_update.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            date_row = [row for idx, row in enumerate(csv_reader) if idx == 6]
            current_update = (str(date_row[0][1]))[-10:]
            self.cur.execute("UPDATE update_data SET Data = ?, Last = ?", (today, current_update))

        # Close the csv file, commit changes, and close the connection
        csv_file.close()
        self.csv_delete("db_update.csv")
        self.conn.commit()

    def present_db(self):
        self.cur.execute('SELECT Last FROM update_data where No=1')
        rows = self.cur.fetchall()
        return rows[0][0]

    def last_updating(self):
        self.cur.execute('SELECT Data FROM update_data where No=1')
        row = self.cur.fetchall()
        return row[0][0]

    def csv_delete(csv_name):
        if os.path.exists(csv_name):
            os.remove(csv_name)
        else:
            pass

    def __del__(self):
        self.conn.close()


def date():
    url = "http://ec.europa.eu/growth/tools-databases/cosing/pdf/COSING_Ingredients-Fragrance%20Inventory_v2.csv"
    urllib.request.urlretrieve(url, "date.csv")

    with open('date.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        interestingrows = [row for idx, row in enumerate(csv_reader) if idx == 6]
        date = (str(interestingrows[0][1]))[-10:]
    Updating.csv_delete("date.csv")

    return date
