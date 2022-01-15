import pygame
from OpenGL.GLUT import *
from cffi.setuptools_ext import execfile

from src.button import Button


pygame.init()
glutInit()
# create display window
SCREEN_HEIGHT = glutGet(GLUT_SCREEN_HEIGHT)
SCREEN_WIDTH = glutGet(GLUT_SCREEN_WIDTH)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Fish Frenzy')

start_img = pygame.image.load("data/menuimg.jpg").convert_alpha()
button_img = pygame.image.load("data/button.png").convert_alpha()
button_img = pygame.transform.scale(button_img, (300, 100))

start_button = Button(SCREEN_WIDTH * 0.5 - 300 / 2, SCREEN_HEIGHT * 0.4 - 100 / 2, button_img, 1)
exit_button = Button(SCREEN_WIDTH * 0.5 - 300 / 2, SCREEN_HEIGHT * 0.6 - 100 / 2, button_img, 1)

# menu loop
run = True
while run:
    screen.blit(start_img, (0, 0))

    if start_button.draw(screen):
        execfile('fishy.py')
        print("Start")
    if exit_button.draw(screen):
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
