import hashlib

def hash_password(password):
    # Crea un oggetto hash SHA-256
    sha256 = hashlib.sha256()

    # Aggiungi la password al nostro oggetto hash
    sha256.update(password.encode('utf-8'))

    # Restituisci la rappresentazione esadecimale dell'hash
    hashed_password = sha256.hexdigest()
    
    return hashed_password

# Esempio di utilizzo:
password_da_salvare = input("Inserisci la password :")
hashed_password = hash_password(password_da_salvare)

print(hashed_password)
