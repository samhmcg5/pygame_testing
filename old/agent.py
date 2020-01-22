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
            event = pygame.event.Event(pygame.USEREVENT, {action="UP"})
            pygame.event.post(event)
            # self.q.put("UP")
            pygame.time.wait(1000)
            # self.q.put("LEFT")
            # pygame.time.wait(500)
            # self.q.put("RELEASE_L")
            # pygame.time.wait(500)
            # self.q.put("RIGHT")
            # pygame.time.wait(500)
            # self.q.put("RELEASE_R")
            # pygame.time.wait(500)

    def get_top(self):
        if not self.q.empty():
            return self.q.get()
        else:
            return None
