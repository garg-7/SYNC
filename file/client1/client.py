import socket
import pygame
import json
import os

pygame.mixer.init()
# pygame.mixer.music.load('stay.mp3')

MUSIC_DIR = 'music'
s = socket.socket()
host = input("Please enter the hostname of the server : ")
port = 9077
s.connect((host, port))

# serverSocket=s.recv(1024).decode()
# print(s.recv(1024).decode())

songInput = input("What song you want to suggest to be played?")
s.send(songInput.encode())

songDecide = s.recv(100).decode()

if(songDecide == 'songAlreadyReceived') :

    print("The song that is to be played is present on the server.")
else :

    print("The song that is to be played is not present on the server.")
    if os.path.isfile(os.path.join(MUSIC_DIR, songSelect)) :

        print('The song that is to be played is present on this client')
        songPresent='yes'
        s.send(songPresent.encode())

        print('Sending the song file to the server endpoint')
        f = open(os.path.join(MUSIC_DIR, songSelect) , 'rb')
        file_data = f.read(110241024)
        s.send(file_data)

        print('Song has been transferred successfully')
        print('The song that is to be played is now present on the server endpoint')

    else :
        print('The song that is to be played is not present on this client')
        songPresent='no'
        s.send(songPresent.encode())

toContinue = s.recv(100).decode()
if toContinue=='Continue':
    songSelect = s.recv(100).decode()

    if os.path.isfile(os.path.join(MUSIC_DIR, songSelect)) :
        songPresent='yes'
        s.send(songPresent.encode())
        print('The song is present on this client.')
    else :
        songPresent='no'
        s.send(songPresent.encode())
        print("The song to be played is not present on this client, receiving the file from the server...")
        filename = os.path.join(MUSIC_DIR, songSelect)
        f = open(filename, 'wb')
        file_data = s.recv(110241024)
        f.write(file_data)
        f.close()
        print("The song file has been received successfully.")

    pygame.mixer.music.load(songSelect)
    while True:

        received = s.recv(100).decode()
        if received == 'play':
            print("Starting playback...")
            pygame.mixer.music.play()
        elif received == 'pause':
            print("Playback paused...")
            pygame.mixer.music.pause()
        elif received == 'resume':
            print("Playback resumed...")
            pygame.mixer.music.unpause()
        elif received == 'stop':
            print("Playback stopped.")
            pygame.mixer.music.stop()
        elif received == 'end':
            print("Connection closed.")
            pygame.mixer.music.stop()
            break

else:
    print("The file couldn't be made available to the server. Exiting...")