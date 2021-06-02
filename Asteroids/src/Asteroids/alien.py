'''
Created on May 25, 2021

@author: samhecht
'''

import random
import math
import pygame
import os
from Asteroids import bullet
from Asteroids import dot
from Asteroids import main


class Alien:
    BIG = 2
    SMALL = 1
    MAX_BULLETS = 1
    WINDOW = pygame.display.set_mode((0, 0))

    
    ALIEN_POINTS = [(-15,-4), (-8,-10) , (8,-10), (15,-4), (-15,-4), (-8,2), (-4,10), (4,10), (8,2), (15,-4), (-8,2), (8,2)]
    
    SAUCER_BIG_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'saucerBig.wav'))
    SAUCER_SMALL_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'saucerSmall.wav'))
    
    SAUCER_BIG_SOUND.set_volume(0.60)
    SAUCER_SMALL_SOUND.set_volume(0.60)
    
    BANG_MEDIUM_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'bangMedium.wav'))
    BANG_SMALL_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'bangSmall.wav'))


    SAUCER_BIG_SOUND_LENGTH = 9/30
    SAUCER_SMALL_SOUND_LENGTH = 15/60 #0.12417233735322952
    
    def __init__(self, isSmall, center_x = None, center_y = None):
        self.vel_y = 0
        self.center_x = round(random.random()) * 900 - 50 if center_x == None else center_x
        self.vel_x = 2 if self.center_x < 0 else -2
        self.center_y = random.random() * 800 if center_y == None else center_y
        self.size = self.SMALL if isSmall or random.random() * 5 > 4 else self.BIG
        self.points = []
        for point in self.ALIEN_POINTS:
            self.points.append((-self.size * point[0] + self.center_x, -self.size * point[1] + self.center_y))
        self.movement_duration = random.random() * 30 + 90
        self.time_moving_y = 0
        self.bullets = []
        self.bounds = pygame.draw.polygon(self.WINDOW, (0,0,0), self.points[:10])
        
        self.dots = []
        
        self.sound_timer = 0
        
        self.handle_saucer_sound()
        
    def start_breaking_animation(self):
        for _ in range(2 + round(1 + random.random() * 2)):
            self.dots.append(dot.Dot(self.center_x, self.center_y, random.random() * 2 * math.pi, self.size))
    
    def handle_breaking_animation(self):
        for dot in self.dots:
            dot.handle_movement(self.dots)
    
    
    def handle_movement(self, aliens):
        if (self.vel_x > 0 and self.center_x - self.bounds.width/2 > 800) or (self.vel_x < 0 and self.center_x + self.bounds.width/2 < 0):
            aliens.remove(self)
            return
        if self.time_moving_y == 0 and random.random() * 180 > 178:
            self.vel_y = -2 if round(random.random()) - 1 < 0 else 2
            self.time_moving_y += 1
        elif self.time_moving_y > self.movement_duration:
            self.time_moving_y = 0
            self.vel_y = 0
        elif self.time_moving_y > 0:
            self.time_moving_y += 1
            
        self.center_x += self.vel_x
        self.center_y += self.vel_y
        for _ in range(len(self.points)):
            point = self.points.pop(0)
            self.points.append((point[0] + self.vel_x, point[1] + self.vel_y))
        
        self.wrap_around()
        
        self.sound_timer += 1/main.FPS
        self.handle_saucer_sound()
        
        
    def wrap_around(self):
        wrap_constant_y = 0
        if self.center_y > 800 and self.bounds.height == 0:
            wrap_constant_y = -800 - 20 * self.size
        elif self.center_y < 0 and self.bounds.height == 0:
            wrap_constant_y = 800 + 20 * self.size
    
        if wrap_constant_y != 0:
            self.axis_of_rotation = (self.center_x, self.center_y + wrap_constant_y)
            for _ in range(len(self.points)):
                point = self.points.pop(0)
                self.points.append((point[0], point[1] + wrap_constant_y))
                
    
    
    
    def handle_bullets(self, player_1):
        if len(self.bullets) != 0:
            self.bullets[0].update_bullet()
        if len(self.bullets) < self.MAX_BULLETS and self.size == self.BIG and random.random() * 100 > 98:
            self.bullets.append(bullet.Bullet(self.center_x, self.center_y, random.random() * 2 * math.pi))
            
        elif len(self.bullets) < self.MAX_BULLETS and self.size == self.SMALL and random.random() * 100 > 98 and self.center_x > 0 and self.center_x < 800:
            x_multiplier = 1 if player_1.axis_of_rotation[0] < 400 else -1
            x_direction = player_1.axis_of_rotation[0] - self.center_x if abs(player_1.axis_of_rotation[0] - self.center_x) < abs(player_1.axis_of_rotation[0] + x_multiplier * 800 - self.center_x) else player_1.axis_of_rotation[0] - self.center_x + x_multiplier * 800
            y_multiplier = 1 if player_1.axis_of_rotation[1] < 400 else -1
            y_direction = player_1.axis_of_rotation[1] - self.center_y if abs(player_1.axis_of_rotation[1] - self.center_y) < abs(player_1.axis_of_rotation[1] + y_multiplier * 800 - self.center_y) else player_1.axis_of_rotation[1] - self.center_y + y_multiplier * 800
            heading_multiplier = 1 if x_direction > 0 else -1
            
            variance = max(0, (((80000 - player_1.score)//10000) * (random.random() * 0.05)))
            variance_multiplier = 1 if round(random.random()) == 1 else -1
            self.bullets.append(bullet.Bullet(self.center_x, self.center_y, math.pi/2 * heading_multiplier + variance * variance_multiplier + math.atan(y_direction/x_direction)))
            
            
            
            
        if len(self.bullets) > 0 and self.bullets[0].distance_travelled > self.bullets[0].MAX_DISTANCE:
            self.bullets.pop(0)
            
            
            
    def break_ufo(self, aliens, p = None):
        if self.size == self.BIG:
            self.BANG_MEDIUM_SOUND.play()
        else:
            self.BANG_SMALL_SOUND.play()
        self.start_breaking_animation()
        if p is not None:
            p.update_score(self.size, True)
        aliens.remove(self)
            
    def handle_saucer_sound(self):
        if self.size == self.BIG and self.sound_timer > self.SAUCER_BIG_SOUND_LENGTH:
            self.sound_timer = 0
        elif self.size == self.SMALL and self.sound_timer > self.SAUCER_SMALL_SOUND_LENGTH:
            self.sound_timer = 0
            
        if self.size == self.BIG and self.sound_timer == 0:
            self.SAUCER_BIG_SOUND.play()
        elif self.sound_timer == 0:
            self.SAUCER_SMALL_SOUND.play()
        
        self.sound_timer += 1/main.FPS
        
        
        
        
        
        
            
            