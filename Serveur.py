# === Serveur (serveur.py) ===
import threading
import socket
import random
from colorama import init, Fore

init(autoreset=True)

HOST = '192.168.1.47'
PORT = 1546
GAME = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(Fore.CYAN + f"Serveur en écoute sur le port {PORT}...")

Players = []
Ip = []
PosX = []
PosY = []
client_sockets = []

class Player:
    @staticmethod
    def add(user, ip, client_socket):
        if user not in Players:
            Players.append(user)
            Ip.append(ip)
            PosX.append(0)
            PosY.append(0)
            print(Fore.GREEN + f"[+] User ajouté: {user} | IP: {ip}")
            client_socket.send('0x1796573'.encode('utf-8'))
            client_sockets.append(client_socket)
        else:
            client_socket.send('0x16E6F'.encode('utf-8'))
            print(Fore.RED + "[x] Échec d'ajout - nom déjà pris")

    @staticmethod
    def get():
        return len(Players)

    @staticmethod
    def getPos(user, client_socket):
        if user in Players:
            index = Players.index(user)
            ReqXY = '0x4' + str(PosX[index]) + 'AND' + str(PosY[index])
            client_socket.send(ReqXY.encode())
            print(Fore.BLUE + f"[\u2192] Envoi de la position: {ReqXY}")
        else:
            print(Fore.RED + "[x] Utilisateur introuvable pour getPos.")
            client_socket.send('0x16E6F'.encode('utf-8'))

    @staticmethod
    def setPos(packet):
        print(Fore.YELLOW + f"[\u2192] Packet reçu: {packet}")
        parts = packet.split("AND")
        if len(parts) >= 3:
            try:
                X = int(parts[0][-1], 16)
                Y = int(parts[1])
                User = parts[2]

                if User in Players:
                    index = Players.index(User)
                    PosX[index] = X
                    PosY[index] = Y
                    print(Fore.GREEN + f"[+] Position mise à jour pour {User}: X={X}, Y={Y}")
                else:
                    print(Fore.RED + f"[x] Utilisateur {User} introuvable.")
            except ValueError:
                print(Fore.RED + "[x] Valeurs invalides dans le packet.")
        else:
            print(Fore.RED + "[x] Format de packet invalide. Attendu: 0x5XANDYANDUser")

class Req:
    @staticmethod
    def connect(usName, ip, client_socket):
        print(Fore.MAGENTA + "[+] Requête de connexion...")
        Player.add(usName[3:], ip, client_socket)
        x_digit = str(random.randint(0, 9))
        y_digit = str(random.randint(1, 9))
        pack = '0x5' + x_digit + 'AND' + y_digit + 'AND' + usName[3:]
        Player.setPos(pack)

    @staticmethod
    def list(packet, client_socket):
        resultat = [element for element in Players if element != packet[3:]]
        resultats = ', '.join(resultat)
        client_socket.send(f'{resultats}'.encode())

    @staticmethod
    def disconnect():
        print(Fore.RED + "[x] Requête de déconnexion")

def packet(packet, client_address, client_socket):
    global GAME

    if packet[:3] == '0x1':
        Req.connect(packet, client_address, client_socket)
    elif packet[:3] == '0x2':
        Req.disconnect()
    elif packet[:3] == '0x3':
        Req.list(packet, client_socket)
    elif packet[:3] == '0x4':
        user = packet[3:]
        Player.getPos(user, client_socket)
    elif packet[:3] == '0x5':
        Player.setPos(packet)

    if Player.get() == 2 and not GAME:
        GAME = True
        print(Fore.CYAN + "[+] Lancement du jeu...")
        for sock in client_sockets:
            try:
                sock.send('0x466f756e64'.encode())
                print(Fore.CYAN + "[\u2713] Message '0x466f756e64' envoyé à un client")
            except Exception as e:
                print(Fore.RED + f"[x] Erreur en envoyant le message de démarrage : {e}")

def client_thread(client_socket, client_address):
    print(Fore.LIGHTBLUE_EX + f"[+] Connexion de {client_address}")
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                print(Fore.YELLOW + f"[-] Déconnexion de {client_address}")
                break
            packet(data, client_address[0], client_socket)
    except ConnectionResetError:
        print(Fore.RED + f"[!] Connexion réinitialisée par {client_address}")
    finally:
        client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    thread = threading.Thread(target=client_thread, args=(client_socket, client_address))
    thread.start()