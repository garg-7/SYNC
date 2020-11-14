import socket
from _thread import start_new_thread
import pygame
import json
import time
import os

pygame.mixer.init()

MUSIC_DIR = 'music'

#Establishing connection
s = socket.socket()
host = socket.gethostname()
port = 9077
print(host)
s.bind((host,port))
s.listen()

def doOpn(clientsocket, cmd):
    clientsocket.send(cmd.encode())

# Input of the number of clients
networkCount = input("How many clients do you want to allow?")
networkCount = int(networkCount)

# Establshing Connection with the clients and printing their address with allotted IDs 
ID = 0
clients = []
while ID<networkCount:
    clientsocket, address = s.accept()
    clients.append((clientsocket, address))
    # clientsocket.send(s.encode())
    # start_new_thread(pingClient(), (clientsocket, ID))
    print(f"Connected with {address}, allotted ID={ID}")
    ID+=1
    
# receiving the track suggestions from the clients and printing them
print("Following are the track recommendations by the client servers ")
for c in clients:
    songs=c[0].recv(1024).decode()
    print(songs)

# taking input of the song to be played
songSelect = input("Enter the song to be played (followed by the file extension)")

#Making different cases on the basis of presence of the track at this endpoint
print("Checking if server end point has the song.")
if(os.path.isfile(os.path.join(MUSIC_DIR, songSelect))) :
    print ("Song is already present on the server endpoint")
    #song already present, informing the clients that the song is available
    for c in clients :
        c[0].send('songAlreadyReceived'.encode())
        
else :
    print("Song is not present on the server endpoint")
    #track not present, checking if the clients have the track at their endpoints
    for c in clients:
        c[0].send(songSelect.encode())
        songPresent=c[0].recv(1024).decode()
        #Making different cases on the basis of presence of the track at the corresponding client endpoint
        if(songPresent == 'yes'):
            if not os.path.isfile(os.path.join(MUSIC_DIR, songSelect)):
                print (f"Client {c[1]} has the song")
                print ("Receiving the song from " , c[1])
            
            #track is present, transferring the track to the server endpoint and saving the file
            filename = os.path.join(MUSIC_DIR, songSelect)
            f = open(filename, 'wb')
            file_data = c[0].recv(110241024)
            f.write(file_data)
            f.close()
            if not os.path.isfile(os.path.join(MUSIC_DIR, songSelect)):
                print ("Song successfully received from ", c[1])
                print ("The server now has the song file to be played.")
        else :
            #track not available at this client endpoint
            print (f"Client {c[1]} does not have the track")

if os.path.isfile(os.path.join(MUSIC_DIR, songSelect)) :
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, songSelect))

    #track is available at the server's endpoint
    #informing the clients that track will be played
    for c in clients:
        c[0].send("Continue".encode())
    
    #Making different cases on the basis of presence of the track at the corresponding client endpoint
    print("Veryifying whether all the clients have the song.")
    for c in clients:
        c[0].send(songSelect.encode())         # send the song name to every client
        songPresent=c[0].recv(1024).decode()   # receive whether the song is present there or not
        if(songPresent == 'yes') :
            # track already available at this client endpoint
            print(f"{songSelect.split('.')[0]} is present in ", c[1])
        else :
            #track is not present at the client endpoint, transferring the track from the server
            print("Transferring song to ", c[1])
            f = open(os.path.join(MUSIC_DIR, songSelect) , 'rb')
            file_data = f.read(110241024)
            c[0].send(file_data)
            print("Song transferred to ", c[1])
            
    #now song is available at all the client endpoints 
    while True:
        #taking input and sending the commands to all the client endpoints for playing the track
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
    #stopping and sending the stop command to all the clients since track is unavailable.
    for c in clients:
        c[0].send("Stop".encode())
