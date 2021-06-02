'''
Created on May 25, 2021

@author: samhecht
'''

import math
import random

class Dot:
    
    RADIUS = 2
    VEL = 1
    
    
    
    def __init__(self, center_x, center_y, heading, asteroid_size):
        self.x = center_x + self.RADIUS
        self.y = center_y + self.RADIUS
        self.heading = heading
        self.vel_x = self.VEL * math.sin(self.heading)
        self.vel_y = self.VEL * math.cos(self.heading)
        self.distance_travelled = 0
        self.max_distance = random.random() * 20 + 20 * asteroid_size
        
        
        
    def handle_movement(self, dots):
        if self.distance_travelled < self.max_distance:
            self.x += self.vel_x
            self.y -= self.vel_y
            self.distance_travelled += self.VEL
        else:
            dots.remove(self)