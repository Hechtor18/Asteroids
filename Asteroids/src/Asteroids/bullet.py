'''
Created on May 14, 2021

@author: samhecht
'''

import math
import pygame
import os

class Bullet:
    RADIUS = 3
    VEL = 10
    MAX_DISTANCE = 500
    FIRE_BULLET_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'fire.wav'))

    
    
    def __init__(self, center_x, center_y, heading):
        self.x = center_x + self.RADIUS
        self.y = center_y + self.RADIUS
        self.heading = heading
        self.vel_x = self.VEL * math.sin(self.heading)
        self.vel_y = self.VEL * math.cos(self.heading)
        self.distance_travelled = 0
        
        self.bounds = self.get_bounds()
        
        self.FIRE_BULLET_SOUND.play()
        
    def update_bullet(self):
        self.x += self.vel_x
        self.y -= self.vel_y
        self.wrap_around()
        self.distance_travelled += self.VEL
        
        
    def wrap_around(self):
        if self.x > 800:
            self.x -= 800 
        elif self.x < 0:
            self.x += 800
        if self.y > 800:
            self.y -= 800
        elif self.y < 0:
            self.y += 800
            
    def get_bounds(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.RADIUS ,self.y - self.RADIUS, 2 * self.RADIUS, 2 * self.RADIUS)        
            
            
            
            
            
            
            
            
            
            
        