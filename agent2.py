from threading import Thread
from queue import Queue
import pygame
from enum import Enum

from defines import *

clock = pygame.time.Clock()


class StateMachine(Enum):
    REQUEST_STATE = 0
    READ_STATE = 1
    CALC_ACTION = 2
    REQUEST_REWARD = 3
    READ_REWARD = 4
    UPDATE_Q = 5


#########################
###     AGENT         ###
#########################


class AgentThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.state = StateMachine.REQUEST_STATE
        self.q = Queue()
        self.running = True

    def stop(self):
        self.running = False

    def get_top(self):
        if not self.q.empty():
            return self.q.get()
        else:
            return None

    def parse_msg(self, msg):
        if "key" not in msg.keys():
            return
        if msg["key"] == "BALL":
            self.state.ball_x = msg["x"]
            self.state.ball_y = msg["y"]
        elif msg["key"] == "GOAL":
            self.state.goal_x = msg["x"]
            self.state.goal_y = msg["y"]

    def tell(self, info):
        self.q.put(info)

    # logic
    # OBJECTIVE:
    #   Minimize disance from BALL to GOAL
    def action(self, delta_x, delta_y):
        event = pygame.event.Event(pygame.USEREVENT, {"key": "NONE"})

        if abs(delta_x) < 10:
            delta_x = 0
        if abs(delta_y) < 15:
            delta_y = 0

        if delta_x < 0:
            event = pygame.event.Event(
                pygame.USEREVENT, {"key": "ACTION" ,"action": Action.RIGHT})
            pygame.event.post(event)
        if delta_x > 0:
            event = pygame.event.Event(
                pygame.USEREVENT, {"key": "ACTION", "action": Action.LEFT})
            pygame.event.post(event)
        if delta_y > 0:
            event = pygame.event.Event(
                pygame.USEREVENT, {"key": "ACTION", "action": Action.UP})
            pygame.event.post(event)
        return event

# TODO add id field to request messages

    def run(self):
        while self.running:
            # print(self.state)
            # Requeat current state from world
            if self.state == StateMachine.REQUEST_STATE:
                event = pygame.event.Event(
                    pygame.USEREVENT, {"key":"REQUEST", "request": Requests.STATE})
                pygame.event.post(event)
                self.state = StateMachine.READ_STATE
            # Poll queue for state, calulate action, post action to queue
            elif self.state == StateMachine.READ_STATE:
                # print(self.state)
                msg = self.get_top()
                if msg:
                    if msg["key"] == "STATE":
                        self.action(msg["dx"], msg["dy"])
                        self.state = StateMachine.REQUEST_REWARD
            # Request the reward value from the world
            elif self.state == StateMachine.REQUEST_REWARD:
                # print(self.state)
                event = pygame.event.Event(
                    pygame.USEREVENT, {"key": "REQUEST", "request": Requests.REWARD})
                pygame.event.post(event)
                self.state = StateMachine.READ_REWARD
            # Given the reward, update Q table
            elif self.state == StateMachine.READ_REWARD:
                # print(self.state)
                msg = self.get_top()
                if msg:
                    if msg["key"] == "REWARD":
                        self.state = StateMachine.REQUEST_STATE
                
            clock.tick(60)
