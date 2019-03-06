import sqlite3
class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cosing 
        (Ref_No INTEGER PRIMARY KEY, INCI_name TEXT, INN TEXT, 
        PhEur TEXT, CAS_No TEXT, EC_No TEXT, Chem_Name TEXT, 
        Restriction TEXT, Function TEXT, Update_Date TEXT)""")
        self.conn.commit()


    def view(self):
        self.cur.execute("SELECT * FROM cosing")
        rows = self.cur.fetchall()
        return rows

    def search(self, inci=""):
        self.cur.execute("SELECT * FROM cosing WHERE INCI_name = ? OR CAS_No = ?", (inci, inci))
        rows = self.cur.fetchall()
        return rows
        print(self.cur.execute("SELECT * FROM cosing WHERE INCI_name = ? OR CAS_No = ?", (inci, inci)))
   #destructor-->now we close the connection to our database here
    def __del__(self):
        self.conn.close()