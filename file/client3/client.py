import socket
import pygame
import json
import os

pygame.mixer.init()
# pygame.mixer.music.load('stay.mp3')

s = socket.socket()
host = input(str("Please enter the host address of the sender : "))
port = 9077
s.connect((host, port))

# serverSocket=s.recv(1024).decode()
# print(s.recv(1024).decode())

songInput = input('What song you want to suggest to be played ..')
s.send(songInput.encode())

songDecide = s.recv(100).decode()

if(songDecide == 'songAlreadyReceived') :
    print('The song that is to be played is present on the server endpoint') 
else :
    print('The song that is to be played is not present on the server endpoint') 
    if(os.path.isfile(songDecide)) :
        print('The song that is to be played is present on this endpoint') 
        songPresent='yes'
        s.send(songPresent.encode()) 
    
        print('Initialting transfer of the song to the server endpoint')
        file = open(songDecide , 'rb')
        file_data = file.read(110241024)
        s.send(file_data)
        print('Song has been transferred successfully')
        print('The song that is to be played is now present on the server endpoint') 
        
    else : 
        print('The song that is to be played is not present on this endpoint') 
        songPresent='no'
        s.send(songPresent.encode()) 
    

songSelect = s.recv(100).decode()

if(os.path.isfile(songSelect)) :
    songPresent='yes'
    s.send(songPresent.encode()) 
    print('Song is already present')
else : 
    songPresent='no'
    s.send(songPresent.encode())
    print('Song is not present, transferring ...')
    filename = songSelect
    file = open(filename, 'wb')
    file_data = s.recv(110241024)
    file.write(file_data)
    file.close()
    print('Song transferred to the machine successfully')
    
pygame.mixer.music.load(songSelect)
while True:
    
    received = s.recv(100).decode()
    if received == 'play':
        print("Starting playback...")
        pygame.mixer.music.play(1)
    elif received == 'pause':
        print("|| Playback paused ||")
        pygame.mixer.music.pause()
    elif received == 'resume':
        print("Resumed playback...")
        pygame.mixer.music.unpause()
    elif received == 'stop':
        print("* Playback stopped *")
        pygame.mixer.music.stop()
    elif received == 'end':
        print("## connection closed ##")
        pygame.mixer.music.stop()
        break



# print(d)

# pygame.mixer.init()
# pygame.mixer.music.load('chloe.mp3')
# pygame.mixer.music.play(1)

# cmd = ''
# while cmd!='pause':
#     cmd = input()
