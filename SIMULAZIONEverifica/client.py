# Importa la libreria socket con alias 'sck' per semplificare il riferimento
import socket as sck

# Crea un oggetto socket per la comunicazione tramite IPv4 e TCP
cl = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

# Connette il socket al server locale sulla porta 8000
cl.connect(('localhost', 8000))

# Ciclo infinito per interagire con il server
while True:
    # Stampa le opzioni disponibili per l'utente
    print('cosa vuoi sapere:')
    print('se un file esiste                       -> filename;<<nome_del_file>>')
    print('il numero di frammenti di un file       -> nframm;<<nome_del_file>>')
    print('ip del frammento n al file f            -> getip;<<nome_del_file>>;<<num_frammento>>')
    print('tutti gli ip di ogni frammento del file -> eachip;<<nome_del_file>>')

    # Richiede l'input all'utente
    val = input('>> ')

    # Invia la richiesta al server
    cl.sendall(val.encode())

    # Riceve e stampa la risposta dal server
    print(cl.recv(4096).decode())
    print()
