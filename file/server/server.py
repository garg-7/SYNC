import socket
from _thread import start_new_thread
import pygame
import json
import time

pygame.mixer.init()
pygame.mixer.music.load('stay.mp3')

s = socket.socket()
host = socket.gethostname()
port = 9077
print(host)
s.bind((host,port))
s.listen()

def doOpn(clientsocket, cmd):
    clientsocket.send(cmd.encode())

ID = 0
clients = []
while ID<1:
    clientsocket, address = s.accept()
    clients.append(clientsocket)
    # clientsocket.send(s.encode())
    # start_new_thread(pingClient(), (clientsocket, ID))
    print(f"Connected with {address}, allotted ID={ID}")
    ID+=1

while True:
    
    for c in clients:
        songs=c.recv(1024).decode()
        print (songs)
    cmd = input('What do you want to do? (play/pause/resume/stop/end)')
    for c in clients:
        start_new_thread(doOpn, (c, cmd))
    if cmd == 'play':
        print("Starting playback...")
        pygame.mixer.music.play(1)
    elif cmd == 'pause':
        print("|| Playback paused ||")
        pygame.mixer.music.pause()
    elif cmd == 'resume':
        print("Resumed playback...")
        pygame.mixer.music.unpause()
    elif cmd == 'stop':
        print("* Playback stopped *")
        pygame.mixer.music.stop()
    elif cmd == 'end':
        print("connection(s) closed.")
        break
    