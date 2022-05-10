#Imports
import pygame
import os
import random
import tkinter
import time

#Screengrösse erkennen
root = tkinter.Tk()
width = root.winfo_screenwidth()   
height = root.winfo_screenheight() 
Pixel = width * height            
if height < 1200:
    scrolldown = round((height-1200)/2)
else:
    scrolldown = 0 

#Globale konstante Variablen
width1  = int(width/7)
height1 = int(height/2.4486)
On = True   
FPS = 60
hp = 1
WEISS   = ( 255, 255, 255)
Score = 0
xS = 0
xS -= 20
xR = -12
i = 0
rScore = 0
xObstacle = 0
spawn = False
l = 1
a = 1
h = 1
u = 1

#Setup
pygame.init()
Display = pygame.display.set_mode((width,height))   
pygame.display.set_caption('SuperMorio')
clock = pygame.time.Clock()                          
file = os.path.join('Desktop', 'Death1.mp3')
file1 = os.path.join('Desktop', 'coconut.mp3')
pygame.init()
pygame.mixer.init()

#Bilder
Hintergrund = pygame.image.load(os.path.join('Desktop','bg.jpg')).convert() 
Hintergrund.scroll(0, 0)
Hintergrund = pygame.transform.scale(Hintergrund, (width,height))
Font = pygame.font.SysFont('timesnewroman',  30)
img = pygame.image.load(os.path.join('Desktop', 'player1.png')).convert()    
img = pygame.transform.scale(img, (196/1920*width,400/1200*height))
img1 = pygame.image.load(os.path.join('Desktop', 'player_jumping1.png')).convert()   
img1 = pygame.transform.scale(img1, (196/1920*width,400/1200*height))
img2 =  pygame.image.load(os.path.join('Desktop', 'fiat_multipla.png')).convert()   
img2 = pygame.transform.scale(img2, (100/1920*width,100/1200*height))
img3 = pygame.image.load(os.path.join('Desktop', 'plane.png')).convert()   
img3 = pygame.transform.scale(img3, (100/1920*width,100/1200*height))
img4 =  pygame.image.load(os.path.join('Desktop', 'heart.png')).convert()   
img4 = pygame.transform.scale(img4, (100/1920*width,100/1200*height))
img5 = pygame.image.load(os.path.join('Desktop', 'empty.png')).convert()   
img5 = pygame.transform.scale(img5, (100/1920*width,100/1200*height))
img6 = pygame.image.load(os.path.join('Desktop', 'player_ducking.png')).convert()   
img6 = pygame.transform.scale(img6, (196/1920*width,295/1200*height))
img.set_colorkey(WEISS) 
img1.set_colorkey(WEISS)
img2.set_colorkey(WEISS)
img3.set_colorkey(WEISS)
img4.set_colorkey(WEISS)
img5.set_colorkey(WEISS)
img6.set_colorkey(WEISS)

#Klassen
class Sprites(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

class obstacles(Sprites):
    def __init__(self):
        Sprites.__init__(self)
        self.images = []
        self.images.append(img2)
        self.images.append(img3)
        self.images.append(img5)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height1 + ((400/1200*height)-(100/1200*height))
        self.image = self.images[0]
        self.hitbox = pygame.Rect(0,0,0,0)
        self.pop = 0
        self.r = 0
        self.ry = 0
   
    def update(self):
        Display.blit(self.image, self.rect)
        self.rect.x = xS % Hintergrund.get_rect().width        
        if self.rect.x > self.pop:
            self.rect.y = height1 + ((400/1200*height)-(100/1200*height))
            self.r = random.randint(0,9)
        if self.r == 0:
            self.image = self.images[0]
            self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 100/1920*width,100/1200*height) #Hitbox

        elif self.r == 1:
            self.rect.y = height1
            self.image = self.images[1]
            self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 100/1920*width,100/1200*height) #Hitbox
        else:
            self.image = self.images[2]
            self.hitbox = (0,0,0,0)
        self.pop = self.rect.x

