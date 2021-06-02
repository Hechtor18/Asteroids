'''
Created on May 24, 2021

@author: samhecht
'''

from Asteroids import player
import math
import random

class Line:
    LINE_LENGTH = math.sqrt(math.pow(10 - 0, 2) + math.pow(20 - -10, 2))
    
    def __init__(self, axis_of_rotation):
        center_x = axis_of_rotation[0]
        center_y = axis_of_rotation[1]
        HEADING = random.random() * 2 * math.pi
        ORIENTATION = random.random() * math.pi
        self.p1 = (center_x + self.LINE_LENGTH/2 * math.cos(ORIENTATION), center_y + self.LINE_LENGTH/2 * math.sin(ORIENTATION))
        self.p2 = (center_x - self.LINE_LENGTH/2 * math.cos(ORIENTATION), center_y - self.LINE_LENGTH/2 * math.sin(ORIENTATION))
        #print(str(p1[0]) + "," + str(p1[1]))
        self.vel_x = math.cos(HEADING) / 1.75
        self.vel_y = math.sin(HEADING) / 1.75
        self.duration = random.random() * 25 + 35
        
    
    def move_line(self):
        self.p1 = (self.p1[0] + self.vel_x, self.p1[1] + self.vel_y)
        self.p2 = (self.p2[0] + self.vel_x, self.p2[1] + self.vel_y)