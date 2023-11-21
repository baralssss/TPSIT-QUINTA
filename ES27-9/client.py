# Importa le classi necessarie dalla libreria socket
from socket import socket, AF_INET, SOCK_STREAM

# Crea un oggetto socket per la comunicazione tramite IPv4 e TCP
client = socket(AF_INET, SOCK_STREAM)

# Stabilisce una connessione al server specificato (IP: '192.168.1.147', Porta: 8880)
client.connect(('192.168.1.147', 8880))

# Ciclo infinito per mantenere aperta la connessione e consentire l'invio di comandi
while True:
    # Ottiene l'input dall'utente, invia il comando al server dopo la codifica
    client.sendall(input('Inserisci un comando: ').encode())
    #print(client.recv(4096).decode())
