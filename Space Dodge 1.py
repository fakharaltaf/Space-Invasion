import pygame
import time
import random

# Screen Configurations:
WIDTH, HEIGHT = 1000, 666
pygame.display.set_caption("Space Adventure")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialising system fonts in pygame
pygame.font.init()
font = pygame.font.SysFont("Aharoni", 30)
font1 = pygame.font.SysFont("Aharoni", 80)

# Random Themes
gamerule = random.randint(1,3)
print(gamerule)
if gamerule == 1:
    # Loading Images:
    BG = pygame.image.load("Images\Background-black.png")
    Rocket = pygame.image.load("Images\Rocket.png")
    Enemy_ship = pygame.image.load("Images\enemy-ship.png")
    Laser_img = pygame.image.load("Images\laser-1.png")
elif gamerule == 2:
    # Loading Images:
    BG = pygame.image.load("Background Objects\Space.png")
    Rocket = pygame.image.load("Background Objects\Cricket.png")
    Enemy_ship = pygame.image.load("Background Objects\Scarab.png")
    Laser_img = pygame.image.load("Images\laser-1.png")
elif gamerule == 3:
    # Loading Images:
    BG = pygame.image.load("Background Objects\Space.png")
    Rocket = pygame.image.load("Background Objects\Cricket.png")
    Enemy_ship = pygame.image.load("Background Objects\Scarab.png")
    Laser_img = pygame.image.load("Images\laser-1.png")

# Loading Audio Files
pygame.mixer.init()
BGS = pygame.mixer.Sound("Media\Heavenly Music - Sound Effect (HD).mp3")

i = random.randint(0,3)
if i == 0:
    deathsound = pygame.mixer.Sound("Media\GTA V Wasted_Busted - Gaming Sound Effect (HD).mp3")
elif i == 1:
    deathsound = pygame.mixer.Sound("Media\death sound.mp3")
elif i==2:
    deathsound = pygame.mixer.Sound("Media\Mission Failed - Sound Effect [Perfect Cut].mp3")
elif i == 3:
    deathsound = pygame.mixer.Sound("Media\Fatality - Mortal Kombat Sound Effect (HD).mp3")

j = random.randint(1,2)
if j == 1:
    kill_sound = pygame.mixer.Sound("Media\wow sound effect.mp3")
elif j == 2:
    kill_sound = pygame.mixer.Sound("Media\Wee sound effect.mp3")

Shoot_sound = pygame.mixer.Sound("Media\Shootsound.mp3")

kill_sound.set_volume(0.02)
Shoot_sound.set_volume(0.02) 
BGS.set_volume(0.02)
BGS.play(loops = -1)
deathsound.set_volume(0.02)

clock = pygame.time.Clock()

# Classes
class ship():
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.cooldowntimer = 60
        self.ship = None
        self.laser = Laser_img
        self.lasers = []
    def cooldown(self, cooldown):
        if self.cooldowntimer >= cooldown:
            self.cooldowntimer = 0
        elif self.cooldowntimer > 0:
            self.cooldowntimer += 1

    def draw(self):
        screen.blit(self.ship, (self.x, self.y))
        for laser in self.lasers:
            laser.draw()

    def runlasers(self,obj):
        self.cooldown(45)
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
    def shoot(self, speed):
        if self.cooldowntimer == 0:
            laser = Laser(self.x + Laser_img.get_width()/2, self.y, speed)
            self.lasers.append(laser)
            self.cooldowntimer = 2

class Player(ship):
    def __init__(self,x, y , health):
        super().__init__(x, y, health)
        self.ship = Rocket
        self.laser = Laser_img
        self.speed = 5
        self.current_score = 0
        self.mask = pygame.mask.from_surface(self.ship)
    def runlasers(self,enemies_on_screen):
        self.cooldown(25)
        for laser in self.lasers:
            laser.move()
            if laser.offscreen():
                self.lasers.remove(laser)
            else:
                for obj in enemies_on_screen:
                    if laser.collide(obj):   
                        enemies_on_screen.remove(obj)
                        kill_sound.play()
                        self.current_score += 50
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
class Enemy(ship):
    def __init__(self, x, y, health):
        super().__init__(x, y, health)
        self.ship = Enemy_ship
        self.laser = Laser_img
        self.speed = 0.7
        self.mask = pygame.mask.from_surface(self.ship)
    def move(self):
        self.y += self.speed

