import database
from datetime import datetime

class Table_etat:
    def __init__(self, code, etat, description):
        self.code = code
        self.etat = etat
        self.date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.description = description

    def insert_demande(self):
        query = """INSERT INTO table_etat (code, etat, date_etat, description)
                   VALUES (%s, %s, %s, %s)"""
        values = (self.code, self.etat, self.date, self.description)

        database.cursor.execute(query, values)
        database.conn.commit()

    def get_all_demandes():
        database.cursor.execute("SELECT * FROM `table_etat` JOIN `demande` ON table_etat.code=demande.code ORDER BY table_etat.date_etat LIMIT 100")
        return database.cursor.fetchall()
    

