import pygame
from consts import *

class Entity:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.r = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collisions = {"right": False, "left": False, "top": False, "bottom": False}
        
    def draw(self, world):
        pygame.draw.rect(world, self.color, self.r)
        
    def apply_gravity(self):
        self.r.y += self.gravity
        
    def get_collision(self, collider_list):
        self.collisions = {"right": False, "left": False, "top": False, "bottom": False}
        i = self.r.collidelist(collider_list)
        if i != -1:
            overlap = self.r.clip(collider_list[i])
            if overlap.right < collider_list[i].centerx and overlap.height > overlap.width:
                self.collisions["right"] = True
            if overlap.left > collider_list[i].centerx and overlap.height > overlap.width:
                self.collisions["left"] = True
            if overlap.top > collider_list[i].centery and overlap.width > overlap.height:
                self.collisions["top"] = True
            if overlap.bottom < collider_list[i].centery and overlap.width > overlap.height:
                self.collisions["bottom"] = True
            return collider_list[i]
        else:
            return False
                
        
    def update(self):
        pass