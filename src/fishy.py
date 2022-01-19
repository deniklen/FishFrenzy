import random
import time  # to be used in timer
from random import randint
from sys import exit

import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.time import delay
from scipy import interpolate

from src import designscene, menu

pygame.init()
glutInit()  # Initialize Glut Features

# Possible levels ==> [Score to pass, maximum time]
levels = [[50, 999], [60, 999], [70, 999], [85, 999], [100, 999]]  # 5 levels
level = 1  # initial level,

seconds = 0  # the actual timer of every level
time_start = 0  # just for calculating time
######## Control the Small Fishes Motion ###########

x_ax = 100  # 'INCREASING'  = increasing number of curve points which means 'MORE' curve resolution(integer)
patterns_num = 5  # Number of Available patterns (integer)

vertical_displacement = 2  # 'DECREASING'  = decreasing vertical motion which means 'MORE STABLE' Motion
x_displacement = 0.2  # Speed of small fish
##################################################

start = 0
score = 0
big_fish_size = 3.1
texture = ()
current_x = 0
current_y = 0
mouse_dir = 1
sound = True
photos = ['data/Fishleft1.png', 'data/Fishright1.png', 'data/Fishleft2.png', 'data/Fishright2.png',
          'data/Fishleft3.png', 'data/Fishright3.png', 'data/Fishleft4.png', 'data/Fishright4.png',
          'data/Fishleft5.png', 'data/Fishright5.png', 'data/Fishleft6.png', 'data/Fishright6.png',
          'data/Fishleft7.png', 'data/Fishright7.png', 'data/Fishleft8.png', 'data/Fishright8.png',
          'data/Fishleft9.png', 'data/Fishright9.png', 'data/Fishleft10.png', 'data/Fishright10.png',
          'data/Fishleft11.png', 'data/Fishright11.png', 'data/ground.jpg', 'data/menu.jpg']

x_points = [i for i in range(-50, int(glutGet(GLUT_SCREEN_WIDTH)) + 50, x_ax)]
num_points = len(x_points)

fish_array = designscene.generate_a()
count = len(fish_array)
paths = []
lost_flag = 1


def generate_patterns():
    global paths, num_points, patterns_num, vertical_displacement
    paths = []  # clear paths
    for j in range(patterns_num):
        new_path = []
        for i in range(num_points):
            new_path.append(randint(int(glutGet(GLUT_SCREEN_HEIGHT)) - vertical_displacement,
                                    int(glutGet(GLUT_SCREEN_HEIGHT)) + vertical_displacement))

        paths.append(interpolate.splrep(x_points, new_path))  # tck


def f(i):
    global paths, fish_array

    if fish_array[i][3] == 1:
        f_x = interpolate.splev(fish_array[i][0], paths[fish_array[i][4]])
    else:
        f_x = int(glutGet(GLUT_SCREEN_WIDTH)) - interpolate.splev(fish_array[i][0], paths[fish_array[i][4]])

    if fish_array[i][0] > int(glutGet(GLUT_SCREEN_WIDTH)) + 50:
        fish_array[i][3] = -fish_array[i][3]
        fish_array[i][6] = fish_array[i][6] - 1  # look at

    elif fish_array[i][0] < -50:
        fish_array[i][3] = -fish_array[i][3]
        fish_array[i][6] = fish_array[i][6] + 1

    return f_x + fish_array[i][5] - (int(glutGet(GLUT_SCREEN_WIDTH)) / 2)


def drawtext(string, x, y):
    glLineWidth(5)
    glColor(1, 1, 0)  # Yellow Color
    glLoadIdentity()
    glTranslate(x, y, 0)
    glRotate(180, 1, 0, 0)
    glScale(.26, .26, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)


