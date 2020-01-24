from enum import Enum

size = width, height = 800, 600
black = (0, 0, 0)
white = (255, 255, 255)
red = (178, 34, 34)
delta_t = (1.0/60.0)
gravity = 200

class Action(Enum):
    NONE = 0
    UP = 1
    RIGHT = 2
    LEFT = 3
    RELEASE_R = 4
    RELEASE_L = 5

class Requests(Enum):
    STATE = 0
    REWARD = 1