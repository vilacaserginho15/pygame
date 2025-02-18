import pygame
import math
from laser_beam import * 

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def collision(self, other):
        distance = self.position.distance_to(other.position) 
        if distance <= self.radius + other.radius: 
            return True
        else:
            return False 
        
    def check_for_laser_collision(self,laser):
        to_asteroid_x = self.position.x - laser.start_pos.x #position of laser and asteroid
        to_asteroid_y = self.position.y - laser.start_pos.y 
        angle_to_center = math.atan2(to_asteroid_y, to_asteroid_x) #finding the angle of laser to asteroid
        relative_angle = angle_to_center - laser.angle #pointing the angle at the right direction
        distance_to_asteroid = math.sqrt(to_asteroid_x ** 2 + to_asteroid_y ** 2) #find distance using math.sqrt from asteroid to laser after finding angle
        final_distance = abs(distance_to_asteroid * math.sin(relative_angle)) 
        return final_distance <= self.radius

    def check_for_player_collision(self,player):
        triangle_points = player.triangle() 
        collision_buffer = 0.7
        adjusted_radius = self.radius * collision_buffer
        distance_1 = self.position.distance_to(triangle_points[0])
        distance_2 = self.position.distance_to(triangle_points[1]) 
        distance_3 = self.position.distance_to(triangle_points[2]) 
        line_ab_distance = self.distance_to_line(triangle_points[0], triangle_points[1])
        line_bc_distance = self.distance_to_line(triangle_points[1], triangle_points[2]) 
        line_ac_distance = self.distance_to_line(triangle_points[0], triangle_points[2]) 
        if (adjusted_radius > distance_1 or
        adjusted_radius > distance_2 or
        adjusted_radius > distance_3 or
        adjusted_radius > line_ab_distance or
        adjusted_radius > line_bc_distance or
        adjusted_radius > line_ac_distance):
            return True 

        
    def distance_to_line(self, point_1, point_2):
        line_vector = point_1 - point_2 
        point_vector = self.position - point_1 
        line_length = line_vector.length() 
        t = max(0, min(1, point_vector.dot(line_vector) / (line_length * line_length))) 
        projection = point_1 + line_vector * t 
        return (self.position - projection).length()
        

    
    def draw(self, screen):
        # sub-classes must override 
        pass 

    def update(self, dt):
        # sub-classes must override
        pass