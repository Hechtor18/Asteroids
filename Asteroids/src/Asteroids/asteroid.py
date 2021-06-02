'''
Created on May 15, 2021

@author: samhecht
'''

import math
import random
import pygame
import os
from Asteroids import main
from Asteroids import dot


class Asteroid:
    WINDOW = pygame.display.set_mode((0, 0))
    BIG = 4
    MEDIUM = 2
    SMALL = 1
    
    BANG_LARGE_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'bangLarge.wav'))
    BANG_MEDIUM_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'bangMedium.wav'))
    BANG_SMALL_SOUND = pygame.mixer.Sound(os.path.join('Sound Effects', 'bangSmall.wav'))
    
    MIN_VEL = 2
    MAX_VEL = 4 - MIN_VEL
    
    #Add 5 more asteroids so that there are 8
    
    ASTEROID_1 = [(-10,-8), (-10,-3), (-7,5), (-9,9), (-2,10), (5,10), (9,4), (6,-3), (9,-9), (2,-10), (-4,-7)]
    ASTEROID_2 = [(-10,-7), (-9,-2), (-7,5), (-3,9), (-2,10), (5,5), (9,4), (6,-7), (9,-9), (5,-10)]
    ASTEROID_3 = [(-10,-10), (-7,0), (-10,10), (-7,10), (-4,7), (3,9), (9,8), (6,0), (9,-9), (0,-7)]
    ASTEROID_4 = [(-10,-10), (-7,-5), (-9,0), (-7,5), (-10,10), (0,7), (2, 9), (8,9), (6,6), (10,-6), (6,-10), (-1,-8)]
    ASTEROID_5 = [(-8,-9), (-4, -9), (0, -3), (9, -9), (7, -3), (10, 0), (10, 7), (4, 9), (0,8), (-2, 9), (-4,8), (-6,9), (-8,8), (-10,9), (-8, 3)]
    ASTEROID_6 = [(-8,-8), (-6, -4), (-9, 7), (0, 8), (5, 10), (9,9), (7, -3), (8,-10), (4,-7), (-5,-9)]
    ASTEROID_7 = [(-9,-9),(-7, -3), (-9, -1), (-7, 5), (-9, 7), (-7, 9), (0, 10), (4, 5), (9, 10),(8, 5), (6, 0), (9, 2), (8, -5), (10, -10), (3, -7), (-4, -9)]
    ASTEROID_8 = [(-7,-9), (-6, 1), (-7,3), (-10, 9), (-3, 7), (5, 6), (9, 9), (6, -1), (8, -4), (9, -10), (5, -6), (0, -9), (-6, -10)]

        
    ASTEROIDS = [ASTEROID_1, ASTEROID_2, ASTEROID_3, ASTEROID_4, ASTEROID_5, ASTEROID_6, ASTEROID_7, ASTEROID_8]
    
    
    
    def __init__(self, size = None, center_x = None, center_y = None):
        if size is None:
            self.size = self.BIG
        else:
            self.size = size/2
        if center_x is None or center_y is None:
            self.center_x = random.random() * main.WIDTH
            self.center_y = random.random() * main.HEIGHT
        else:
            self.center_x = center_x
            self.center_y = center_y
        self.heading = random.random() * 2 * math.pi
        VEL = (random.random() * self.MAX_VEL) + self.MIN_VEL
        self.VEL_X = VEL / self.size * math.sin(self.heading)
        self.VEL_Y = VEL / self.size * math.cos(self.heading)
        self.type = (int)(random.random() * len(self.ASTEROIDS))
        self.points = []

        for point in self.ASTEROIDS[self.type]:
            self.points.append((self.center_x + point[0] * self.size, self.center_y - point[1] * self.size))
        rotate_around(self.points, self.center_x, self.center_y)
        
        self.wrap_constant_x = 0
        self.wrap_constant_y = 0
        
        self.bounds = pygame.draw.polygon(self.WINDOW, (0,0,0), self.points)
        
        self.width = self.bounds.width
        self.height = self.bounds.height
        self.dots = []
        
        
    def start_breaking_animation(self):
        for _ in range(2 + round(1 + random.random() * 2)):
            self.dots.append(dot.Dot(self.center_x, self.center_y, random.random() * 2 * math.pi, self.size))
    
    def handle_breaking_animation(self):
        for dot in self.dots:
            dot.handle_movement(self.dots)
    
    def handle_movement(self):
        self.center_x += self.VEL_X
        self.center_y -= self.VEL_Y
       
        self.wrap_around()
        self.update_points()
        
    
    def wrap_around(self):
        if self.center_x - self.width/2 > 800 and self.VEL_X > 0:
            #print("RIGHT TO LEFT")
            self.center_x -= 800 + self.width 
            self.wrap_constant_x = -800 - self.width  
        elif self.center_x + self.width/2 < 0 and self.VEL_X < 0:
            #print("LEFT TO RIGHT")
            self.center_x += 800 + self.width 
            self.wrap_constant_x = 800 + self.width 
            
            
        if self.center_y - self.height/2 > 800 and self.VEL_Y < 0:
            #print("BOTTOM TO TOP")
            self.center_y -= 800 + self.height 
            self.wrap_constant_y = -800 - self.height  
        elif self.center_y + self.height/2 < 0 and self.VEL_Y > 0:
            #print("TOP TO BOTTOM")
            self.center_y += 800 + self.height
            self.wrap_constant_y = 800 + self.height 
        
        
        
        
    def update_points(self):
        for _ in range(len(self.points)):
            point = self.points.pop(0)
            self.points.append((point[0] + self.VEL_X + self.wrap_constant_x, point[1] - self.VEL_Y + self.wrap_constant_y))
            
        self.wrap_constant_x = 0
        self.wrap_constant_y = 0
        
        
    def split_asteroid(self, asteroids, player = None):
        if self.size == self.BIG:
            self.BANG_LARGE_SOUND.play()
        elif self.size == self.MEDIUM:
            self.BANG_MEDIUM_SOUND.play()
        else:
            self.BANG_SMALL_SOUND.play()
        self.start_breaking_animation()
        if player is not None:
            player.update_score(self.size)
        if self.size != self.SMALL:
            asteroids.remove(self)
            small_aster_1 = Asteroid(self.size, self.center_x, self.center_y)
            small_aster_2 = Asteroid(self.size, self.center_x, self.center_y)
            asteroids.append(small_aster_1)
            asteroids.append(small_aster_2)
            
            return
        
        
        asteroids.remove(self)
        

                
    
        
def rotate_around(points, center_x, center_y) -> [(float,float)]:
    rotation = round(random.random() * 4 - 0.5) * math.pi / 2
    for _ in range(len(points)):
        point = points.pop(0)
        rotated_point = ((point[0]-center_x)*math.cos(rotation) - (point[1]-center_y)*math.sin(rotation) + center_x, 
                 (point[0]-center_x)*math.sin(rotation) + (point[1]-center_y)*math.cos(rotation) + center_y)
        points.append(rotated_point)
    
    return points
    
    
         