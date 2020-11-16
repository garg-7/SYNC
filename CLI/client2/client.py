import socket
import pygame
import json
import os

pygame.mixer.init()
# pygame.mixer.music.load('stay.mp3')

MUSIC_DIR = 'music'

#Establishing connection
s = socket.socket()
host = input("Please enter the hostname of the server : ")
port = 9077
s.connect((host, port))

# serverSocket=s.recv(1024).decode()
# print(s.recv(1024).decode())

#input for suggestions
songInput = input("What song you want to suggest to be played?")
s.send(songInput.encode())

#receiving input of the track to be played
songDecide = s.recv(100).decode()

#Making different cases on the basis of presence of the track at server endpoint
if(songDecide == 'songAlreadyReceived') :
    #song is present on the server endpoint
    print("The song that is to be played is present on the server.")
else :
    #song is not present on the server endpoint
    print("The song that is to be played is not present on the server.")
    
    #Making different cases on the basis of presence of the track at this endpoint
    if os.path.isfile(os.path.join(MUSIC_DIR, songDecide)) :
        print('The song that is to be played is present on this client')
        songPresent='yes'
        s.send(songPresent.encode())

        #transferring song to the server endpoint
        print('Sending the song file to the server endpoint')
        f = open(os.path.join(MUSIC_DIR, songDecide) , 'rb')
        file_data = f.read(110241024)
        s.send(file_data)

        print('Song has been transferred successfully')
        print('The song that is to be played is now present on the server endpoint')

    else :
        #song not present on this endpoint
        print('The song that is to be played is not present on this client')
        songPresent='no'
        s.send(songPresent.encode())

#receiving input if playback would be possible
toContinue = s.recv(100).decode()
if toContinue=='Continue':
    songSelect = s.recv(100).decode()

    #Making different cases on the basis of presence of the track at this endpoint
    if os.path.isfile(os.path.join(MUSIC_DIR, songSelect)) :
    # if os.path.isfile(songSelect) :
        #song already present
        songPresent='yes'
        s.send(songPresent.encode())
        print('The song is present on this client.')
    else :
        songPresent='no'
        #song not present
        s.send(songPresent.encode())
        print("The song to be played is not present on this client, receiving the file from the server...")
        
        #song transferring to this client from the server endpoint
        filename = os.path.join(MUSIC_DIR, songSelect)
        # filename = songSelect
        f = open(filename, 'wb')
        file_data = s.recv(110241024)
        f.write(file_data)
        f.close()
        print("The song file has been received successfully.")

    pygame.mixer.music.load(os.path.join(MUSIC_DIR, songSelect))
    while True:
        #receiving commands from the server and executing them
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
    #song playback not possible
    print("The file couldn't be made available to the server. Exiting...")