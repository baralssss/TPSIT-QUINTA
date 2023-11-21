# Importa la classe socket per la gestione delle connessioni di rete
from socket import socket, AF_INET, SOCK_STREAM

# Importa la classe Thread per gestire l'input e l'output in modo concorrente
from threading import Thread

# Crea un socket client per la comunicazione tramite IPv4 e TCP
client = socket(AF_INET, SOCK_STREAM)

# Stabilisce la connessione con il server specificato (IP: '192.168.1.147', Porta: 8888)
client.connect(('192.168.1.147', 8888))

# Ciclo infinito per mantenere la connessione e consentire l'invio di comandi
while True:
    # Ottiene l'input dall'utente, invia il comando al server dopo la codifica
    client.sendall(input('Inserisci un comando: ').encode())
    
    # Riceve la risposta dal server (massimo 4096 byte) e la decodifica
    print(client.recv(4096).decode())
