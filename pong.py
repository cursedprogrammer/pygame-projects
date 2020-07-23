import pygame
import random
from pygame.locals import *
res = (500, 500)
pygame.init()
w = pygame.display.set_mode(res)
pygame.display.set_caption('Pong')
black = (0,0,0)
white = (255,255,255)
directions = (-1, 1)
FPS = 30
PAUSE = 0
clock = pygame.time.Clock()
pygame.key.set_repeat(30)
p1_score = 0
p2_score = 0
blipsound = pygame.mixer.Sound("pongblip.wav")

class Paddle:
    def __init__(self, x, y, width, h, col, cont, upkey, downkey):
        self.x = x
        self.y = y
        self.width = width
        self.h = h
        self.col = col
        self.cont = cont
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.h)
        self.upkey = upkey
        self.downkey = downkey
        
        
    def move(self, k):
        if k == self.upkey:
            self.playerRect.top -= 10
        elif k == self.downkey:
            self.playerRect.top += 10
            
            
    def draw(self):
        pygame.draw.rect(self.cont, self.col, self.playerRect)
        
            
            
class Ball:
    def __init__(self, x, y, width, h, col, cont, vel=7):
        self.x = x
        self.y = y
        self.width = width
        self.h = h
        self.col = col
        self.d = [random.choice(directions), 0]
        self.vel = vel
        self.cont = cont
        self.ballRect = pygame.Rect(self.x, self.y, width, h)
        
    
    def draw(self):
        pygame.draw.rect(self.cont, self.col, self.ballRect)
        
        
    def respawn(self):
        self.ballRect.left = self.x
        self.ballRect.top = self.y
        self.d = [random.choice(directions), 0]
        
        
    def mv_ball(self):
        self.ballRect.left += self.d[0] * self.vel
        self.ballRect.top += self.d[1] * self.vel
        
    def chk_ball(self, col_list):
        global p1_score
        global p2_score
        if self.ballRect.top <= 0:
            self.d[1] *= -1
        elif self.ballRect.top + self.ballRect.h >= res[1]:
            self.d[1] *= -1
        elif self.ballRect.left < 0:
            p2_score += 1
            self.respawn()
        elif self.ballRect.left + self.width > res[0]:
            p1_score += 1
            self.respawn()
        elif self.ballRect.collidelist(col_list) != -1:
            blipsound.play()
            i = self.ballRect.collidelist(col_list)
            if self.ballRect.center[1] >= col_list[i].top and self.ballRect.center[1] <= col_list[i].top + col_list[i].height * (1/3):
                self.d[0] *= -1
                self.d[1] = -1
            elif self.ballRect.center[1] >= col_list[i].top + col_list[i].height * (1/3) and self.ballRect.center[1] <= col_list[i].top + col_list[i].height * (2/3):
                self.d[0] *= -1
                self.d[1] = 0
            elif self.ballRect.center[1] >= col_list[i].top + col_list[i].height * (2/3) and self.ballRect.center[1] <= col_list[i].top + col_list[i].height:
                self.d[0] *= -1
                self.d[1] = 1
            
    

def score(no):
    txt = pygame.font.Font(None, 40)
    test_txt = txt.render(str(no), 0, white)
    return test_txt
    
        
# Initialize game
p1 = Paddle(20, 250, 7.5, 45, white, w, K_w, K_s)
p2 = Paddle(res[0] - 40, 250, 7.5, 45, white, w, K_UP, K_DOWN)
b = Ball(res[0] / 2, res[1] / 2, 7, 7, white, w)
collider_list = [p1.playerRect, p2.playerRect]
def main_loop():
    w.convert()
    players = [p1,p2]
    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
            elif e.type == KEYDOWN and (e.key == p1.upkey or e.key == p1.downkey):
                p1.move(e.key)
            elif e.type == KEYDOWN and (e.key == p2.upkey or e.key == p2.downkey):
                p2.move(e.key)
            
        w.fill(black)
        w.blit(score(p1_score), (100, 30))
        w.blit(score(p2_score), (res[0] - 120, 30))
        for p in players:
            p.draw()
        b.draw()
        b.mv_ball()
        b.chk_ball(collider_list)
        pygame.display.update()
        
        
if __name__ == '__main__':
    main_loop()
    