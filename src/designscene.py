import random
from random import randint
from OpenGL.GLUT import *
glutInit()
divider = [int(glutGet(GLUT_SCREEN_HEIGHT) * 0.2),
           int(glutGet(GLUT_SCREEN_HEIGHT) * 0.4),
           int(glutGet(GLUT_SCREEN_HEIGHT) * 0.6),
           int(glutGet(GLUT_SCREEN_HEIGHT) * 0.8),
           int(glutGet(GLUT_SCREEN_HEIGHT))]

vertical_displacement = 2  # 'DECREASING'  = decreasing vertical motion which means 'MORE STABLE' Motion
x_displacement = 0.2  # Speed of small fish


def random_offset():
    return randint(vertical_displacement + 20, int(glutGet(GLUT_SCREEN_HEIGHT)) - vertical_displacement - 20)


def generate_a():
    a = [[0, divider[0], random.choice([2, 5]), 1, 0, random_offset(), 1],
         [int(glutGet(GLUT_SCREEN_WIDTH)) * 0.8, divider[1], random.choice([2, 5]), 1, 1, random_offset(), 3],
         [0, divider[2], random.choice([2, 5]), 1, 2, random_offset(), 5],
         [int(glutGet(GLUT_SCREEN_WIDTH)) * 0.1, divider[3], random.choice([2, 5]), 1, 3, random_offset(), 7],
         [0, divider[4], random.choice([2, 5]), 1, 4, random_offset(), 9],
         [int(glutGet(GLUT_SCREEN_WIDTH)) * 0.9, divider[0], random.choice([2, 5]), -1, 4, random_offset(), 0],
         [int(glutGet(GLUT_SCREEN_WIDTH)), divider[1], random.choice([2, 5]), -1, 3, random_offset(), 2],
         [int(glutGet(GLUT_SCREEN_WIDTH)) * 0.25, divider[2], random.choice([2, 5]), -1, 2, random_offset(),
          4],
         [int(glutGet(GLUT_SCREEN_WIDTH)), divider[3], random.choice([2, 5]), -1, 1, random_offset(), 6],
         [int(glutGet(GLUT_SCREEN_WIDTH)) * 0.75, divider[4], random.choice([2, 5]), -1, 0, random_offset(),
          8]]
    return a
