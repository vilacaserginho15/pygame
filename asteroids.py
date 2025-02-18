from circleshape import CircleShape
import pygame
from constants import * 
import random 
import math 

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity):
        super().__init__(x, y, radius)
        self.velocity = velocity 

    def wrap_around_screen(self,SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:  # Changed from SCREEN_WIDTH
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0  # Fixed to use position.y consistently
        elif self.position.y < 0:  # Changed from SCREEN_HEIGHT
            self.position.y = SCREEN_HEIGHT

    def draw(self,screen):
        points = []
        num_of_lumps = 8
        for lumps in range(num_of_lumps):
            angle = 2 * math.pi * lumps / num_of_lumps
            random_lumps = random.uniform(20.0, 22.0 ) 
            pos_lumps_x = self.position.x + random_lumps * math.cos(angle)
            pos_lumps_y = self.position.y + random_lumps * math.sin(angle) 
            points.append((pos_lumps_x, pos_lumps_y)) 

        pygame.draw.polygon(screen, "white", points) 


    def update(self, dt):
        self.position += self.velocity * dt 

    def split(self): 
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return []
        else:
            random_angles = random.uniform(20,50) 
            new_velocities_1 = self.velocity.rotate(random_angles) * 1.2
            new_velocities_2 = self.velocity.rotate(-random_angles) * 1.2
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            smaller_asteroid = Asteroid(self.position.x, self.position.y, new_radius, new_velocities_1) 
            smaller_asteroid_2 = Asteroid(self.position.x , self.position.y,  new_radius, new_velocities_2)
            return [smaller_asteroid, smaller_asteroid_2]
        