class Laser:
    def __init__(self,x,y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.img = Laser_img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
    def collide(self,obj1):
        return collision(self, obj1)
    def offscreen(self):
        return not(self.y <= HEIGHT and self.y >= 0)
    def move(self):
        self.y += self.speed

# Functions:

def collision(obj1, obj2):
    xoffset = obj2.x - obj1.x
    yoffset = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (xoffset,yoffset)) != None

# Menu Driver Code

def menu():
    run = True
    while run:
        
        screen.blit(BG, (0,0))
        welcome = font1.render("Click a Mouse Button to start", 1, "white")
        screen.blit(welcome, (WIDTH/2-welcome.get_width()/2,HEIGHT/2))
        pygame.display.update()
        # Checks if the tab is closed 
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                main()
                

# Main Driver Code Function
def main():

    # Initializing Variables
    start_time = time.time()
    elapsed_time = 0
    player_lives = 8
    player_level = 0
    enemies_on_screen = []
    enemy_wave = 10
    enemy_laser_speed = 4
    player_laser_speed = 12
    player = Player(500,333,100)
    gameover = False
    lost_timer = 0
    
    # Highscore system
    h = open("highscore.txt","r")
    highscore = int(h.read())
    h.close()

    # Function for Drawing images on screen
    def draw():
        
        # Drawing Background
        screen.blit(BG, (0,0))
        
        # Drawing ships on screen
        for enemy in enemies_on_screen:
            enemy.draw()
            if random.randint(1, 150) == 1:
                enemy.shoot(enemy_laser_speed)
        player.draw()
        
        # Initializing Stats:
        display_time = font.render(f"Time: {round(elapsed_time)} seconds", 1,"white")
        display_lives = font.render(f"Lives: {player_lives}", 1, "red")
        display_level = font.render(f"Level: {player_level}", 1, "white")
        display_health = font.render(f"Health: {round(100*(player.health/100))}%", 1, "red")
        display_highscore = font.render(f"High Score: {round(highscore)}", 1, "white")
        display_current_score = font.render(f"Score: {round(player.current_score)}",1 ,"white")
        
        # Displaying Stats:
        screen.blit(display_health,(840,HEIGHT-30))
        screen.blit(display_level,(900,10))
        screen.blit(display_lives,(10,10))
        screen.blit(display_time, (10,HEIGHT-30))
        screen.blit(display_highscore,(10,40))
        screen.blit(display_current_score,(10, HEIGHT - 70))
        
        # Game over message
        if gameover == True:
            deathsound.play()
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
                quit()

        
        # Losing Message Timer thingy
        if gameover == True:
            lost_timer += 1
            if lost_timer >= 60 * 5:
                menu()
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
            player.shoot(-player_laser_speed)
            Shoot_sound.play()
        if keys[pygame.K_ESCAPE]:
            player_lives -= player_lives
        # Level Up
        if len(enemies_on_screen) <= 0:
            
            # Creating Enemies Objects
            for i in range(enemy_wave):
                enemies_on_screen.append(Enemy(random.randrange(0,900),random.randrange(-5000*((player_level+1)/5),0),100))
            player_level += 1
            enemy_wave += 5
            player_lives += 2
            player_laser_speed += 1
            enemy_laser_speed += 1

        # Game Over
        if player_lives <= 0 or player.health <= 0:
            gameover = True
            if player.current_score > highscore:
                h = open("highscore.txt","w")
                h.write(str(player.current_score))
                h.close()
        
        # Moving player lasers    
        player.runlasers(enemies_on_screen) 
        
        # Moving Enemies
        for enemy in enemies_on_screen:
            enemy.move()
            enemy.runlasers(player)
            if collision(enemy, player):
                player.health -= 30
                if enemy in  enemies_on_screen:
                    enemies_on_screen.remove(enemy)
                    kill_sound.play()
                    player.current_score += 20
   
            # Deleting enemies that have left the screen
            # Lives count Fucntionality
            if enemy.y + enemy.getheight() >= HEIGHT:
                player_lives -= 1
                enemies_on_screen.remove(enemy)
        
                

        draw()
    pygame.quit()

# Main driver code function call
if __name__ == "__main__":
    menu()