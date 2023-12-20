# Importa i moduli e le librerie necessarie
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import AlphaBot
import time
import random
import string

# Imposta l'indirizzo IP del robot
IP_ROBOT = '192.168.1.137'

# Crea un'istanza dell'applicazione Flask
app = Flask(__name__)

# Crea un'istanza della classe AlphaBot per controllare il robot
r = AlphaBot.AlphaBot()

# Funzione per generare una stringa casuale di caratteri alfanumerici
def strALF(lunghezza):
    caratteri = string.ascii_letters + string.digits
    return ''.join(random.choice(caratteri) for _ in range(lunghezza))

# Genera un token casuale e stampalo (a scopo di test)
lunghezza = 40
token = strALF(lunghezza)
print(token)

# Funzione per convalidare le credenziali di accesso contro il database
def validate(username, password):
    completion = False
    # Connetti al database
    con = sqlite3.connect('./db.db')
    cur = con.cursor()
    # Recupera tutti gli utenti dal database
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    # Verifica se lo username e la password forniti corrispondono a un utente nel database
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser == username:
            completion = check_password(dbPass, password)
    # Chiudi la connessione al database
    cur.close()
    con.close()
    return completion

# Funzione per verificare se la password fornita corrisponde alla password memorizzata
def check_password(hashed_password, user_password):
    return hashed_password == user_password

# Route per la pagina di login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    # Verifica se il metodo della richiesta è POST (invio del modulo)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Convalida le credenziali di accesso
        completion = validate(username, password)
        # Se il login non ha avuto successo, imposta un messaggio di errore
        if not completion:
            error = 'Credenziali non valide. Riprova.'
        else:
            # Reindirizza alla pagina principale in caso di login riuscito
            return redirect(url_for("index"))
    # Renderizza il template login.html con il messaggio di errore
    return render_template('login.html', error=error)

# Route per la pagina principale
@app.route('/index', methods=['GET', 'POST'])
def index():
    error = None
    # Verifica se il metodo della richiesta è POST (invio del modulo)
    if request.method == 'POST':
        # Elabora i dati del modulo in base al pulsante premuto
        if request.form.get('F') == 'Forward':
            print('Avanti')
            r.backward()
            time.sleep(1)
            r.stop()
        elif request.form.get('B') == 'Indietro':
            print('Indietro')
            r.forward()
            time.sleep(1)
            r.stop()
        elif request.form.get('S') == 'Stop':
            print('Stop')
            r.stop()
            time.sleep(1)
        elif request.form.get('R') == 'Destra':
            print('Destra')
            r.right()
            time.sleep(1)
            r.stop()
        elif request.form.get('L') == 'Sinistra':
            print('Sinistra')
            r.left()
            time.sleep(1)
            r.stop()
        else:
            print("Sconosciuto")
    # Verifica se il metodo della richiesta è GET (caricamento iniziale della pagina)
    elif request.method == 'GET':
        # Renderizza il template index.html
        return render_template("index.html")
        # Stampa il token (Nota: Questa riga non verrà mai eseguita, poiché è dopo la dichiarazione di ritorno)
        print(token)
    # Renderizza il template index.html
    return render_template("index.html")

# Esegui l'applicazione Flask
if __name__ == '__main__':
    app.run(debug=True, host=IP_ROBOT, port=5000)
