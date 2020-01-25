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


# Q LEARNING DEFINITIONS
COLLIDE_REWARD = 200
DISCRETE_SIZE = [160, 120]
discrete_bucket_size = [10, 10]
ACTION_NUM = 4
LEARNING_RATE = 0.3
DISCOUNT = 0.95
DX_MIN = -800
DY_MIN = -600

START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = 100
epsilon_decay_value = 1/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)
