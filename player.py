from constants import *
import pygame
from circleshape import CircleShape
from shot import * 
from asteroids import *
import random 
from laser_beam import *





class Player(CircleShape): 
    def __init__(self,x,y, asteroids):
        super().__init__(x,y,PLAYER_RADIUS) 
        self.rotation = 0 
        self.timer = 0 
        self.extra_lives = 1
        self.rewarded_kills = 0
        self.kill_count = 0
        self.kill_increment = 1 
        self.asteroids = asteroids 
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.INVULNERABLE_DURATION = 3000
        self.is_accelerated = False
        self.acceleration_timer = 0 
        self.acceleration_duration = 5000 
        self.shield_power = False
        self.shield_power_timer = 0
        self.shield_power_duration = 5000 

    def wrap_around_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:  # Changed from SCREEN_WIDTH
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0  # Fixed to use position.y consistently
        elif self.position.y < 0:  # Changed from SCREEN_HEIGHT
            self.position.y = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt) 
        if keys[pygame.K_d]:
            self.rotate(dt) 
        if keys[pygame.K_w]: 
            self.move(dt) 
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot() 
        if keys[pygame.K_q]:
            self.shoot_laser() 
        if self.timer > 0:
            self.timer -= dt 
            if self.timer < 0:
                self.timer = 0 


    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        if self.is_accelerated:
            self.position += forward * PLAYER_ACCELERATION * dt

    def updated_acceleration(self,current_time):
        if self.is_accelerated:
            if current_time - self.acceleration_timer > self.acceleration_duration:
                self.is_accelerated = False 


    def shoot_laser(self):
        if self.timer > 0:
            return False
        else:
            self.timer = LASER_SHOT_COOLDOWN
            new_laser_shot = LaserBeam(self.position, self.rotation)
            return new_laser_shot
        
    
    def shoot(self):    
        if self.timer > 0: 
            return False
        else:
            self.timer = PLAYER_SHOOT_COOLDOWN
            new_shot = Shot() 
            new_shot.position = self.position.copy()
            new_shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED 
            return new_shot 
        
    def update_vulnerability(self,current_time):
        if self.is_invulnerable: 
            if current_time - self.invulnerable_timer > self.INVULNERABLE_DURATION:
                self.is_invulnerable = False

    def update_shield(self,current_time): 
        if self.shield_power:
            if current_time - self.shield_power_timer > self.shield_power_duration: 
                self.shield_power = False 

    def get_shield_powerup(self,current_time):
        if self.kill_count > self.rewarded_kills + 50: 
            self.rewarded_kills = self.kill_count
            self.shield_power = True 
            self.shield_power_timer = current_time
        

    def respawn(self):
         if self.extra_lives <= 0: 
            print("No lives left, killing player")
            self.kill()
         else:
            self.extra_lives -= 1 
            print(f"Respawning. Lives remaining: {self.extra_lives}")
            safe_position = True
            while not safe_position:
                safe_position = True 
                self.x = random.randint(0, SCREEN_WIDTH) 
                self.y = random.randint(0, SCREEN_HEIGHT)
                for asteroid in self.asteroids: 
                    if self.collision(asteroid):
                        safe_position = False
                        break
                self.is_invulnerable = True
                self.invulnerable_timer = pygame.time.get_ticks()
                
         

    def multiple_lives(self):
         if self.kill_count >= self.rewarded_kills + 10:
             self.extra_lives += 1 
             self.rewarded_kills += 10 

    
    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]