import pygame

pygame.mixer.init()
pygame.mixer.music.load('chloe.mp3')
pygame.mixer.music.play(1)

cmd = ''
while cmd!='pause':
    cmd = input()