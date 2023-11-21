import socket as sck
import time
import datetime

cl = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

# Connette il socket al server locale sulla porta 8000
cl.connect(('localhost', 8000))

TIME = 15  # Tempo in secondi configurabile

while True:
    # Invio primo messaggio per ottenere il fiume
    cod = input('Inserisci il codice località (da 1 a 10) per assegnare il fiume: ')
    cl.sendall(cod.encode())

    # Riceve il fiume dal server
    fiume = cl.recv(4096).decode()
    print(fiume)

    # Richiede l'input all'utente
    val = input('Inserisci il livello: ')
    current_time = datetime.datetime.now()
    print(current_time)

    # Invia la richiesta al server
    cl.sendall(val.encode())
    cl.sendall(current_time.strftime('%Y-%m-%d %H:%M:%S').encode())  # Invia data e ora formattate

    # Riceve e stampa la risposta dal server per avvenuto invio dati con controllo allarme sirena
    risp = cl.recv(4096).decode()
    print(risp)
    if risp == "sirena":
        print("Sirena di emergenza attiva:")
        for i in range(0, 10):
            print("ROSSO")
            print("VERDE")

    # Attesa tempo impostato
    time.sleep(TIME)
