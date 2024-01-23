# Importa i moduli e le librerie necessarie
from flask import Flask, render_template, redirect, url_for, make_response, request
import sqlite3
import AlphaBot
import time
import random
import string
from re import U
import hashlib
from datetime import datetime

# Imposta l'indirizzo IP del robot
IP_ROBOT = '192.168.1.137'

# Crea un'istanza dell'applicazione Flask
app = Flask(__name__)

# Crea un'istanza della classe AlphaBot per controllare il robot
r = AlphaBot.AlphaBot()
#r = None

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
            if completion == True:
                return True
    # Chiudi la connessione al database
    cur.close()
    con.close()

# Funzione per verificare se la password fornita corrisponde alla password memorizzata
def check_password(hashed_password, user_password):
    def hash_password(user_password):
        # Crea un oggetto hash SHA-256
        sha256 = hashlib.sha256()

        # Aggiungi la password al nostro oggetto hash
        sha256.update(user_password.encode('utf-8'))

        # Restituisci la rappresentazione esadecimale dell'hash
        user_password_hashed = sha256.hexdigest()
    
        return user_password_hashed

    
    user_password_hashed = hash_password(user_password)
    if user_password_hashed == hashed_password:
        return True
    else:
        print("Error: User password")
        
        
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
        if completion == True:
            usernameV = request.cookies.get('username')
            usernameV = username
            print(usernameV)
            if usernameV=="john":
                resp = make_response(redirect(url_for("indexRIS")))
                resp.set_cookie('username', 'john')
                return resp
            else:
                #settare il cookie
                resp = make_response(redirect(url_for("index")))
                resp.set_cookie('username', 'utentegenerico')
                return resp
        # Se il login non ha avuto successo, imposta un messaggio di errore
        else:
            error = 'Credenziali non valide. Riprova.'
    # Renderizza il template login.html con il messaggio di errore
    return render_template('login.html', error=error)

def WonDB(user, msg, timeR):
    con = sqlite3.connect('./db.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO Movimenti (USERNAME, MOVIMENTO, DATAora) VALUES ('{user}', '{msg}', '{timeR}');")
    cur.close()
    con.commit()
    con.close()

def realTime():
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

# Route per la pagina principale
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = "mario"
    error = None
    # Verifica se il metodo della richiesta è POST (invio del modulo)
    if request.method == 'POST':
        # Elabora i dati del modulo in base al pulsante premuto
        if request.form.get('F') == 'Forward':
            msg = 'Avanti'
            print(msg)
            r.backward()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('B') == 'Backward':
            msg = 'Indietro'
            print(msg)
            r.forward()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('S') == 'Stop':
            msg = 'Stop'
            print(msg)
            r.stop()
            time.sleep(1)
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('R') == 'Right':
            msg = 'Destra'
            print(msg)
            r.right()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('L') == 'Left':
            msg = 'Sinistra'
            print(msg)
            r.left()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
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

# Route per la pagina principale
@app.route('/indexRIS', methods=['GET', 'POST'])
def indexRIS():
    user = 'john'
    error = None
    # Verifica se il metodo della richiesta è POST (invio del modulo)
    if request.method == 'POST':
        # Elabora i dati del modulo in base al pulsante premuto
        if request.form.get('F') == 'Forward':
            msg = 'Avanti'
            print(msg)
            r.backward()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('B') == 'Backward':
            msg = 'Indietro'
            print(msg)
            r.forward()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('S') == 'Stop':
            msg = 'Stop'
            print(msg)
            r.stop()
            time.sleep(1)
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('R') == 'Right':
            msg = 'Destra'
            print(msg)
            r.right()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
        elif request.form.get('L') == 'Left':
            msg = 'Sinistra'
            print(msg)
            r.left()
            time.sleep(1)
            r.stop()
            timeR = realTime()
            WonDB(user, msg, timeR)
        else:
            print("Sconosciuto")
    # Verifica se il metodo della richiesta è GET (caricamento iniziale della pagina)
    elif request.method == 'GET':
        # Renderizza il template index.html
        return render_template("indexRIS.html")
        # Stampa il token (Nota: Questa riga non verrà mai eseguita, poiché è dopo la dichiarazione di ritorno)
        print(token)
    # Renderizza il template index.html
    return render_template("indexRIS.html")


# Esegui l'applicazione Flask
if __name__ == '__main__':
    app.run(debug=True, host=IP_ROBOT, port=5000)
