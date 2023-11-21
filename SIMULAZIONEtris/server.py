import socket as sck
from threading import Thread

# Costanti per i messaggi di gioco
MESSAGE_TURN = '__your_turn__'
TIME_TO_MOVE = '__time_to_move__'
STR_DRAW = '__draw__'
MESSAGE_END_GAME = '__end_game__'

# Inizializzazione della tavola di gioco
table = [' ', 'x', ' ', 'o', 'o', 'o', ' ', ' ', 'x']

# Inizializzazione delle variabili globali per i giocatori, il turno e il vincitore
gioc1, gioc2 = None, None
turnOf, winner = None, None


class Client(Thread):
    def __init__(self, conn: sck.socket, symbol):
        Thread.__init__(self)
        self.conn = conn
        self.symbol = symbol

    def closeGame(self):
        global winner, gioc2, gioc1

        # Invia il messaggio di fine partita al client
        if winner == STR_DRAW:
            self.conn.sendall(f'{MESSAGE_END_GAME}La partita è terminata in parità'.encode())
        elif winner == self:
            self.conn.sendall(f'{MESSAGE_END_GAME}COMPLIMENTI, HAI VINTO!!'.encode())
        else:
            self.conn.sendall(f'{MESSAGE_END_GAME}Sorry, hai perso'.encode())

        # Chiudi la connessione del client e imposta il giocatore a None
        self.conn.close()
        if self == gioc1:
            gioc1 = None
        else:
            gioc2 = None

    def run(self):
        global gioc1, turnOf, gioc2, winner

        try:
            # Invia il simbolo del giocatore e inizia la partita
            self.conn.sendall(f'Il tuo simbolo è: {self.symbol}\nINIZIO PARTITA!!!'.encode())

            while True:
                # Controlla se c'è un vincitore o se è il turno del giocatore corrente
                if winner is not None:
                    break
                elif self == turnOf:
                    # Invia lo stato attuale della tavola di gioco
                    self.conn.sendall(f"{MESSAGE_TURN}{'--'.join(table)}".encode())

                    # Ricevi la mossa del giocatore corrente
                    data = self.conn.recv(4096).decode()

                    # Controlla se è il momento di effettuare una mossa
                    if TIME_TO_MOVE in data:
                        ind = int(data[len(TIME_TO_MOVE):])
                        table[ind] = self.symbol

                        # Controlla il vincitore della partita
                        winner = getWinner()

                        # Se non c'è un vincitore, cambia il turno all'altro giocatore
                        if winner is None:
                            turnOf = gioc2 if self == gioc1 else gioc1
                        else:
                            turnOf = None

        except:
            # Gestisce le eccezioni durante l'esecuzione del thread
            conn.close()
            if self == gioc1:
                gioc1 = None
            else:
                gioc2 = None


def getWinner():
    global table

    # Controlla le righe e le colonne per determinare il vincitore
    for n in range(3):
        if table[n * 3] == table[n * 3 + 1] and table[n * 3] == table[n * 3 + 2] and table[n * 3] != ' ':
            return gioc1 if gioc1.symbol == table[n * 3] else gioc2
        elif table[n] == table[n + 3] and table[n] == table[n + 6] and table[n] != ' ':
            return gioc1 if gioc1.symbol == table[n] else gioc2

    # Controlla le diagonali per determinare il vincitore
    if table[0] == table[4] and table[0] == table[8] and table[0] != ' ':
        return gioc1 if gioc1.symbol == table[0] else gioc2
    elif table[2] == table[4] and table[2] == table[6] and table[2] != ' ':
        return gioc1 if gioc1.symbol == table[2] else gioc2

    # Se non c'è un vincitore, controlla se la partita è finita in pareggio
    return STR_DRAW if table.count(' ') == 0 else None


# Inizializzazione del socket del server
server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
server.bind(('0.0.0.0', 8000))

try:
    while True:
        # Controlla se uno dei giocatori è ancora disponibile o se c'è un vincitore
        if gioc1 is None or gioc2 is None:
            winner = None
            server.listen()
            conn, addr = server.accept()
            if gioc1 is None:
                gioc1 = Client(conn, 'x')
            else:
                gioc2 = Client(conn, 'o')
        elif winner is not None:
            # Chiudi la partita se c'è un vincitore
            gioc1.closeGame()
            gioc2.closeGame()
        elif turnOf is None:
            # Inizia il gioco assegnando il turno al giocatore 1 e avviando i thread
            turnOf = gioc1
            gioc1.start()
            gioc2.start()

except:
    # Gestisce le eccezioni durante l'esecuzione del server
    server.close()
