from threading import Thread
from queue import Queue

import pygame

#########################
###     AGENT         ###
#########################
class AgentThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.q = Queue()
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            event = pygame.event.Event(pygame.USEREVENT, {"key":"UP"})
            pygame.event.post(event)
            pygame.time.wait(1000)
            event = pygame.event.Event(pygame.USEREVENT, {"key": "LEFT"})
            pygame.event.post(event)
            pygame.time.wait(500)
            event = pygame.event.Event(pygame.USEREVENT, {"key": "RELEASE_L"})
            pygame.event.post(event)
            pygame.time.wait(500)
            event = pygame.event.Event(pygame.USEREVENT, {"key": "RIGHT"})
            pygame.event.post(event)
            pygame.time.wait(500)
            event = pygame.event.Event(pygame.USEREVENT, {"key": "RELEASE_R"})
            pygame.event.post(event)
            pygame.time.wait(500)

    def get_top(self):
        if not self.q.empty():
            return self.q.get()
        else:
            return None
