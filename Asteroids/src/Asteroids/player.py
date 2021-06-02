'''
Created on May 14, 2021

@author: samhecht
'''
import math
import pygame
import random
import os
from Asteroids import bullet
from Asteroids import main
from Asteroids import asteroid
from Asteroids import line
from Asteroids import alien

class Player:
    WINDOW = pygame.display.set_mode((0, 0))
    FREQUENCY = math.pi/32
    ACCELERATION = 0.15
    DECELERATION_PERCENTAGE = 1.0/150
    MAX_SPEED = 8
    MAX_BULLETS = 10
    
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,0,255)
    
    EXTRA_LIFE_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'extraShip.wav'))
    BANG_MEDIUM_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'bangMedium.wav'))
    THRUST_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'thrust.wav'))

    
    MAX_THRUST_SOUND_LENGTH = 0.28761905431747437

    def __init__(self, center_x, center_y, player_number):
                    
        USER_POINT_1 = (center_x + 10, center_y - -20)
        USER_POINT_2 = (center_x + 0, center_y - 10)
        USER_POINT_3 = (center_x + -10, center_y - -20)
        USER_POINT_4 = (center_x + -5, center_y - -10)
        USER_POINT_5 = ((center_x + 5, center_y - -10))
        THRUST_POINT_1 = ((center_x - 3, center_y - -10))
        THRUST_POINT_2 = ((center_x, center_y - -18))
        THRUST_POINT_3 = ((center_x + 3, center_y - -10))

        self.vel_x = 0
        self.vel_y = 0
        
        self.heading = 0


        self.bullets = []
        

        self.flash = False

        self.points = [USER_POINT_1, USER_POINT_2, USER_POINT_3, USER_POINT_4, USER_POINT_5, THRUST_POINT_1, THRUST_POINT_2, THRUST_POINT_3]

        self.axis_of_rotation = (center_x, center_y)
        
        self.bounds = pygame.draw.polygon(self.WINDOW, (0,0,0), self.points)
        
        self.lives = 3
        
        self.score = 0
        
        
        self.is_losing_life = False
        self.is_hyperspacing = False
        
        self.hyperspace_timer = 0
        self.respawn_timer = 0
        
        self.lines = []
        
        self.thrust_timer = 0
        
        self.player_number = player_number
        
        self.color = (0,0,0)
        
        if self.player_number == 0:
            self.COLOR = self.WHITE
        elif self.player_number == 1:
            self.COLOR = self.BLUE
        else:
            self.COLOR = self.RED
            
        self.score_text = main.FONT.render(str(self.score), 1, self.COLOR)

        
        

    def rotate_points(self, delta_heading1):
        for _ in range(len(self.points)):
            point = self.points.pop(0)
            new_point = ((point[0]-self.axis_of_rotation[0])*math.cos(delta_heading1) - (point[1]-self.axis_of_rotation[1])*math.sin(delta_heading1) + self.axis_of_rotation[0], 
                 (point[0]-self.axis_of_rotation[0])*math.sin(delta_heading1) + (point[1]-self.axis_of_rotation[1])*math.cos(delta_heading1) + self.axis_of_rotation[1])
            self.points.append(new_point)



        
    def wrap_around(self):
        wrap_constant_x = 0
        wrap_constant_y = 0
        if self.axis_of_rotation[0] > 800 and self.bounds.width == 0:
            wrap_constant_x = -835
        elif self.axis_of_rotation[0] < 0 and self.bounds.width == 0:
            wrap_constant_x = 835
        if self.axis_of_rotation[1] > 800 and self.bounds.height == 0:
            wrap_constant_y = -835
        elif self.axis_of_rotation[1] < 0 and self.bounds.height == 0:
            wrap_constant_y = 835
    
        if wrap_constant_y != 0 or wrap_constant_x != 0:
            self.axis_of_rotation = (self.axis_of_rotation[0] + wrap_constant_x, self.axis_of_rotation[1] + wrap_constant_y)
            for _ in range(len(self.points)):
                point = self.points.pop(0)
                new_point = (point[0] + wrap_constant_x, point[1] + wrap_constant_y)
                self.points.append(new_point)
            
    
    
    def move_ship(self):
    
        self.axis_of_rotation = (self.axis_of_rotation[0] + self.vel_x, self.axis_of_rotation[1] - self.vel_y)
    
        self.wrap_around()
      
        for _ in range(len(self.points)):
            point = self.points.pop(0)
            new_point = (point[0] + self.vel_x, point[1] - self.vel_y)
            self.points.append(new_point)
        
    

    def get_motion_deltas(self, keys_pressed):
        delta_heading = 0
        
        self.flash = False
        if self.vel_x != 0:
            self.vel_x *= 1-self.DECELERATION_PERCENTAGE
        if self.vel_y != 0:
            self.vel_y *= 1-self.DECELERATION_PERCENTAGE
        if keys_pressed[pygame.K_RIGHT] and self.player_number <= 1:
            delta_heading += self.FREQUENCY
        if keys_pressed[pygame.K_LEFT] and self.player_number <= 1:
            delta_heading -= self.FREQUENCY
        if keys_pressed[pygame.K_UP] and abs(self.vel_x + self.ACCELERATION * math.sin(self.heading + delta_heading)) <= self.MAX_SPEED and self.player_number <= 1:
            self.vel_x += self.ACCELERATION * math.sin(self.heading + delta_heading)
            self.flash = True
        if keys_pressed[pygame.K_UP] and abs(self.vel_y + self.ACCELERATION * math.cos(self.heading + delta_heading)) <= self.MAX_SPEED and self.player_number <= 1:
            self.vel_y += self.ACCELERATION * math.cos(self.heading + delta_heading)
            self.flash = True
            
        if keys_pressed[pygame.K_d] and self.player_number == 2:
            delta_heading += self.FREQUENCY
        if keys_pressed[pygame.K_a] and self.player_number == 2:
            delta_heading -= self.FREQUENCY
        if keys_pressed[pygame.K_w] and abs(self.vel_x + self.ACCELERATION * math.sin(self.heading + delta_heading)) <= self.MAX_SPEED and self.player_number == 2:
            self.vel_x += self.ACCELERATION * math.sin(self.heading + delta_heading)
            self.flash = True
        if keys_pressed[pygame.K_w] and abs(self.vel_y + self.ACCELERATION * math.cos(self.heading + delta_heading)) <= self.MAX_SPEED and self.player_number == 2:
            self.vel_y += self.ACCELERATION * math.cos(self.heading + delta_heading)
            self.flash = True
        
        self.heading += delta_heading
        if self.flash and self.thrust_timer == 0:
            self.THRUST_SOUND.play()
            self.handle_thrust_timer(True)
        return delta_heading
    
    def handle_movement(self, keys_pressed):
        delta_heading = self.get_motion_deltas(keys_pressed)
        self.move_ship()
        self.rotate_points(delta_heading)
        self.handle_thrust_timer()
        
    def add_bullet(self):
        if len(self.bullets) < self.MAX_BULLETS:
            self.bullets.append(bullet.Bullet(self.axis_of_rotation[0] + 5 * math.sin(self.heading), 
                                              self.axis_of_rotation[1] - 5 * math.cos(self.heading), 
                                              self.heading)) 
        
    def handle_bullets(self):
        for _ in range(len(self.bullets)):
            bullet = self.bullets.pop(0)
            bullet.update_bullet()
            if bullet.distance_travelled < bullet.MAX_DISTANCE:
                self.bullets.append(bullet)
            
        
        
    def reset_bounds(self):
        self.bounds = pygame.draw.polygon(self.WINDOW, (0,0,0), self.points)
        
        
    
    
    def lose_life(self, offset) -> bool:
        prev_lives = self.lives
        prev_score = self.score
        

        
        if prev_lives - 1 <= 0:
            self.lives = 0
            return True
        self.__init__(main.WIDTH/2 + offset, main.HEIGHT/2 + 5, self.player_number)
        
        self.lives = prev_lives - 1
        self.score = prev_score
        self.score_text = main.FONT.render(str(self.score), 1, self.COLOR)
        
        return False
    
    
    def update_score(self, size, is_alien = None, is_player = None):
        
        extra_lives = self.score//10000
        if is_player != None:
            self.score += 2000
        elif is_alien is None:
            if size == asteroid.Asteroid.BIG:
                self.score += 20
            elif size == asteroid.Asteroid.MEDIUM:
                self.score += 50
            else:
                self.score += 100
        else:
            if size == alien.Alien.BIG:
                self.score += 200
            else:
                self.score += 500
                
        self.score_text = main.FONT.render(str(self.score), 1, self.COLOR)
        if extra_lives < self.score//10000:
            self.EXTRA_LIFE_SOUND.play()
            self.lives += 1
    
    
    def get_double_bounds(self) -> pygame.Rect:
        return pygame.Rect(self.bounds.x - self.bounds.width/2, self.bounds.y - self.bounds.height/2, self.bounds.width * 2, self.bounds.height * 2)
    
    

    def start_breaking_animation(self):
        self.BANG_MEDIUM_SOUND.play()
        self.is_losing_life = True
        self.lines = []
        for _ in range(4):
            self.lines.append(line.Line(self.axis_of_rotation))
        
    
    
    def move_lines(self):
        for l in self.lines:
            l.move_line()
        
        
    def handle_thrust_timer(self, start = False):
        if self.thrust_timer == 0 and start:
            self.thrust_timer += 1/main.FPS
        elif self.thrust_timer >= self.MAX_THRUST_SOUND_LENGTH:
            self.thrust_timer = 0
        elif self.thrust_timer > 0:
            self.thrust_timer += 1/main.FPS
        
        
    def hyperspace(self):
        change_in_x_y = (random.random() * 800, random.random() * 800)
        self.vel_x = 0
        self.vel_y = 0
        self.axis_of_rotation = (self.axis_of_rotation[0] + change_in_x_y[0], self.axis_of_rotation[1] + change_in_x_y[1])
        for _ in range(len(self.points)):
            point = self.points.pop(0)
            self.points.append((point[0] + change_in_x_y[0], point[1] + change_in_x_y[1]))
            
        self.wrap_around()
        self.is_hyperspacing = True
        


        