class Heart(Sprites):
    def __init__(self):
        Sprites.__init__(self)
        self.images = []
        self.images.append(img4)
        self.images.append(img5)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height1
        self.image = self.images[0]
        self.hitbox = pygame.Rect(0,0,0,0)
        self.pop = 0
        self.r = 0
   
    def update(self):
        Display.blit(self.image, self.rect)
        self.rect.x = xS % Hintergrund.get_rect().width  
        if self.rect.x > self.pop:
            self.r = random.randint(0,49)
        if self.r == 0:
            self.image = self.images[0]
            self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 100/1920*width,100/1200*height) 
        else:
            self.image = self.images[1]
            self.hitbox = (0,0,0,0)
        self.pop = self.rect.x

class Player(Sprites):
    def __init__(self):
        Sprites.__init__(self)
        self.images = []
        self.images.append(img)
        self.images.append(img1)
        self.images.append(img6)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = width1   
        self.rect.y = height1   
        self.down = True
        self.up = False
        self.duck = False
        self.hitbox = pygame.Rect(0,0,0,0)
        self.hp = hp

    def update(self):
        Display.blit(self.image, self.rect)
        self.hitbox = pygame.Rect(self.rect.x,self.rect.y,196/1920*width,400/1200*height) 
        if self.rect.y == height1:
            self.down = True
        else:
            self.down = False
        if self.up == True:
            self.rect.y -= 20
        else: 
            self.rect.y += 15
        
        if self.rect.y >= height1:
            self.rect.y = height1
        
        if self.rect.y == height1 - 400: 
            self.up = False
        
        if self.rect.y != height1:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        if self.duck:
            self.image = self.images[2]
            self.hitbox = pygame.Rect(self.rect.x,self.rect.y+90,196/1920*width,295/1200*height)#(400-295)*(295/1200*height)
            self.rect.y = height1 + 90 
        
#Spawning
player = Player()
heart = Heart()
obstacle = obstacles()
sprites = pygame.sprite.Group()
sprites.add(player,obstacle)
pygame.mixer.music.load(file1)
pygame.mixer.music.play(-1)

#Gameloop
while On:
    
    Score1 = Font.render("Score: " + str(rScore), False, WEISS)
    move_x = xS % Hintergrund.get_rect().width 
    Display.blit(Hintergrund, (move_x - Hintergrund.get_rect().width ,0)) 
    Score = Score - xS/1000000
    rScore = round(Score)
    i = (i + 1)
    xS = -(abs(xS) + pow(i * 4, 0.35)/1.05)
    if xS < 10:
        xS -= 10

    if move_x < Pixel:
        Display.blit(Hintergrund, (move_x, 0))
        sprites.draw(Display)
        #pygame.draw.rect(Display, (255,0,0), player.hitbox,2)
        #pygame.draw.rect(Display, (0,0,255), obstacle.hitbox,2)
        #pygame.draw.rect(Display, (0,255,0), heart.hitbox,2)
                                                            
    if l != a and player.hitbox.colliderect(obstacle.hitbox) != True:
        a = 0
        l = 0   
        player.hp = player.hp - 1

    if u != h and player.hitbox.colliderect(heart.hitbox) != True:
        u = 0
        h = 0   
        if player.hp >= 3:
            player.hp = 3
        else:
            player.hp = player.hp + 1   

    if player.hitbox.colliderect(obstacle.hitbox):
        a = l
        l = l - 1
    
    if player.hitbox.colliderect(heart.hitbox):
        h = u
        u = u - 1
    
    if player.hp == 0:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(1)
            time.sleep(2)
            print("Score: ", rScore)   
            On = False
            pygame.quit
            quit() 
    
    for event in pygame.event.get():
              
        if event.type == pygame.KEYDOWN:
            if event.key == ord('w') and player.down == True:
                player.up = True
                player.down = False
            if event.key == ord('s') and player.down == True:
                player.duck = True
            if event.key == ord('o'):                                      
                On = False    
                pygame.quit
                quit()
            
        if event.type == pygame.KEYUP:
            if event.key == ord('s'):
                player.duck = False 
          
    player.update()
    heart.update()
    obstacle.update()
    clock.tick(FPS)
    Display.blit(Score1, (width/1.15, height/12))                            
    pygame.display.update()
