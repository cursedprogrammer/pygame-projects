import pygame
from entity import Entity
from consts import *

class Player(Entity):
    def __init__(self, x, y, width, height, color=RED):
        super().__init__(x, y, width, height, color)
        self.start_pos = [x, y]
        self.directions = {"right": False, "left": False, "up": False, "down": False}
        self.keys = pygame.key.get_pressed()
        self.vel = MOVEMENT_SPEED
        self.jump_timer = JUMP_TIME
        self.onAir = True
        self.isJumping = False
        self.isRunning = False
        self.turbo = False
        self.entity_type = PLAYER
        
        
    def get_keys(self):
        self.keys = pygame.key.get_pressed()
        self.directions["right"] = self.keys[pygame.K_RIGHT]
        self.directions["left"] = self.keys[pygame.K_LEFT]
        self.isJumping = self.keys[pygame.K_UP]
        self.isRunning = self.keys[pygame.K_LSHIFT]
        
        
    def jump(self):
        if self.isJumping and self.jump_timer > 0:
            self.onAir = True
            self.directions["up"] = True
            self.jump_timer -= 1
        elif self.directions["up"] and self.jump_timer > 0 and self.isJumping:
            self.jump_timer -= 1
        else:
            self.directions["up"] = False
            
    #def wall_jump(self):
    #    if self.onAir = True and self.isJumping:
        #    if self.collisions["right"]
            
    def run(self):
        if self.isRunning:
            self.vel = RUNNING_SPEED
        else:
            self.vel = MOVEMENT_SPEED
            
        
    def apply_gravity(self):
        if self.onAir and self.directions["up"] == False:
            self.directions["down"] = True
        
    def boundary_check(self):
        if self.r.right > X_RES:
            self.r.right = X_RES
        if self.r.left < 0:
            self.r.left = 0
        if self.r.top < 0:
            self.r.top = 0
        if self.r.bottom > Y_RES:
           self.r.bottom = Y_RES
    
    def horizontal_collision(self, collider_list):
        col_rect = self.get_collision(collider_list)
        if self.directions["right"] and col_rect:
            self.r.right = col_rect.left
        elif self.directions["left"] and col_rect:
            self.r.x = col_rect.x + col_rect.width
        
    def vertical_collision(self, collider_list):
        col_rect = self.get_collision(collider_list)
        if self.directions["up"] and col_rect:
            self.r.y = col_rect.y + col_rect.height
        elif self.directions["down"] and col_rect:
            self.r.y = col_rect.y - col_rect.height
            self.directions["down"] = False
            if self.isJumping == False:
                self.jump_timer = JUMP_TIME
                self.onAir = False
        else:
            self.onAir = True
    
        
        
        
    def move_x(self):
        if self.directions["right"]:
            self.r.x += self.vel
        if self.directions["left"]:
            self.r.x -= self.vel
        
    def move_y(self):
        if self.directions["up"]:
            self.r.top -= JUMP_FORCE
        elif self.directions["down"]:
            self.r.bottom += GRAVITY

            
    def update(self, rects):
        self.apply_gravity()        
        self.get_keys()
        self.run()
        self.move_x()
        self.horizontal_collision(rects)
        self.move_y()
        self.vertical_collision(rects)
        self.jump()