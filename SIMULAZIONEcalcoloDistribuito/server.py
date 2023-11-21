# Importa la libreria socket con alias 'sck' per semplificare il riferimento
import socket as sck

# Importa la libreria sqlite3 con alias 'sql'
import sqlite3 as sql

# Importa la classe Thread dal modulo threading
from threading import Thread

# Importa la funzione sleep dal modulo time
from time import sleep

# Classe Client che eredita da Thread
class Client(Thread):
    def __init__(self, id, conn: sck.socket, addr):
        Thread.__init__(self)
        self.id = id
        self.conn = conn
        self.addr = addr

    def run(self):
        global operations

        try:
            # Invia l'id del client al client stesso
            self.conn.sendall(f'id del client: {self.id}'.encode())

            # Ciclo attraverso le operazioni associate al client
            for diz in operations:
                if diz['client'] == self.id:
                    # Invia l'operazione al client
                    self.conn.sendall(diz['operation'].encode())

                    # Riceve e stampa il risultato dell'operazione dal client
                    print(f"{diz['operation']} = {self.conn.recv(4096).decode()} from {self.addr[0]} - {self.addr[1]}")

            # Invia 'exit' al client e chiude la connessione
            self.conn.sendall('exit'.encode())
            self.conn.close()
        except:
            # In caso di errore, chiude la connessione
            conn.close()

# Connessione al database SQLite e recupero delle operazioni
db = sql.connect('operations.db')
cur = db.cursor()
operations = []
for id, client, op in cur.execute('SELECT * FROM operations').fetchall():
    operations.append({'id': id, 'client': client, 'operation': op})
cur.close()
db.close()

# Creazione del socket del server
server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))

# Inizializzazione del contatore dei client
n_cl = 1

# Ciclo principale del server
while True:
    # Accetta connessioni in arrivo
    server.listen()
    conn, addr = server.accept()

    # Creazione di un nuovo thread per gestire il client
    cl = Client(n_cl, conn, addr)
    cl.start()

    # Incremento del contatore dei client
    n_cl += 1

# Chiusura del socket del server
server.close()
