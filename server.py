import socket


import pygame
import json

pygame.mixer.init()
pygame.mixer.music.load('chloe.mp3')

s = socket.socket()
host = socket.gethostname()
port = 9077
s.bind((host,port))
s.listen(5)

d = {
    'cmd': 'pause',
    'loop': 4,
}

command = json.dumps(d)
c, addr = s.accept()
print("Connection accepted from " + repr(addr[1]))

while True:
    cmd = input('What do you want to do? (play/pause/resume/stop/end)')
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
        c.send(cmd.encode())
        print("connection closed.")
        c.close()
        break
    c.send(cmd.encode())