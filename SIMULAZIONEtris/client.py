import socket as sck

# Costanti per la gestione del gioco
DISTANCE_CAMPI = 5
MESSAGE_YOUR_TURN = '__your_turn__'
TIME_TO_MOVE = '__time_to_move__'
MESSAGE_END_GAME = '__end_game__'

# Funzione per stampare il campo di gioco
def printCampo(campo):
    righe = []
    for n in range(3):
        c = campo[n * 3: n * 3 + 3]
        line = '|'.join([f' {v} ' for v in c])
        indexes = '|'.join(f' {i + 3 * n} ' for i in range(len(c)))
        righe.append(line + (' ' * DISTANCE_CAMPI) + indexes)

    print(('\n---+---+---' + (' ' * DISTANCE_CAMPI) + '--+---+---\n').join(righe))
    print()

# Inizializzazione del socket del client
cl = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
cl.connect(('localhost', 8000))

# Ricevi il messaggio di benvenuto dal server
print(cl.recv(4096).decode())

try:
    while True:
        # Ricevi il messaggio dal server
        mess = cl.recv(4096).decode()

        if MESSAGE_YOUR_TURN in mess:
            # Se è il turno del giocatore, stampa il campo di gioco e aspetta la mossa del giocatore
            mess = mess[len(MESSAGE_YOUR_TURN):].split('--')
            printCampo(mess)

            mossa = None
            while True:
                mossa = int(input('Inserisci il numero in base alla casella: '))
                if mossa >= len(mess) or mess[mossa] != ' ':
                    print('Mossa impossibile da eseguire, ', end='')
                else:
                    print('Attendi la mossa dell\'avversario\n')
                    break
            # Invia la mossa al server
            cl.sendall(f'{TIME_TO_MOVE}{mossa}'.encode())
        elif MESSAGE_END_GAME in mess:
            # Se la partita è terminata, stampa il messaggio finale e chiudi la connessione
            print(mess[len(MESSAGE_END_GAME):])
            cl.sendall(''.encode())
            cl.close()
except:
    # Gestisce le eccezioni durante l'esecuzione del client
    cl.close()
