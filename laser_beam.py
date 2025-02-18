import pygame
import math
from constants import *  

class LaserBeam(pygame.sprite.Sprite): 
    def __init__(self,start_pos, angle ):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().init__()

        self.start_pos = start_pos 
        self.angle = math.radians(angle) 

        beam_lenght = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)

        self.end_1 = self.start_pos.x + beam_lenght * math.cos(self.angle)
        self.end_2 = self.start_pos.y + beam_lenght * math.sin(self.angle) 

    def draw(self,screen):
        pygame.draw.line(screen,"red", self.start_pos, (self.end_1, self.end_2) , 3)

    

    