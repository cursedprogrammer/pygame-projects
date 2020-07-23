import pygame
from consts import *
from entity import Entity

class Goal(Entity):
    def __init__(self, x, y, width, height, color=GREEN):
        super().__init__(x, y, width, height, color)
        self.entity_type = GOAL
        