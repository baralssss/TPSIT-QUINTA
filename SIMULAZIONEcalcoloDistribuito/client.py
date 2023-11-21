# Importa la libreria socket con alias 'sck' per semplificare il riferimento
import socket as sck

# Crea un oggetto socket per la comunicazione tramite IPv4 e TCP
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

# Connette il socket al server locale sulla porta 5000
s.connect(('localhost', 5000))

# Stampa il messaggio ricevuto dal server dopo la connessione
print(s.recv(4096).decode())

# Ciclo infinito per ricevere e inviare dati al server
while True:
    # Riceve dati dal server
    data = s.recv(4096).decode()

    # Controlla se il server ha inviato 'exit' per chiudere la connessione
    if data == 'exit':
        s.close()
        break
    else:
        # Stampa il messaggio ricevuto dal server
        print(f'>> {data}')

        # Esegue l'operazione definita nel messaggio usando 'eval'
        ris = eval(data)

        # Stampa il risultato dell'operazione
        print(ris)

        # Invia il risultato al server dopo la conversione in stringa
        s.sendall(f'{ris}'.encode())
