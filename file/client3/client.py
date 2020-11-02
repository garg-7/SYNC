import socket
import pygame
import json

pygame.mixer.init()
pygame.mixer.music.load('stay.mp3')

s = socket.socket()
host = input(str("Please enter the host address of the sender : "))
port = 9077
s.connect((host, port))

# serverSocket=s.recv(1024).decode()
# print(s.recv(1024).decode())
while True:
    songInput = input('What song you want to suggest to be played ..')
    s.send(songInput.encode())
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
