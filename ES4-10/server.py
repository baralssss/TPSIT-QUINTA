import AlphaBot as ab
import socket as sck
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO

# Definizione dei pin per i sensori IR
DR = 16
DL = 19

# Variabili globali per la gestione dello stato del robot
IN_EMERGENZA = False
IN_AZIONE = False
IS_BACK = False

# Classe per il thread dei sensori IR
class Sensori(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        # Inizializzazione dei GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

        emergenza = False
        global IN_EMERGENZA
        global IN_AZIONE
        global susina

        try:
            while True:
                # Controlla i sensori solo se il robot è in azione e non è in stato di emergenza o retrocesso
                if not IN_AZIONE or IN_EMERGENZA or IS_BACK:
                    continue

                # Leggi lo stato dei sensori
                DR_status = GPIO.input(DR)
                DL_status = GPIO.input(DL)

                # Gestisci l'emergenza in base allo stato dei sensori
                if ((DL_status == 1) and (DR_status == 0) and not IN_EMERGENZA):
                    susina.stop()
                    IN_EMERGENZA = True
                    conn.sendall('EMERGENZA: gira a sinistra'.encode())
                elif ((DL_status == 0) and (DR_status == 1) and not IN_EMERGENZA):
                    susina.stop()
                    IN_EMERGENZA = True
                    conn.sendall('EMERGENZA: gira a destra'.encode())
                elif ((DL_status == 0) and (DR_status == 0) and not IN_EMERGENZA):
                    susina.stop()
                    IN_EMERGENZA = True
                    conn.sendall('EMERGENZA: vai indietro'.encode())

        except KeyboardInterrupt:
            GPIO.cleanup()

# Inizializzazione del robot AlphaBot
susina = ab.AlphaBot()

# Inizializzazione del socket del server
socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
socket.bind(('0.0.0.0', 8888))

socket.listen()
conn, addr = socket.accept()

# Dizionario per mappare i comandi di movimento
move = {'f': susina.forward, 'b': susina.backward, 'l': susina.right, 'r': susina.left}

# Creazione e avvio del thread per i sensori
s = Sensori(conn)
s.start()

while True:
    # Ricezione dei comandi dal client
    data = conn.recv(4096).decode()
    
    # Verifica che il messaggio contenga il carattere separatore ';'
    if ';' not in data:
        conn.sendall(f'il messaggio inviato deve contenere il carattere separatore {SEP}'.encode())
        continue

    # Split dei dati
    datas = data.split(';')

    # Verifica e esecuzione del comando di movimento
    if datas[0].lower() in move:
        if datas[0].lower() == 'b':
            IS_BACK = True

        move[datas[0].lower()]()
        IN_AZIONE = True
        sleep(float(datas[1]))

        # Stop del robot se non è in stato di emergenza
        if not IN_EMERGENZA:
            susina.stop()
            conn.sendall('comando fatto'.encode())

        IN_EMERGENZA = False
        IN_AZIONE = False
        IS_BACK = False
    else:
        conn.sendall(f"il primo parametro passato deve essere uno tra {'-'.join(list(move.keys()))}".encode())
