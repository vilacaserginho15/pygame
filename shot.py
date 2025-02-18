import pygame
from constants import * 
from circleshape import * 

class Shot(CircleShape):
    def __init__(self):
        super().__init__(0, 0, SHOT_RADIUS)
       

    def draw(self,screen):
        pygame.draw.circle(screen, "white" , self.position , SHOT_RADIUS, 2) 

    def update(self, dt):
        self.position += self.velocity * dt 