def add_small_fish():
    global count, fish_array, level, levels
    count += 1

    new_rand_x = random.randint(0, 1)
    new_rand_y = random.randint(0, 7)
    new_rand_pattern = randint(0, patterns_num - 1)
    if score <= round(levels[level - 1][0] / 3):
        rand_scale = random.randint(0, 100)
        if rand_scale < 85:
            scale = random.choice([2, 2.5])
        else:
            scale = random.choice([5.5, 6])
    elif round(levels[level - 1][0] / 3 * 2) >= score > round(levels[level - 1][0] / 3):
        rand_scale = random.randint(0, 100)
        if rand_scale < 30:
            scale = random.choice([2, 2.5])
        elif 85 > rand_scale > 30:
            scale = random.choice([5.5, 6])
        else:
            scale = random.choice([9, 9.5])
    else:
        scale = random.choice([2, 9.5])
    if new_rand_x == 0:
        new_fish_shape = random.choice([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
        direction = 1
    else:
        new_fish_shape = random.choice([0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
        direction = -1
    if new_rand_y == 0:
        position = 0
    elif new_rand_y == 1:
        position = glutGet(GLUT_SCREEN_WIDTH) * 0.1
    elif new_rand_y == 2:
        position = glutGet(GLUT_SCREEN_WIDTH) * 0.2
    elif new_rand_y == 3:
        position = glutGet(GLUT_SCREEN_WIDTH) * 0.25
    elif new_rand_y == 4:
        position = glutGet(GLUT_SCREEN_WIDTH) * 0.75
    elif new_rand_y == 5:
        position = glutGet(GLUT_SCREEN_WIDTH) * 0.8
    elif new_rand_y == 6:
        position = glutGet(GLUT_SCREEN_WIDTH) * 0.9
    else:
        position = glutGet(GLUT_SCREEN_WIDTH)
    fish_array.append(
        list((position, 0, scale, direction, new_rand_pattern, designscene.random_offset(), new_fish_shape)))


def remove_small_fish(i):
    global fish_array, count
    global fish_array
    del fish_array[i]
    count -= 1


def remove_big_fish_lost():
    global lost_flag
    lost_flag = 2


def increase_Score():
    global score
    score += 1


def eating_sound():
    s_file = pygame.mixer.Sound("data/eating.wav")
    if sound:
        s_file.play()
    else:
        s_file.stop()


def game_over_sound():
    s_file = pygame.mixer.Sound("data/gameover.wav")
    if sound:
        s_file.play()
    else:
        s_file.stop()


def collision(i):
    global current_x, current_y, score, count, patterns_num, big_fish_size, seconds, fish_array
    x = fish_array[i][0]
    y = fish_array[i][1]
    if abs(current_x - x) < 30 and abs(current_y - y) < 30 and fish_array[i][2] > big_fish_size:
        remove_big_fish_lost()
        game_over_sound()
        pygame.time.delay(750)
        glutDestroyWindow(glutGetWindow())
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif abs(current_x - x) < 30 and abs(current_y - y) < 30 and fish_array[i][2] < big_fish_size:
        remove_small_fish(i)
        increase_Score()
        add_small_fish()
        eating_sound()


def load_texture():
    global texture, photos
    texture = glGenTextures(24)
    for i in range(24):
        imgload = pygame.image.load(photos[i])
        img = pygame.image.tostring(imgload, "RGBA", True)
        width = imgload.get_width()
        height = imgload.get_height()
        glBindTexture(GL_TEXTURE_2D, texture[i])  # Set this image in images array
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture[i])


def myint():
    s_file = pygame.mixer.Sound("data/feeding-frenzy.wav")
    if sound:
        s_file.play()
    else:
        s_file.stop()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, int(glutGet(GLUT_SCREEN_WIDTH)), int(glutGet(GLUT_SCREEN_HEIGHT)), 0, -1.0, 1.0)
    load_texture()
    glClearColor(1, 1, 1, .5)
    generate_patterns()


def start_time():
    global time_start
    time_start = time.time()


##########################################################################################
def main_scene():
    global texture, current_x, current_y, current_z, count, big_fish_size, fish_array, lost_flag, mouse_dir, score, levels, level
    '''if lost_flag == 2:
        glutDestroyWindow(glutGetWindow())
    if lost_flag == 0:
        glutDestroyWindow(glutGetWindow())
    '''
    if score > 0:
        enlargement = score / round(levels[level - 1][0] / 3)
        big_fish_size = 3.1 + enlargement
        if big_fish_size > 4:
            big_fish_size = 4
    if score >= round(levels[level - 1][0] / 3):
        enlargement = score / round(levels[level - 1][0] / 3 * 2)
        big_fish_size = 7 + enlargement
        if big_fish_size > 8:
            big_fish_size = 8
    if score >= round(levels[level - 1][0] / 3 * 2):
        enlargement = score / round(levels[level - 1][0])
        big_fish_size = 10 + enlargement

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)  # | GL_DEPTH_BUFFER_BIT)
    if lost_flag == 1:  # play the game
        glBindTexture(GL_TEXTURE_2D, texture[22])  # background

        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex3f(int(glutGet(GLUT_SCREEN_WIDTH)), int(glutGet(GLUT_SCREEN_HEIGHT)), 0)
        glTexCoord(0, 1)
        glVertex3f(int(glutGet(GLUT_SCREEN_WIDTH)), 0, 0)
        glTexCoord(1, 1)
        glVertex3f(0, 0, 0)
        glTexCoord(1, 0)
        glVertex3f(0, int(glutGet(GLUT_SCREEN_HEIGHT)), 0)
        glEnd()

        # Texture Added
        string = "Score:" + str(score)

        drawtext(string, 20, 40)
        glLoadIdentity()

        # Texture Added
        string = "Timer:" + str(levels[level - 1][1] - seconds)

        drawtext(string, 20, 100)
        glLoadIdentity()

        # Texture Added
        string = "Level:" + str(level)

        drawtext(string, 20, 70)
        glLoadIdentity()

        global start
        if start == 0:
            glutWarpPointer(int(glutGet(GLUT_SCREEN_WIDTH) / 2), int(glutGet(GLUT_SCREEN_HEIGHT) / 2))
            glTranslate(int(glutGet(GLUT_SCREEN_WIDTH) / glutGet(GLUT_SCREEN_HEIGHT)),
                        int(glutGet(GLUT_SCREEN_HEIGHT) / 2), 0)
            start = 1

        glTranslate(current_x, current_y, 0)
        glColor4f(1, 1, 1, 1)
        if mouse_dir == 1:
            glBindTexture(GL_TEXTURE_2D, texture[21])
        else:
            glBindTexture(GL_TEXTURE_2D, texture[20])

        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex3f(-10 * big_fish_size, 10 * big_fish_size, 0)
        glTexCoord(0, 1)
        glVertex3f(-10 * big_fish_size, -10 * big_fish_size, 0)
        glTexCoord(1, 1)
        glVertex3f(10 * big_fish_size, -10 * big_fish_size, 0)
        glTexCoord(1, 0)
        glVertex3f(10 * big_fish_size, 10 * big_fish_size, 0)
        glEnd()
        glLoadIdentity()

    if lost_flag == 1:

        for i in range(count):
            glLoadIdentity()
            fish_array[i][1] = f(i)
            glTranslate(fish_array[i][0], fish_array[i][1], 0)

            fish_array[i][0] += (fish_array[i][3] * x_displacement)

            if fish_array[i][3] == 1:
                glBindTexture(GL_TEXTURE_2D, texture[fish_array[i][6]])
            if fish_array[i][3] == -1:
                glBindTexture(GL_TEXTURE_2D, texture[fish_array[i][6]])

            glBegin(GL_QUADS)
            glTexCoord(0, 0)
            glVertex3f(-10 * fish_array[i][2], 10 * fish_array[i][2], 0)
            glTexCoord(0, 1)
            glVertex3f(-10 * fish_array[i][2], -10 * fish_array[i][2], 0)
            glTexCoord(1, 1)
            glVertex3f(10 * fish_array[i][2], -10 * fish_array[i][2], 0)
            glTexCoord(1, 0)
            glVertex3f(10 * fish_array[i][2], 10 * fish_array[i][2], 0)
            glEnd()
            collision(i)

    glFlush()

    ###################### Levels ###########################################
    # Check for the Level

    if score >= levels[level - 1][0]:  # Only 5 levels then get Error
        next_level(level)
        glutIdleFunc(main_scene)

    # continue timer
    game_timer()


def game_timer():
    global seconds, time_start, levels, level, lost_flag

    seconds = int(time.time() - time_start)
    if seconds == 575:
        s_file = pygame.mixer.Sound("data/feeding-frenzy.wav")
        if sound:
            s_file.play()
        else:
            s_file.stop()
    if seconds >= levels[level - 1][1]:
        lost_flag = 1


def start_again():
    global lost_flag, fish_array, score, big_fish_size, score, start, time_start
    fish_array = designscene.generate_a()
    start = 0
    score = 0
    big_fish_size = 3.1
    lost_flag = 1
    time_start = time.time()


def next_level(i):
    global x_displacement, patterns_num, vertical_displacement, level, levels
    x_displacement = 0.2 + (i * 0.05)
    vertical_displacement = 5 + (i * 2)
    patterns_num += 5 + (i * 1)
    generate_patterns()
    level += 1
    if level > len(levels):
        exit("Thanks, I was hungry !")
        # End of the game
    else:
        start_again()


def mouse(new_x, new_y):
    global current_x, current_y, mouse_dir
    if new_x > current_x:
        mouse_dir = 1
    else:
        mouse_dir = -1
    current_x = new_x
    current_y = new_y


def run(sound_flag):
    global sound
    sound = sound_flag
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)  # Initialize Window Options
    glutInitWindowSize(int(glutGet(GLUT_SCREEN_WIDTH)), int(glutGet(GLUT_SCREEN_HEIGHT)))
    glutCreateWindow(b"fish")
    glutFullScreen()
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Blend
    glEnable(GL_BLEND)

    myint()
    start_time()
    glutIdleFunc(main_scene)
    glutSetCursor(GLUT_CURSOR_NONE)
    glutPassiveMotionFunc(mouse)
    glutDisplayFunc(main_scene)
    glutMainLoop()
