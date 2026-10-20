import pygame
import sys
from constants import *

def main():
    # Инициализация Pygame
    pygame.init()
    
    # Создание игрового окна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sound Spy - Lab 1")
    
    # Контроллер кадров
    clock = pygame.time.Clock()
    
    # Главный игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Очистка и отрисовка
        screen.fill(GRAY)
        
        # Текст для проверки
        font = pygame.font.SysFont(None, 36)
        text = font.render("Lab 1: Sound Spy Environment Initialized", True, WHITE)
        screen.blit(text, (50, 50))
        
        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
