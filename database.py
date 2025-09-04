import pymysql
import vars

conn = pymysql.connect(
    host=vars.DB_HOST,
    user=vars.DB_USER,
    password=vars.DB_PASSWORD,
    database="Analyse_Demande",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

cols_demande = {"code": "varchar(12) PRIMARY KEY", "objet": "text", "ppr": "VARCHAR(10)", "nom": "VARCHAR(30)", 
        "prenom": "VARCHAR(30)", "description": "text", "date_demande": "DATETIME", "etat": "INT", "bureau": "VARCHAR(10)", 
        "direction": "VARCHAR(30)", "mail": "VARCHAR(100)"}
add_lines_demande = []
query = "CREATE TABLE IF NOT EXISTS demande (\n"
i=0
for key in cols_demande.keys():
    query += key+" "+cols_demande[key]
    i += 1
    if i < len(cols_demande): query += ",\n"
for e in add_lines_demande:
    query += ",\n"+e
query +="\n);"
cursor.execute(query)
conn.commit()


cols_etat = {"id": "INT AUTO_INCREMENT PRIMARY KEY", "code": "varchar(12)", "etat": "INT", "date_etat": "DATETIME", "description": "text"}
add_lines_etat = ["FOREIGN KEY (code) REFERENCES demande(code)"]
query = "CREATE TABLE IF NOT EXISTS table_etat (\n"
i = 0
for key in cols_etat.keys():
    query += key+" "+cols_etat[key]
    i += 1
    if i < len(cols_etat): query += ",\n"
for e in add_lines_etat:
    query += ",\n"+e
query += "\n);"
cursor.execute(query)
conn.commit()
