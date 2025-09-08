from flask import Flask, flash, render_template, request, redirect, url_for, session
from demande import Demande, reorder_data
from database import *
from table_etat import Table_etat
from datetime import *
from Model1 import Model_Prediction
import pandas as pd
import vars

model = Model_Prediction()
model.train() # a retirer en cas de test rapide de l'application et pour le debugage
app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes=10)

@app.before_request
def make_session_non_permanent():
    session.permanent = False
app.secret_key = vars.SESSION_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        ppr = request.form.get('ppr')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        description = request.form.get('description')
        bureau = request.form.get('bureau')
        direction = request.form.get('direction')
        mail = request.form.get('mail')
        o = request.form.get('objet')

        Demande(ppr, nom, prenom, description, bureau, direction, mail, o).insert_demande()
        flash("Demande envoyer.", "success")
    return redirect(url_for('index'))

@app.route('/suivi', methods=['GET', 'POST'])
def suivi():
    if request.method == 'POST':
        code = request.form['code']
        demande = Demande.get_demande(code)
        if demande:
            demande["etat_char"] = etat_from_nbr(demande["etat"])
            demande["date_demande"] = demande["date_demande"].date()
        return render_template('suivi.html', demande=demande, searched=code)
    return render_template('suivi.html', demandes=None, searched=None)

@app.route('/tech/historique', methods=['GET', 'POST'])
def tech():
    if not session.get("name"):
        session["path"] = "/tech/historique"
        return redirect("/tech/login")
    demandes = Table_etat.get_all_demandes()
    
    for i in range(len(demandes)):
        demandes[i]["description_demande"] = demandes[i]["demande.description"]
        demandes[i]["etat_char"] = etat_from_nbr(demandes[i]["etat"])

    demandes = pd.DataFrame(reorder_data(demandes))
    if len(demandes)==0:
        return render_template('tech_etat.html', demandes=demandes)
    if request.method == 'POST':
        code = request.form.get("code")
        if code:
            demandes = demandes[demandes["code"]==code]
            if len(demandes)!=0:
                flash("selection par Code.", "success")
            else:
                flash("Code '"+code+"' n'existe pas.", "danger")
            demandes = demandes.to_dict(orient='records')
            return render_template('tech_etat.html', demandes=demandes)
        ppr = request.form.get("ppr")
        demandes = demandes[demandes["ppr"]==ppr]
        if len(demandes)!=0:
                flash("selection par PPR.", "success")
        else:
            flash("PPR '"+ppr+"' n'existe pas.", "danger")
        
        demandes = demandes.to_dict(orient='records')
        return render_template('tech_etat.html', demandes=demandes)
    demandes = demandes.to_dict(orient='records')
    return render_template('tech_etat.html', demandes=demandes)

@app.route('/tech/traiter', methods=['GET', 'POST'])
def tech2():
    if not session.get("name"):
        session["path"] = "/tech/traiter"
        return redirect("/tech/login")
    global model
    model.predict()
    demandes = Demande.get_all_demande()
    for i in range(len(demandes)):
        demandes[i]["etat_char"] = etat_from_nbr(demandes[i]["etat"])
    demandes = pd.DataFrame(reorder_data(demandes))
    if len(model.df_pred)!=0:
        demandes = demandes.merge(model.df_pred[["code", "pred_proba", "pred_label"]], on="code", how="left")
    demandes = demandes.to_dict(orient='records')
    if request.method == 'POST':
        code = request.form['code']
        if code == '1':
            pred_refused = []
            pred_refused = model.df_pred[model.df_pred["pred_label"]==1][model.df_pred["etat"]==1]
            for i in range(len(pred_refused)):
                Demande.update_demande(code=pred_refused["code"], etat=4, description_tech="")
            if len(pred_refused) == 0:
                flash("Aucune prediction refuser a été detecter", "warning")
            else:
                flash("Predictions refuser ont été modifier.", "success")
            return render_template('tech_demandes.html', demandes=demandes)
        elif code == '0':
            pred_accept = []
            pred_accept = model.df_pred[model.df_pred["pred_label"]==0][model.df_pred["etat"]==1]
            for i in range(len(pred_accept)):
                Demande.update_demande(code=pred_accept["code"], etat=3, description_tech="")
            if len(pred_accept) == 0:
                flash("Aucune prediction accepter a été detecter.", "warning")
            else:
                flash("Predictions accepter ont été modifier.", "success")
            return render_template('tech_demandes.html', demandes=demandes)
        new_etat = request.form['etat']
        desc = request.form['description']
        Demande.update_demande(code=code, etat=new_etat, description_tech=desc)
        flash(f"Demande de code '{code}' a été modifier a l'état '{etat_from_nbr(new_etat)}'.", "success")
    return render_template('tech_demandes.html', demandes=demandes)

@app.route('/tech/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form["name"] == vars.ADMIN_LOGIN and request.form["password"] == vars.ADMIN_PASSWORD:
            session["name"] = request.form["name"]
            flash('Vous étez connecter.', "success")
            if session.get("path") == "/tech/historique":
                return redirect("/tech/historique")
            else:
                return redirect("/tech/traiter")
        flash('Mot de passe ou login erroné.', "danger")
    return render_template("tech_login.html")

@app.route('/tech/logout')
def logout():
    session.clear()
    return redirect("/")

def etat_from_nbr(etat):
    if etat == 1:
        return "Envoyer"
    if etat == 2:
        return "En cours de traitement"
    if etat == 3:
        return "Traité"
    if etat == 4:
        return "Refus"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


