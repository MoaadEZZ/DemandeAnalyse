import random
from datetime import datetime
import database
from table_etat import Table_etat
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from vars import APP_PASSWORD, EMAIL_SENDER

limit = "100"

def reorder_data(data):
    if len(data) == 0:
        return {}
    cols = data[0].keys()
    new_data = {}
    for e in cols:
        new_data[e] = [data[i][e] for i in range(len(data))]
    return new_data

def load_data():
    data = {}
    demandes = Demande.get_all_demande()
    for col in database.cols_demande.keys():
        data[col] = [demandes[i][col] for i in range(len(demandes))]
    return data

class Demande:
    def __init__(self, ppr=None, nom=None, prenom=None, description=None, bureau=None, direction=None, mail=None, o=None):
        self.PPR = ppr
        self.objet = o
        self.nom = nom
        self.prenom = prenom
        self.description = description
        self.etat = 1
        self.bureau = bureau
        self.direction = direction
        self.code = random_code()
        while Demande.get_demande(self.code) != None:
            self.code = random_code()
        self.mail = mail
        self.date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.date)
        self.table_etat = Table_etat(self.code, self.etat, "")
        

    def insert_demande(self):
        query = """INSERT INTO demande (code, objet, ppr, nom, prenom, description, date_demande, etat, bureau, direction, mail)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (self.code, self.objet, self.PPR, self.nom, self.prenom, self.description, self.date, self.etat, self.bureau, self.direction, self.mail)
        database.cursor.execute(query, values)
        database.conn.commit()
        self.table_etat.insert_demande()
        self.send_code_to_mail()


    def send_code_to_mail(self):
        msg = MIMEMultipart()
        recipients = [EMAIL_SENDER, self.mail]
        content = f"""\n
    Bonjour,

    Le code de la demande avec l'objet '{self.objet}' : '{self.code}'.

    Cordialement.

    P.S: veuillez ne pas répondre à ce mail."""
        msg['Subject'] = "Code de demande"
        msg['From'] = EMAIL_SENDER
        msg['To'] = ', '.join(recipients)

        msg.attach(MIMEText(content, 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_SENDER, APP_PASSWORD)
                server.sendmail(EMAIL_SENDER, recipients, msg.as_string())
            print("✅ Email envoyé avec succès.")
        except Exception as e:
            print(f"❌ Erreur d'envoi d'email : {e}")

    @staticmethod
    def get_demande(code):
        query = "SELECT * FROM demande WHERE code = %s"
        database.cursor.execute(query, code)
        return database.cursor.fetchone()
    
    @staticmethod
    def get_demande_by_ppr(ppr):
        query = "SELECT * FROM demande WHERE ppr = %s LIMIT "+limit
        database.cursor.execute(query, (ppr,))
        return database.cursor.fetchall()

    @staticmethod
    def get_all_demande():
        query = "SELECT * FROM demande LIMIT "+limit
        database.cursor.execute(query)
        return database.cursor.fetchall()

    @staticmethod
    def update_demande(code, o=None, nom=None, prenom=None, description=None, etat=None, bureau=None, direction=None, mail=None, description_tech=None):
        fields = []
        values = []
        if o is not None:
            fields.append("objet = %s")
            values.append(o)
        if nom is not None:
            fields.append("nom = %s")
            values.append(nom)
        if prenom is not None:
            fields.append("prenom = %s")
            values.append(prenom)
        if description is not None:
            fields.append("description = %s")
            values.append(description)
        if etat is not None:
            fields.append("etat = %s")
            values.append(etat)
        if bureau is not None:
            fields.append("bureau = %s")
            values.append(bureau)
        if direction is not None:
            fields.append("direction = %s")
            values.append(direction)
        if mail is not None:
            fields.append("mail = %s")
            values.append(mail)

        if fields:
            query = f"UPDATE demande SET {', '.join(fields)} WHERE code = %s"
            values.append(code)
            database.cursor.execute(query, tuple(values))
            database.conn.commit()
            Table_etat(code=code, etat=etat, description=description_tech).insert_demande()

    @staticmethod
    def get_past_demandes(ppr, date_demande):
        query = "SELECT * FROM demande WHERE ppr = %s AND date_demande < %s ORDER BY date_demande DESC;"
        database.cursor.execute(query, (ppr, date_demande))
        return database.cursor.fetchall()

def random_code():
    code = ""
    for i in range(12):
        r = random.randint(0, 30)
        if r < 10:
            code += chr(random.randint(97, 122))
        elif 10 <= r < 20:
            code += chr(random.randint(65, 90))
        else:
            code += chr(random.randint(49, 57))
    return code
