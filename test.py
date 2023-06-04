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
Rocket = pygame.image.load("Images\Rocket.png")

clock = pygame.time.Clock()
# SpaceShip Variables
player_speed = 10
player_width = 40
player_height = 60
# Asteroid Variables
asteroid_height = 15
asteroid_width = 15
asteroid_speed = 10
# Classes
class ship():
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship = None
        self.laser = None
    def draw(self):
        screen.blit(self.ship, (self.x, self.y))

class Player(ship):
    def __init__(self,x, y , health = 100):
        super().__init__(x, y, health)
        self.ship = Rocket
        self.laser = None
        self.health = health
    def getheight(self):
        return self.ship.get_height()
    def getwidth(self):
        return self.ship.get_width()

# Functions
def draw_text(text,font,textcolor ,x,y):
    img = font.render(text, True, textcolor)
    screen.blit(img, x, y)
# Main Driver Code Function
def main():

    elapsed_time = 0
    run = True
    def draw():
        
        screen.blit(BG, (0,0))

        # displaying time:
        display_time = font.render(f"Time: {round(elapsed_time)} seconds", 1,"white")
        draw_text("Press SPACE to start game",font, "white",160,250)
        screen.blit(display_time, (10,10))
        # Updates display
        pygame.display.update()

    while run:
        keys = pygame.key.get_pressed()
        # Check for window close:
        
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
                break
            if keys[pygame.K_UP]:
                gameplay()
            else:
                draw()

def gameplay():
    start_time = time.time()
    elapsed_time = 0
    run = True
    player = Player(500,333)
    
    # Function for Drawing images on screen
    def redraw():
        screen.blit(BG, (0,0))
        player.draw()
        # displaying time:
        display_time = font.render(f"Time: {round(elapsed_time)} seconds", 1,"white")
        
        screen.blit(display_time, (10,10))
        # Updates display
        pygame.display.update()
    

    # Main Loop
    while run:
        
        clock.tick(60)
        elapsed_time = time.time() - start_time
        # Checks if the tab is closed 
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        
        
        # Controls:

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x  >= 0:
            player.x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player.getwidth() <= WIDTH :
            player.x += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y >= 0:
            player.y -= player_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player.getheight() <= HEIGHT:
            player.y += player_speed

        redraw()
    pygame.quit()


# Main driver code function call
if __name__ == "__main__":
    main()