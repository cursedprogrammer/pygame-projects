import random
import pygame

CAPTION = "Breakout"
RES = (500, 500)
STATES = (True, False)
SPEED = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLOCK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
FPS = 30
PAUSE = 0

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(30)
        self.game_area = pygame.Rect(RES[0] / 100, RES[1] / 100, 350, RES[1] - (RES[1] / 50))
        pygame.display.set_caption(CAPTION)
        self.p = Player(self.game_area.midbottom[0], self.game_area.midbottom[1] - 40, 50, 15, WHITE)
        self.b = Ball(self.game_area.center[0], self.game_area.center[1], 10, 10, WHITE)
        self.block_list = []

    def draw_ui(self):
        pygame.draw.rect(self.window, WHITE, self.game_area, 1)
        
    def draw_entities(self):
        pygame.draw.rect(self.window, WHITE, self.p.rect)
        pygame.draw.rect(self.window, WHITE, self.b.rect)
        for block in self.block_list:
            pygame.draw.rect(self.window, block.color, block.rect)
        
    def generate_blocks(self, w, h, rows):
        self.x_pos = self.game_area.left
        self.y_pos = self.game_area.top
        for i in range(rows):            
            for j in range(self.x_pos, self.game_area.right, w):
                if random.choice(STATES) == True:
                    self.block_list.append(Block(self.x_pos, self.y_pos, w, h, random.choice(BLOCK_COLORS)))
                self.x_pos += w
            self.y_pos += h
            self.x_pos = self.game_area.left

    def player_collisions(self):
        if self.p.rect.right > self.game_area.right:
            self.p.rect.right = self.game_area.right
        elif self.p.rect.left < self.game_area.left:
            self.p.rect.left = self.game_area.left
            
    def respawn(self):
        self.b.rect.x = self.game_area.center[0]
        self.b.rect.y = self.game_area.center[1]
            
    def ball_collisions(self):
        if self.b.rect.right >= self.game_area.right:
            self.b.x_vel *= -1
        elif self.b.rect.left <= self.game_area.left:
            self.b.x_vel *= -1
        elif self.b.rect.top <= self.game_area.top:
            self.b.y_vel *= -1
        elif self.b.rect.bottom >= self.game_area.bottom:
            self.respawn()
        elif self.b.rect.colliderect(self.p.rect):
            self.b.y_vel *= -1
        else:
            if self.b.rect.collidelist(self.block_list) != -1:
                self.col_rect = self.block_list[self.b.rect.collidelist(self.block_list)].rect
                if self.b.rect.top >= self.col_rect.bottom:
                    self.b.y_vel *= -1
                elif self.b.rect.y >= self.col_rect.top and self.b.rect.y <= self.col_rect.bottom:
                    self.b.x_vel *= -1
                elif self.b.rect.bottom <= self.col_rect.top:
                    self.b.y_vel *= -1
                del self.block_list[self.b.rect.collidelist(self.block_list)]

    def run(self):
        print(self.game_area.width)
        print(self.game_area.height)
        self.generate_blocks(50, 20, 5)
        while True:
            self.clock.tick(FPS)
            self.window.fill(BLACK)
            self.draw_ui()
            self.draw_entities()
            self.b.move()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT:
                        self.p.move('r')
                    elif e.key == pygame.K_LEFT:
                        self.p.move('l')
            self.player_collisions()
            self.ball_collisions()
            if len(self.block_list) == 0:
                self.respawn()
                self.generate_blocks(50, 20, 5)
            pygame.display.update()
                    

class GameObject:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
    
class Player(GameObject):
    def __init__(self, x, y, w, h, color):
        GameObject.__init__(self, x, y, w, h, color)
        
    def move(self, dir):
        if dir == 'r':
            self.rect.x += SPEED
        elif dir == 'l':
            self.rect.x -= SPEED
            
    
class Ball(GameObject):
    def __init__(self, x, y, w, h, color):
        GameObject.__init__(self, x, y, w, h, color)
        self.x_vel = random.choice([-1, 1])
        self.y_vel = random.choice([-1, 1])
        
    def move(self):
        self.rect.x += self.x_vel * SPEED
        self.rect.y += self.y_vel * SPEED
    
    
class Block:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

game = Game()
game.run()