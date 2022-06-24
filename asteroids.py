import pygame
import time
import random
import math

pygame.init()

display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Asteroids')
rocket = pygame.image.load('rocket.png')
pygame.display.set_icon(rocket)
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)

class Object:
   # def __init__(self):
   #     self.rect
   #     self.velocity
   #     self.angle
   #     self.radius
    def move(self):
        velocity_x = self.velocity * math.sin(math.radians(self.angle))
        velocity_y = self.velocity * math.cos(math.radians(self.angle))
        self.rect=self.rect.move(velocity_x,velocity_y)
    def intersects(self,obj):
        if (self.rect.x-obj.rect.centerx)**2 + (self.rect.y-obj.rect.centery)**2 < self.radius**2:
            return True
        return False
    def out(self):
        if self.rect.x < -100 or self.rect.x > display_width or self.rect.y < -100 or self.rect.y > display_height:
            return True
        return False

class Asteroid(Object):
    def __init__(self):
        self.radius = random.randint(15,50)
        x = random.randint(0,display_width)
        y = 0 - self.radius
        self.rect = pygame.Rect((x, y), (self.radius, self.radius))
        self.velocity = random.randint(1,4)
        self.angle = random.randint(-45,45)
    def display(self):
        pygame.draw.circle(screen,white,(self.rect.x,self.rect.y),self.radius,2)
    def move(self):
        Object.move(self)
        if(self.rect.y - 100 > display_height):
            self.__init__()

class Player(Object):
    def __init__(self):
        self.original_img = rocket
        self.img = rocket
        self.rect = self.img.get_rect(topleft=(display_width/2,display_height/2))
        self.velocity = 0
        self.rotation = 0
        self.angle = 0
    def move(self):
        Object.move(self)
        self.rotate()
        if self.rect.x < -60:
            self.rect.x = display_width
        elif self.rect.x > display_width:
            self.rect.x = -60
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > display_height-60:
            self.rect.y = display_height-60      
    def rotate(self):
        self.angle += self.rotation
        self.img = pygame.transform.rotate(self.original_img,self.angle)
        self.rect = self.img.get_rect(center=self.rect.center)
    def display(self):
        screen.blit(self.img,self.rect)

class Bullet(Object):
    def __init__(self,player):
        self.rect = pygame.Rect((player.rect.centerx, player.rect.centery), (5, 5))
        self.angle = player.angle
        self.velocity = -10
    def display(self):
        pygame.draw.circle(screen,white,(self.rect.x,self.rect.y),5,20)

def msg(fontsize,text,x,y):
    font = pygame.font.Font('freesansbold.ttf',fontsize)
    textSurf= font.render(text,True,white) 
    textRect = textSurf.get_rect()
    textRect.center = (x,y)
    screen.blit(textSurf,textRect)
    pygame.display.update()

def game_over(score):
    msg(60,"Game over",display_width/2,display_height/2)
    msg(40,"Score: " + str(score),display_width/2,display_height/2 + 60)
    time.sleep(2)

def points(score):
    msg(40,"Score: " + str(score),675,40)

def game_loop():

    level = 0
    asteroids_destroyed = 0
    player = Player()
    asteroids = []
    bullets = []
    bullets_left=[]
    id=0
    timer=0
    game_exit = False
    global game_restart
    game_restart = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                game_restart = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.rotation = 4
                if event.key == pygame.K_d:
                    player.rotation = -4
                if event.key == pygame.K_w:
                    player.velocity = -5
                if event.key == pygame.K_s:
                    player.velocity = 3
                if event.key == pygame.K_SPACE and len(bullets)<5:
                    new_bullet = Bullet(player)
                    bullets.append(new_bullet)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.rotation = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity = 0

        timer+=1
        if timer%100==0:
            level += 1
        if level < 40:
            if timer%(41 - level)==0:
                a = Asteroid()
                asteroids.append(a)
        elif len(asteroids) < 300:
            a = Asteroid()
            asteroids.append(a)


        screen.fill(black)

        player.move()
        player.display()

        bullets_left = []
        for b in bullets:
            b.move()
            b.display()
            l = len(asteroids)
            asteroids[:] = [a for a in asteroids if not a.intersects(b)]
            if len(asteroids)==l:
                if not b.out():
                    bullets_left.append(b)
            else:
                asteroids_destroyed  += 1
        bullets = bullets_left


        for a in asteroids:
            a.move()
            a.display()
            if(a.intersects(player)):
                game_over(level+asteroids_destroyed)
                game_exit=True
                game_restart=True
        points(level + asteroids_destroyed)
        pygame.display.update()
        clock.tick(60)

game_restart = True
while(game_restart):
    game_loop()
pygame.quit()
quit()