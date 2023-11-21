import socket
import time
import RPi.GPIO as GPIO

# Costanti
PORT = 8000
HOST = "0.0.0.0"
MY_ADDRESS = (HOST, PORT)

# Classe per il controllo del robot AlphaBot
class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        # Definizione dei pin del motore
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in4
        self.IN4 = in3
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        # Configurazione dei pin GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def forward(self):
        # Movimento in avanti
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        # Stop
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self):
        # Movimento all'indietro
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def left(self, speed=30):
        # Svolta a sinistra
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self, speed=30):
        # Svolta a destra
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
    def set_pwm_a(self, value):
        # Imposta il ciclo di lavoro del motore A
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        # Imposta il ciclo di lavoro del motore B
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        # Imposta i motori
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

# Creazione di un oggetto AlphaBot
Ab = AlphaBot()

# Creazione di un socket per la comunicazione
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(MY_ADDRESS)
s.listen()
print(f'Server listening on {HOST}:{PORT}...')

# Definizione dei comandi validi
COMMANDS = ["F", "B", "L", "R", "E"]
check = True
check_order = 0

try:
    # Accettazione di nuove connessioni
    conn, address = s.accept()

    while True:
        # Ricezione dei dati dal client
        data = conn.recv(1024).decode()
        # Divisione dei dati ricevuti in comando e numero
        command, number = data.split(';')
        # Verifica che il formato del messaggio sia corretto
        if not (command in COMMANDS):
            # Invia un messaggio di errore al client
            conn.sendall(
                'Invalid message format. Expected format: "command";"number"'.encode())
        # Invia una risposta al client
        conn.sendall(
            f'Received command "{command}" with number "{number}"'.encode())

        if command == ('F'):
            Ab.forward()

        elif command == ('B'):
            Ab.backward()

        elif command == ('L'):
            Ab.left()
        
        elif command == ('R'):
            Ab.right()
        
        elif command == ('E'):
            break

        time.sleep(float(number))
        Ab.stop()
except KeyboardInterrupt:
    # Pulizia dei pin GPIO in caso di interruzione da tastiera
    GPIO.cleanup()
