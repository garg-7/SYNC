import socket
from _thread import start_new_thread
import pygame
import json
import time
import os

pygame.mixer.init()
# pygame.mixer.music.load('stay.mp3')

MUSIC_DIR = 'music'
s = socket.socket()
host = socket.gethostname()
port = 9077
print(host)
s.bind((host,port))
s.listen()

def doOpn(clientsocket, cmd):
    clientsocket.send(cmd.encode())

networkCount = input("How many clients do you want to allow?")
networkCount = int(networkCount)

ID = 0
clients = []
while ID<networkCount:
    clientsocket, address = s.accept()
    clients.append((clientsocket, address))
    # clientsocket.send(s.encode())
    # start_new_thread(pingClient(), (clientsocket, ID))
    print(f"Connected with {address}, allotted ID={ID}")
    ID+=1

for c in clients:
    songs=c[0].recv(1024).decode()
    print(songs)
    
songSelect = input("Enter the song to be played (followed by the file extension)")

print("Checking if server end point has the song.")

if(os.path.isfile(os.path.join(MUSIC_DIR, songSelect))) :
    print ("Song is already present on the server endpoint")
    for c in clients :
        c[0].send('songAlreadyReceived'.encode())
else : 
    print("Song is not present on the server endpoint")
    for c in clients:
        c[0].send(songSelect.encode())            
        songPresent=c[0].recv(1024).decode()       
        if(songPresent == 'yes'):
            if not os.path.isfile(os.path.join(MUSIC_DIR, songSelect)):
                print (f"Client {c[1]} has the song")
                print ("Receiving the song from " , c[1])
            filename = songSelect
            f = open(filename, 'wb')
            file_data = c[0].recv(110241024)
            f.write(file_data)
            f.close()
            if not os.path.isfile(os.path.join(MUSIC_DIR, songSelect)):
                print ("Song successfully received from ", c[1])
                print ("The server now has the song file to be played.")
        else :
            print (f"Client {c[1]} does not have the song")

if(os.path.isfile(songSelect)) :           
    pygame.mixer.music.load(songSelect)    

    for c in clients:
        c[0].send("Continue".encode())

    print("Veryifying whether all the clients have the song.")
    for c in clients:
        c[0].send(songSelect.encode())         # send the song name to every client
        songPresent=c[0].recv(1024).decode()   # receive whether the song is present there or not
        if(songPresent == 'yes') :      
            print(f"{songSelect.split('.')[0]} is present in ", c[1])
        else : 
            print("Transferring song to ", c[1])
            f = open(songSelect , 'rb')
            file_data = f.read(110241024)
            c[0].send(file_data)
            print("Song transferred to ", c[1])
    while True:
        cmd = input('What do you want to do? (play/pause/resume/stop/end)')
        for c in clients:
            start_new_thread(doOpn, (c[0], cmd))
        # adding suitable delay
        # time.sleep(0.21)
        if cmd == 'play':
            print("Starting playback...")
            pygame.mixer.music.play()
        elif cmd == 'pause':
            print("Playback paused...")
            pygame.mixer.music.pause()
        elif cmd == 'resume':
            print("Playback resumed...")
            pygame.mixer.music.unpause()
        elif cmd == 'stop':
            print("Playback stopped.")
            pygame.mixer.music.stop()
        elif cmd == 'end':
            print("Connection(s) closed.")
            break
else :
    print("Song is not present on the server and could not be obtained from any client.")
    for c in clients:
        c[0].send("Stop".encode())
