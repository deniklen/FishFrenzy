import os
import sys

import pygame
from src import fishy
from src.button import Button

pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.NOFRAME)
pygame.display.set_caption('Fish Frenzy')

start_img = pygame.image.load("data/menuimg.jpg").convert_alpha()
button_sound = pygame.image.load("data/buttonszvukom.png").convert_alpha()
button_sound = pygame.transform.scale(button_sound, (400, 150))
button_no_sound = pygame.image.load("data/buttonbezzvuka.png").convert_alpha()
button_no_sound = pygame.transform.scale(button_no_sound, (400, 150))
button_exit = pygame.image.load("data/exitbutton.png").convert_alpha()
button_exit = pygame.transform.scale(button_exit, (400, 150))



start_button = Button(pygame.display.Info().current_w * 0.35 - 400 / 2, pygame.display.Info().current_h * 0.35 - 150 / 2,
                      button_sound, 1)
exit_button = Button(pygame.display.Info().current_w * 0.5 - 400 / 2, pygame.display.Info().current_h * 0.6 - 150 / 2,
                     button_exit, 1)
mute_button = Button(pygame.display.Info().current_w * 0.65 - 400 / 2, pygame.display.Info().current_h * 0.35 - 150 / 2,
                     button_no_sound, 1)

# menu loop
def run():
    sound_flag = 1
    run_flag = True

    while run_flag:
        screen.blit(start_img, (0, 0))

        if start_button.draw(screen):
            sound = True
            fishy.run(sound)
        if exit_button.draw(screen):
            run_flag = False
        if mute_button.draw(screen):
            sound = False
            fishy.run(sound)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_flag = False

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    run()
    os.execv(__file__, sys.argv)
