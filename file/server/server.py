import socket
from _thread import start_new_thread
import pygame
import json
import time
import os

pygame.mixer.init()
# pygame.mixer.music.load('stay.mp3')

s = socket.socket()
host = socket.gethostname()
port = 9077
print(host)
s.bind((host,port))
s.listen()

def doOpn(clientsocket, cmd):
    clientsocket.send(cmd.encode())

networkCount=input('How many other devices do you want to connect?')
networkCount=int(networkCount)

ID = 0
clients = []
while ID<networkCount:
    clientsocket, address = s.accept()
    clients.append(clientsocket)
    # clientsocket.send(s.encode())
    # start_new_thread(pingClient(), (clientsocket, ID))
    print(f"Connected with {address}, allotted ID={ID}")
    ID+=1

for c in clients:
    songs=c.recv(1024).decode()
    print (songs)
    
songSelect = input('Enter the song to be played (followed by the file extension)')

print('Checking if server end point has the song')

if(os.path.isfile(songSelect)) :
    print ('Song is already present on the server endpoint')
    for c in clients : 
        songAlreadyReceived= 'songAlreadyReceived'
        c.send(songAlreadyReceived.encode())
else : 
    print('Song is not present on the server endpoint')
    for c in clients:
        if(os.path.isfile(songSelect)) :
            songAlreadyReceived= 'songAlreadyReceived'
            c.send(songAlreadyReceived.encode())
        else :
            c.send(songSelect.encode())
            songPresent=c.recv(1024).decode()
            print ('input 1      ', songPresent)
            if(songPresent == 'yes') :
                print ('Song is present on ' , c)
                print ('Receiving song from ' , c)
                filename = songSelect
                file = open(filename, 'wb')
                file_data = c.recv(110241024)
                file.write(file_data)
                file.close()
                print ('Song transfering completed from ' , c)
                print ('The server endpoint has the requested song now')
            else :
                print ('Song is not present on ' , c)

if(os.path.isfile(songSelect)) :
    pygame.mixer.music.load(songSelect)

    for c in clients:
        c.send(songSelect.encode())
        songPresent=c.recv(1024).decode()
        if(songPresent == 'yes') :
            print('song is present in ' , c)
        else : 
            print('transferring song to ' , c)
            file = open(songSelect , 'rb')
            file_data = file.read(110241024)
            c.send(file_data)
            print('song transferred to ' , c)
        
    while True:
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
else :
    print('Song is not present at any of the endpoint of the server')