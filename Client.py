# === Client (client.py) ===
import socket
import os
import keyboard
import time

HOST = '192.168.1.47'
PORT = 1546

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def process(packet):
    parts = packet.split("AND")
    X = int(packet.split("AND")[0][-1], 16)
    Y = int(parts[1])
    return X, Y

def creer_grille(x_M, y_M, x_O, y_O, taille=9):
    grille = [["." for _ in range(taille)] for _ in range(taille)]
    if 0 <= x_M < taille and 0 <= y_M < taille:
        grille[y_M][x_M] = "M"
    if 0 <= x_O < taille and 0 <= y_O < taille:
        grille[y_O][x_O] = "O"
    for ligne in grille:
        print(" ".join(ligne))

while True:
    user = input('Enter your username: ')
    if not user.strip():
        continue
    user = "0x1" + user
    client_socket.send(user.encode())
    disp = client_socket.recv(1024).decode('utf-8')

    if disp == '0x1796573':
        os.system('cls')
        break
    elif disp == '0x16E6F':
        os.system('cls')
        print('Username is already taken.')

print('Logged in...')
print('Waiting for a game...')

game_started = False

while True:
    client_socket.send('0x555044'.encode())
    stat = client_socket.recv(1024).decode('utf-8')
    if stat == '0x466f756e64' and not game_started:
        print('Game Found !!')
        game_started = True
        break

req = '0x4' + user[3:]
client_socket.send(req.encode())
data = client_socket.recv(1024).decode()
X, Y = process(data)
print(f"Initial position: X={X}, Y={Y}")

time.sleep(0.6)
req = '0x3' + user[3:]
client_socket.send(req.encode())
EN = client_socket.recv(1024).decode()
print(f"Ennemi: {EN}")

while True:
    req = '0x4' + EN
    client_socket.send(req.encode())
    data = client_socket.recv(1024).decode()
    Xe, Ye = process(data)

    req = f'0x5{X}AND{Y}AND{user[3:]}'
    client_socket.send(req.encode())

    if keyboard.is_pressed('z') and Y > 0:
        Y -= 1
    elif keyboard.is_pressed('s') and Y < 8:
        Y += 1
    elif keyboard.is_pressed('q') and X > 0:
        X -= 1
    elif keyboard.is_pressed('d') and X < 8:
        X += 1

    os.system('cls')
    creer_grille(Xe, Ye, X, Y)
    time.sleep(0.6)