import pygame
from player import *
from goal import *
from consts import *

def get_level(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
    
        

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(SCREEN_RES)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(CAPTION)
        self.rects = []
        self.coins = []
        self.spikes = []
        self.player = None
        self.goal = None
        self.score = 0
        self.level_width = None
        self.level_height = None
        level_map = get_level("level1.txt")
        self.create_level(level_map)
        self.player_score = pygame.font.SysFont("arial", 25)
        self.shift_vel_x = self.player.vel
        self.shift_vel_y = GRAVITY
        
        
    def create_level(self, map):
        x_coord = 0
        y_coord = 0
        for row in map:
            x_coord = 0
            for col in row:
                if col == "1":
                    self.rects.append(pygame.Rect(x_coord, y_coord, BLOCK_SIZE, BLOCK_SIZE))
                elif col == "2":
                    self.player = Player(x_coord, y_coord, PLAYER_WIDTH, PLAYER_HEIGHT)
                elif col == "3":
                    self.goal = Goal(x_coord, y_coord, BLOCK_SIZE, BLOCK_SIZE)
                elif col == "4":
                    self.coins.append(pygame.Rect(x_coord, y_coord, 10, 10))
                elif col == "5":
                    self.spikes.append(pygame.Rect(x_coord, y_coord, BLOCK_SIZE, BLOCK_SIZE))
                x_coord += BLOCK_SIZE
            y_coord += BLOCK_SIZE

    def draw_rects(self):
        for i in self.rects:
            pygame.draw.rect(self.window, BLUE, i)
            
    def draw_entities(self):
        self.player.draw(self.window)
        self.goal.draw(self.window)
        
    def draw_spikes(self):
        for s in self.spikes:
            pygame.draw.polygon(self.window, BLUE, )
            
    def draw_coins(self):
        for c in self.coins:
            pygame.draw.rect(self.window, YELLOW, c)
            
    def manage_shift_vel(self):
        self.shift_vel_x = self.player.vel - 5
            
    def shift_world_horizontal(self, dir):
        if dir == "left":
            for r in self.rects:
                r.x -= self.shift_vel_x
            for c in self.coins:
                c.x -= self.shift_vel_x
            self.goal.r.x -= self.shift_vel_x
        elif dir == "right":
            for r in self.rects:
                r.x += self.shift_vel_x
            for c in self.coins:
                c.x += self.shift_vel_x
            self.goal.r.x += self.shift_vel_x
            
    def world_scroll_horizontal(self):
        if self.player.r.right > 350:
            self.player.r.x = 350 - self.player.r.width
            self.shift_world_horizontal("left")
        elif self.player.r.left < 150:
            self.player.r.x = 150
            self.shift_world_horizontal("right")
            
            
    def shift_world_vertical(self, dir):
        if dir == "down":
            for r in self.rects:
                r.y += self.shift_vel_y
            for c in self.coins:
                c.y += self.shift_vel_y
            self.goal.r.y += self.shift_vel_y
        elif dir == "up":
            for r in self.rects:
                r.y -= self.shift_vel_y
            for c in self.coins:
                c.y -= self.shift_vel_y
            self.goal.r.y -= self.shift_vel_y
            
    def world_scroll_vertical(self):
        if self.player.r.top < Y_RES // 2:
            self.player.r.y = Y_RES // 2
            self.shift_world_vertical("down")
        elif self.player.r.bottom > Y_RES // 2 + self.player.r.height:
            self.player.r.y = Y_RES // 2
            self.shift_world_vertical("up")
            
            
    def coin_collision(self):
        c = self.player.r.collidelist(self.coins)
        if c != -1:
            del self.coins[c]
            self.score += 1
    
    def draw_score(self):    
        self.score_txt = self.player_score.render("Score: " + str(self.score), 0, WHITE)
        self.window.blit(self.score_txt, (20, 40))
        

    def run(self):        
        while True:
            self.clock.tick(FPS)
            self.window.fill(BLACK)
            self.draw_rects()
            self.draw_entities()
            self.draw_coins()
            self.draw_score()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()
            self.player.update(self.rects)
            self.coin_collision()
            self.manage_shift_vel()
            self.world_scroll_horizontal()
            self.world_scroll_vertical()
            
            

game = Game()
game.run()
