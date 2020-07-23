import pygame, random

FPS = 20
PAUSE = 0
GAME_OVER = 0
RES = (500, 500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYBER = (255, 211, 0)
WIDTH = 25
HEIGHT = 25
POSITIONS = [(x, y) for x in range(0, RES[0]) for y in range(0, RES[1]) if x % WIDTH == 0 and y % HEIGHT == 0]
DIRECTIONS = [(0, -1),    # Up
              (0, 1),     # Down
              (1, 0),     # Right
              (-1, 0)]    # Left

class GameManager:
    def __init__(self):
        pygame.init()
        self.score = 0
        self.end_game = False
        self.font = pygame.font.Font(None, 20)
        self.font2 = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()
        self.clock_state = FPS
        self.window = pygame.display.set_mode(RES)
        self.entity_dic = {}
        self.p = Player("snake", RES[0] / 2, RES[1] / 2, WIDTH, HEIGHT, WHITE)
        self.t = Target("target", random.choice(POSITIONS)[0], random.choice(POSITIONS)[1], WIDTH, HEIGHT, WHITE)
        self.window.convert()
        pygame.display.set_caption("Snake")

    def pause_game(self):
        if self.clock_state == FPS:
            self.clock_state = PAUSE
        elif self.clock_state == PAUSE:
            self.clock_state = FPS
    
    def get_score(self):
        self.score_txt = self.font.render("Score: " + str(self.score), 0, WHITE)
        return self.score_txt
        
    def show_pause_message(self):
        self.pause_msg = self.font2.render("Game Paused", 0, CYBER)
        return self.pause_msg
        
    def game_over(self):
        self.clock_state = GAME_OVER
        self.game_over_msg = self.font2.render("GAME OVER", 0, CYBER)
        self.window.blit(self.game_over_msg, (RES[0] / 2 - 70, RES[1] / 2))
        
    def reset(self):
        self.clock_state = FPS
        self.end_game = False
        self.score = 0
        self.p.body = []
        self.p.current_dir = random.choice(DIRECTIONS)
        self.p.rect.x = random.choice(POSITIONS)[0]
        self.p.rect.y = random.choice(POSITIONS)[1]
        self.t.rect.x = random.choice(POSITIONS)[0]
        self.t.rect.y = random.choice(POSITIONS)[1]
        
    def check_collisions(self):
        if (self.t.rect.x == self.p.rect.x and self.t.rect.y == self.p.rect.y):
            self.t.rect.x = random.choice(POSITIONS)[0]
            self.t.rect.y = random.choice(POSITIONS)[1]
            self.p.expand()
            self.score += 1
             
    
    def run(self):
        while True:
            self.clock.tick(self.clock_state)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN and self.end_game == True:
                    self.reset()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_t:
                    self.pause_game()
                elif e.type == pygame.KEYDOWN:
                    self.p.change_direction(e.key)
                
            self.window.fill(BLACK)
            self.p.draw(self.window)
            self.t.draw(self.window)
            self.window.blit(self.get_score(), (0, 0))
            if self.clock_state != PAUSE:
                self.p.move()
            if self.clock_state == PAUSE and self.end_game != True:
                self.window.blit(self.show_pause_message(), (RES[0] / 2 - 70, RES[1] / 2))
            self.p.check_position()
            self.check_collisions()
            if self.p.check_collision_w_body():                
                self.end_game = True
                self.game_over()
            pygame.display.update()
                    
    
class GameObject:
    def __init__(self, name, x, y, w, h, color):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        
    def draw(self, context):
        pass
        
    def move(self):
        pass
        
    
class Player(GameObject):
    def __init__(self, name, x, y, w, h, color):
        GameObject.__init__(self, name, x, y, w, h, color)
        self.current_dir = random.choice(DIRECTIONS)
        self.body = []
        self.tail = None
        self.newpos_x = None
        self.newpos_y = None
        self.oldpos_x = None
        self.oldpos_y = None
        
    def check_position(self):
        if self.rect.x > RES[0]:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = RES[0] - self.w
        elif self.rect.y > RES[1]:
            self.rect.y = 0
        elif self.rect.y < 0:
            self.rect.y = RES[1] - self.h
            
    def expand(self):
        if len(self.body) == 0:
            self.body.append(pygame.Rect(self.rect.x - (self.current_dir[0] * self.w),self.rect.y - (self.current_dir[1] * self.h), self.w, self.h))
            self.tail = self.body[0]
        else:
            self.body.append(pygame.Rect(self.tail.x - (self.current_dir[0] * self.w),self.tail.y - (self.current_dir[1] * self.h), self.w, self.h))
            self.tail = self.body[-1]
            
    def draw(self, context):
        pygame.draw.rect(context, self.color, self.rect)
        if len(self.body) > 0:
            self.draw_body(context)
            
    def draw_body(self, context):
        for b in self.body:
            pygame.draw.rect(context, self.color, b)
            
    def move(self):
        self.newpos_x = self.rect.x
        self.newpos_y = self.rect.y
        self.rect.x += self.current_dir[0] * self.w
        self.rect.y += self.current_dir[1] * self.h
        if len(self.body) > 0:
            for i in self.body:
                self.oldpos_x = i.x
                self.oldpos_y = i.y
                i.x = self.newpos_x
                i.y = self.newpos_y
                self.newpos_x = self.oldpos_x
                self.newpos_y = self.oldpos_y
            
        
    def change_direction(self, k):
        if k == pygame.K_UP and self.current_dir != DIRECTIONS[1]:
            self.current_dir = DIRECTIONS[0]
        elif k == pygame.K_DOWN and self.current_dir != DIRECTIONS[0]:
            self.current_dir = DIRECTIONS[1]
        elif k == pygame.K_RIGHT and self.current_dir != DIRECTIONS[3]:
            self.current_dir = DIRECTIONS[2]
        elif k == pygame.K_LEFT and self.current_dir != DIRECTIONS[2]:
            self.current_dir = DIRECTIONS[3]
            
    def check_collision_w_body(self):
       for i in self.body:
           if self.rect.x == i.x and self.rect.y == i.y:
               return True
       return False

        
    
class Target(GameObject):
    def __init__(self, name, x, y, w, h, color):
        GameObject.__init__(self,name, x, y, w, h, color)
        
    def draw(self, context):
        pygame.draw.rect(context, self.color, self.rect)
        
        
    
    
game = GameManager()
game.run()




