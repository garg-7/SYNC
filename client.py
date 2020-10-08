import socket
import pygame
import json

pygame.mixer.init()
pygame.mixer.music.load('chloe.mp3')

s = socket.socket()
host = socket.gethostname()
port = 9077
s.connect((host, port))

while True:
    received = s.recv(1024).decode()
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
