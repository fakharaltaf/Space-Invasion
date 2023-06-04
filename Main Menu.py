import pygame
import time
import random

# initialising system fonts in pygame
pygame.font.init()
font = pygame.font.SysFont("Aharoni", 30)

# Screen Configurations:
WIDTH, HEIGHT = 1000, 666
pygame.display.set_caption("Space Adventure")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Loading Images:
BG = pygame.image.load("Images\Background-black .png")

clock = pygame.time.Clock()

def main():

    elapsed_time = 0
    run = True
    def draw():
        
        screen.blit(BG, (0,0))

        # displaying time:
        display_time = font.render(f"Time: {round(elapsed_time)} seconds", 1,"white")
        
        screen.blit(display_time, (10,10))
        # Updates display
        pygame.display.update()

    while run:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        # Check for window close:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
                break
        if keys[pygame.K_a]:
            print("Start Game")
        draw()

if __name__ == "__main__":
    main()