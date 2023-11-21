import socket as sck
import sqlite3 as sql
from threading import Thread

class Client(Thread):
    def __init__(self, conn: sck.socket):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        with sql.connect('fiumi.db') as db:
            try:
                while True:
                    codFiume = self.conn.recv(4096).decode()
                    print(codFiume)
                    
                    cur = db.cursor()

                    if 1 < int(codFiume) < 10:
                        fiume = cur.execute("SELECT fiume FROM livelli WHERE id_stazione=?", (codFiume,)).fetchall()
                        print(fiume[0][0])
                        self.conn.sendall(fiume[0][0].encode())
                    
                    limite1 = cur.execute("SELECT livello FROM livelli WHERE id_stazione=?", (codFiume,)).fetchall()
                    limite = limite1[0][0]
                    print(limite)
                    
                    loc1 = cur.execute("SELECT localita FROM livelli WHERE id_stazione=?", (codFiume,)).fetchall()
                    loc = loc1[0][0]
                    print(loc)
                    
                    lvl = self.conn.recv(4096).decode()
                    data = self.conn.recv(4096).decode()
                    
                    percentuale = int(lvl) / limite
                    #print(percentuale)
                    if percentuale < 0.30:
                        self.conn.sendall("Messaggio ricevuto correttamente".encode())
                    elif 0.30 <= percentuale < 0.70:
                        self.conn.sendall("Messaggio ricevuto correttamente".encode())
                        print(f"PERICOLO IMMINENTE! Presso fiume: {fiume[0][0]}, in località: {loc}, in data e ora: {data}")
                    elif percentuale >= 0.70:
                        self.conn.sendall("sirena".encode())
                        print(f"INONDAZIONE IN CORSO! Presso fiume: {fiume[0][0]}, in località: {loc}, in data e ora: {data}")
                                
            except sql.Error as e:
                print(f"Errore SQL: {e}")
            except Exception as e:
                print(f"Errore: {e}")
            finally:
                self.conn.close()

# Configurazione del server socket
server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
server.bind(('0.0.0.0', 8000))

# Ciclo infinito per accettare connessioni dai client
try:
    while True:
        server.listen()
        conn, addr = server.accept()
        cl = Client(conn)
        cl.start()
except KeyboardInterrupt:
    print("Server interrotto.")
    server.close()

