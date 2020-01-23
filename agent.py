from threading import Thread
from queue import Queue

import pygame

clock = pygame.time.Clock()

class AgentState:
    def __init__(self):
        self.ball_x = 0
        self.ball_y = 0
        self.goal_x = 0
        self.goal_y = 0
        self.vel_x = 0
        self.vel_y = 0

#########################
###     AGENT         ###
#########################
class AgentThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.state = AgentState()
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
        elif msg["key"] == "VEL":
            self.state.vel_x = msg["vel_x"]
            self.state.vel_y = msg["vel_y"]

    def tell(self, info):
        self.q.put(info)

    # logic
    # OBJECTIVE:
    #   Minimize disance from BALL to GOAL
    def action(self):
        event = pygame.event.Event(pygame.USEREVENT, {"key": "NONE"})
        delta_x = self.state.ball_x - self.state.goal_x
        delta_y = self.state.ball_y - self.state.goal_y
        # print(delta_x, delta_y)
        if abs(delta_x) < 10:
            delta_x = 0
        if abs(delta_y) < 15:
            delta_y = 0

        if delta_x < 0:
            if self.state.vel_x >= 0:
                event = pygame.event.Event(pygame.USEREVENT, {"key": "RIGHT"})
                pygame.event.post(event)
            else:
                event = pygame.event.Event(pygame.USEREVENT, {"key": "RIGHT"})
                # event = pygame.event.Event(pygame.USEREVENT, {"key": "RELEASE_L"})
                pygame.event.post(event)
        if delta_x > 0:
            if self.state.vel_x <= 0:
                event = pygame.event.Event(pygame.USEREVENT, {"key": "LEFT"})
                pygame.event.post(event)
            else:
                event = pygame.event.Event(pygame.USEREVENT, {"key": "LEFT"})
                # event = pygame.event.Event(pygame.USEREVENT, {"key": "RELEASE_R"})
                pygame.event.post(event)
        if delta_y > 0:
            event = pygame.event.Event(pygame.USEREVENT, {"key":"UP"})
            pygame.event.post(event)
        return event


    def run(self):
        prev_event = pygame.event.Event(pygame.USEREVENT, {"key": "NONE"})
        while self.running:
            msg = self.get_top()
            if msg:
                self.parse_msg(msg)

            event = self.action()

            if event.key is not prev_event.key and event.key is not "UP":
                print(event)
            prev_event = event
            
            # if event is not None:
            #     try:
            #         pygame.event.post(event)
            #     except pygame.error as e:
            #         print("ERROR", event)
            clock.tick(60)

            # event = pygame.event.Event(pygame.USEREVENT, {"key":"UP"})
            # event = pygame.event.Event(pygame.USEREVENT, {"key": "LEFT"})
            # event = pygame.event.Event(pygame.USEREVENT, {"key": "RELEASE_L"})
            # event = pygame.event.Event(pygame.USEREVENT, {"key": "RIGHT"})
            # event = pygame.event.Event(pygame.USEREVENT, {"key": "RELEASE_R"})

    
