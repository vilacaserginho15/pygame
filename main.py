import pygame
import sys 
from constants import *
from circleshape import *
from asteroids import * 
from asteroidfield import * 
from shot import *
from player import *
 

def main():
    pygame.display.init()
    pygame.font.init() 
    font = pygame.font.Font(None, 36)
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}") 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0 
    drawables = pygame.sprite.Group()
    updatables = pygame.sprite.Group() 
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    laser_shots = pygame.sprite.Group() 
    explosions = pygame.sprite.Group() 
    AsteroidField.containers = (updatables,) 
    Asteroid.containers = (asteroids, drawables, updatables) 
    Player.containers = (drawables, updatables) 
    Shot.containers = (shots, drawables, updatables) 
    LaserBeam.containers = (drawables, laser_shots) 
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, asteroids)
    asteroid_field = AsteroidField() 

    while True: 
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               return 
       updatables.update(dt)
       for all_objects in updatables:
           if hasattr(all_objects, 'wrap_around_screen'):
                all_objects.wrap_around_screen(SCREEN_WIDTH, SCREEN_HEIGHT) 
       for asteroid in asteroids:
           collision = asteroid.check_for_player_collision(player)
           if collision and not player.is_invulnerable :
                print(f"Collision detected! Invulnerable: {player.is_invulnerable}")
                if player.extra_lives <= 1:
                    print("Game over!") 
                    sys.exit()
                player.respawn()
                player.is_invulnerable = True 
                player.update_vulnerability(dt)
       for all_asteroids in asteroids: 
            for all_shots in shots:
                if all_asteroids.collision(all_shots): 
                    all_shots.kill()
                    all_asteroids.split()
                    player.is_accelerated = True 
                    current_time = pygame.time.get_ticks() 
                    player.kill_count += player.kill_increment 
                    player.multiple_lives()
                    player.get_shield_powerup(current_time)
                    player.update_shield(current_time) 
       for all_asteroids in asteroids:
           for all_laser_shots in laser_shots:
               if all_asteroids.check_for_laser_collision(all_laser_shots):
                   all_laser_shots.kill() 
                   all_asteroids.split()
                   player.is_accelerated = True 
                   current_time  = pygame.time.get_ticks() 
                   player.kill_count += player.kill_increment 
                   player.multiple_lives() 
                   player.get_shield_powerup(current_time)
                   player.update_shield(current_time) 
    
                   
       screen.fill((0,0,0)) 
       screen_text_2 = font.render(f"Asteroid Kill Count: {player.kill_count} Extra Lives: {player.extra_lives} ", True, 'WHITE') 
       rectangle_2_text = screen_text_2.get_rect()
       screen_text_2_location = (screen.get_width() - rectangle_2_text.width, 0)
       screen.blit(screen_text_2,screen_text_2_location)
       for drawable in drawables:
           drawable.draw(screen) 
       pygame.display.flip()   
       dt = clock.tick(60)/1000

if __name__ == "__main__":
    main() 