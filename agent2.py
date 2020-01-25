from threading import Thread
from queue import Queue
import pygame
from enum import Enum
import numpy as np

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
        self.q_table = np.random.uniform(
            low=-1, high=1, size=(DISCRETE_SIZE + [ACTION_NUM]))

    def stop(self):
        self.running = False

    def get_top(self):
        if not self.q.empty():
            return self.q.get()
        else:
            return None

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

    def get_discrete_state(self, dx, dy):
        disc_dx = (dx - DX_MIN) / discrete_bucket_size[0]
        disc_dy = (dy - DY_MIN) / discrete_bucket_size[1]
        return int(disc_dx), int(disc_dy)

    # Get action from Q table
    # state = dx, dy
    def action_q(self, discrete_state):
        action = np.argmax(self.q_table[discrete_state])
        return Action(action)

# TODO add id field to request messages

    def run(self):
        action = 0
        discrete_state = [0,0]
        counter = 0
        epsilon = 1
        episode = 0
        # temp for debugging
        dx, dy = 0,0

        while self.running:
            # Requeat current state from world
            if self.state == StateMachine.REQUEST_STATE:
            # print(self.state)
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
                        discrete_state = self.get_discrete_state(msg["dx"], msg["dy"])
                        dx, dy = msg["dx"], msg["dy"]
                        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
                            epsilon -= epsilon_decay_value

                        if np.random.random() > epsilon:
                            action = self.action_q(discrete_state)
                        else:
                            print("RANDOM")
                            action = Action(np.random.randint(0, ACTION_NUM))
                        
                        event = pygame.event.Event(
                            pygame.USEREVENT, {"key": "ACTION", "action": action})
                        pygame.event.post(event)
                        
                        # reset reward counter
                        counter = 0
                        if episode < 1000000:
                            episode += 1
                        self.state = StateMachine.REQUEST_REWARD
            
            # Request the reward value from the world
            elif self.state == StateMachine.REQUEST_REWARD:
                # print(self.state)
                counter += 1
                if counter >= 5:
                    counter = 0
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
                        reward = msg["value"]
                        
                        new_discrete_state = self.get_discrete_state(
                            msg["dx"], msg["dy"])
                        
                        max_future_q = np.max(self.q_table[new_discrete_state])
                        
                        current_q = self.q_table[discrete_state + (action.value,)]
                        
                        print(int(dx), int(dy), discrete_state, reward, action)

                        if reward == COLLIDE_REWARD:
                            print("--> GOAL")
                            new_q = reward
                        else:
                            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
                        self.q_table[discrete_state + (action.value,)] = new_q
                        self.state = StateMachine.REQUEST_STATE
                
            clock.tick(60)
