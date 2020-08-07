import pygame
import time

WHITE         = (255, 255, 255)
RED           = (255, 0, 0)
CLOCK_CENTER  = (250, 250)
DEGREE_X_SEC  = 6
DEGREE_X_HOUR = 30
CLOCK_HAND    = pygame.math.Vector2(0, -80)

def draw_numbers(surf):
    number_font = pygame.font.SysFont("arial", 20)
    numbers = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for n in numbers:
        number_surf = number_font.render(str(n), True, WHITE)
        surf.blit(number_surf, CLOCK_CENTER + CLOCK_HAND.rotate(DEGREE_X_HOUR * n) - (5, 10))

def main():
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Clock")
    clock_font = pygame.font.SysFont("arial", 50)
    secs_hand = pygame.math.Vector2(0, -80)
    
    
    while True:    
        secs  =  time.localtime()[5]
        mins  =  time.localtime()[4]
        hours =  time.localtime()[3]
        
        secs_hand  =  CLOCK_HAND.rotate(DEGREE_X_SEC * secs)
        mins_hand  =  CLOCK_HAND.rotate(DEGREE_X_SEC * mins)
        hours_hand =  CLOCK_HAND.rotate(DEGREE_X_HOUR * hours)
        
        clock_txt = str(hours) + ":" + str(mins) + ":" + str(secs)
        clock_surf = clock_font.render(clock_txt, True, WHITE, (175, 200))
        window.fill((0, 0, 0))
        window.blit(clock_surf, (350, 400))
        pygame.draw.circle(window, WHITE, CLOCK_CENTER, 100, 1)
        pygame.draw.line(window, RED, CLOCK_CENTER, CLOCK_CENTER + secs_hand, 1)
        pygame.draw.line(window, WHITE, CLOCK_CENTER, (CLOCK_CENTER + mins_hand), 3)
        pygame.draw.line(window, WHITE, CLOCK_CENTER, (CLOCK_CENTER + hours_hand/2), 5)
        draw_numbers(window)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
                
                
main()