import pygame
import time
import random

# Screen Configurations:
WIDTH, HEIGHT = 1000, 666
pygame.display.set_caption("Space Adventure")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# initialising system fonts in pygame
pygame.font.init()
font = pygame.font.SysFont("Aharoni", 30)
font1 = pygame.font.SysFont("Aharoni", 80)
# Loading Images:
BG = pygame.image.load("Images\Background-black.png")
Rocket = pygame.image.load("Images\Rocket.png")
Enemy_ship = pygame.image.load("Images\enemy-ship.png")
Laser_img = pygame.image.load("Images\laser.png")
clock = pygame.time.Clock()



# Classes
class ship():
    max_cooldown = 60
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship = None
        self.laser = Laser_img
        self.lasers = []
        self.cooldowntimer = 60
    def cooldown(self):
        if self.cooldowntimer >= ship.max_cooldown:
            self.cooldowntimer = 0
        elif self.cooldowntimer > 0:
            self.cooldowntimer += 1

    def draw(self):
        screen.blit(self.ship, (self.x, self.y))
        for laser in self.lasers:
            laser.draw()

    def runlasers(self,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.offscreen():
                self.lasers.remove(laser)
            elif laser.collide(obj):
                self.lasers.remove(laser)
                obj.health -= 10
    def getheight(self):
        return self.ship.get_height()
    def getwidth(self):
        return self.ship.get_width()
    def shoot(self):
        if self.cooldowntimer == 0:
            laser = Laser(self.x + Laser_img.get_width(), self.y, 10)
            self.lasers.append(laser)
            self.cooldowntimer = 2

class Player(ship):
    def __init__(self,x, y , health = 100):
        super().__init__(x, y, health)
        self.ship = Rocket
        self.laser = Laser_img
        self.max_health = health
        self.speed = 5 
        self.mask = pygame.mask.from_surface(self.ship)
    def runlasers(self,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.offscreen():
                self.lasers.remove(laser)
            for obj in objs:
                if laser.collide(obj):   
                    objs.remove(obj)
                    self.lasers.remove(laser)
                    obj.health -= 10
class Enemy(ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship = Enemy_ship
        self.laser = Laser_img
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.ship)
    def move(self):
        self.y += self.speed

class Laser:
    def __init__(self,x,y, speed):
        self.x = x
        self.y = y
        self.speed = -speed
        self.img = Laser_img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
    def move(self):
        self.y += self.speed
    def collide(self,obj1):
        return collision(obj1, self)
    def offscreen(self):
        return not(self.y <= HEIGHT and self.y >= 0)
    def move(self):
        self.y += self.speed


def collision(obj1, obj2):
    xoffset = obj2.x - obj1.x
    yoffset = obj2.y - obj2.x
    return obj1.mask.overlap(obj2.mask, (xoffset,yoffset)) != None

# Main Driver Code Function
def main():

    # Initializing Variables
    start_time = time.time()
    elapsed_time = 0
    player_lives = 10
    player_level = 0
    enemies_on_screen = []
    enemy_wave = 10
    player = Player(500,333)
    gameover = False
    lost_timer = 0
    
    # Creating Enemies Objects
    for i in range(enemy_wave):
        enemies_on_screen.append(Enemy(random.randrange(0,900),random.randrange(-5000*((player_level+1)/5),0)))
    
            

    # Function for Drawing images on screen
    def draw():
        
        # Drawing Background
        screen.blit(BG, (0,0))
        
        # Drawing ships on screen
        for enemy in enemies_on_screen:
            enemy.draw()
        player.draw()
        
        # Initializing Stats:
        display_time = font.render(f"Time: {round(elapsed_time)} seconds", 1,"white")
        display_lives = font.render(f"Lives: {player_lives}", 1, "red")
        display_level = font.render(f"Level: {player_level}", 1, "white")
        
        # Displaying Stats:
        screen.blit(display_level,(900,10))
        screen.blit(display_lives,(10,10))
        screen.blit(display_time, (10,HEIGHT-30))
        
        # Game over message
        if gameover == True:
            lost = font1.render("You Lost HAHAHAHAH", 1, "yellow")
            screen.blit(lost,(WIDTH/2 - lost.get_width()/2 ,333))
        
        # Updates display
        pygame.display.update()
     
    # Main Loop
    run = True
    while run:
        
        clock.tick(60)
        elapsed_time = time.time() - start_time
        
        # Checks if the tab is closed 
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
                break

        
        # Losing Message Timer thingy
        if gameover == True:
            lost_timer += 1
            if lost_timer >= 60 * 5:
                break
            else:
                continue
        
        
        
        # Gets keys pressed in an instance
        keys = pygame.key.get_pressed()
        
        
        # Controls:
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x  >= 0:
            player.x -= player.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player.getwidth() <= WIDTH :
            player.x += player.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y >= 0:
            player.y -= player.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player.getheight() <= HEIGHT:
            player.y += player.speed
        if (keys[pygame.K_SPACE]):
            player.shoot()
        # Level Up
        if len(enemies_on_screen) <= 0:
            player_level += 1
            enemy_wave += 5
        
        # Game Over
        if player_lives <= 0 or player.health <= 0:
            gameover = True
        
        # Moving player lasers    
        player.runlasers(enemies_on_screen) 
        
        # Moving Enemies
        for enemy in enemies_on_screen:
            enemy.move()
            enemy.runlasers(player)
   
            # Deleting enemies that have left the screen
            # Lives count Fucntionality
            if enemy.y + enemy.getheight() >= HEIGHT:
                player_lives -= 1
                player.health -= 5
                enemies_on_screen.remove(enemy)
        
                

        draw()
    pygame.quit()


# Main driver code function call
if __name__ == "__main__":
    main()