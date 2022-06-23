import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Asteroids')
rocket = pygame.image.load('z.png')
pygame.display.set_icon(rocket)
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)

class Asteroid:
    def __init__(self,id):
        self.radius = random.randint(15,50)
        self.x = random.randint(0,display_width)
        self.y = 0 - self.radius
        self.velocity_x = random.randint(-3,3)
        self.velocity_y = random.randint(1,4)
        self.id = id
    def display(self):
        pygame.draw.circle(screen,white,(self.x,self.y),self.radius,2)
    def move(self):
        self.y += self.velocity_y
        self.x += self.velocity_x
        if(self.y - 100 > display_height):
            self.__init__(self.id)
    def intersects(self,x,y):
        o_player = (x+30),(y+30)
        if abs(self.x-o_player[0])<self.radius and abs(self.y-o_player[1])<self.radius:
            return True
        return False

class Player:
    def __init__(self):
        self.x = display_width/2
        self.y = display_height/2
        self.velocity_x = 0
        self.velocity_y = 0
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.x < -60:
            self.x = display_width
        elif self.x > display_width:
            self.x = -60
        if self.y < 0:
            self.y = 0
        elif self.y > display_height-60:
            self.y = display_height-60
    def display(self):
        screen.blit(rocket,(self.x,self.y))


def msg(fontsize,text,x,y):
    font = pygame.font.Font('freesansbold.ttf',fontsize)
    textSurf= font.render(text,True,white) 
    textRect = textSurf.get_rect()
    textRect.center = (x,y)
    screen.blit(textSurf,textRect)
    pygame.display.update()

def game_over(level):
    msg(60,"Game over",display_width/2,display_height/2)
    msg(40,"Score: " + str(level),display_width/2,display_height/2 + 60)
    time.sleep(2)

def points(level):
    msg(40,"Score: " + str(level),700,40)

def game_loop():

    level = 0
    player = Player()
    asteroids = []
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
                    player.velocity_x = -4
                if event.key == pygame.K_d:
                    player.velocity_x = 4
                if event.key == pygame.K_w:
                    player.velocity_y = -4
                if event.key == pygame.K_s:
                    player.velocity_y = 4

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.velocity_x = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity_y = 0

        timer+=1
        if timer%100==0:
            if level < 40:
                level += 1
        if timer%(41 - level)==0:
            a = Asteroid(id)
            id+=1
            asteroids.append(a)

        screen.fill(black)

        player.move()
        player.display()

        for a in asteroids:
            a.move()
            a.display()
            if(a.intersects(player.x,player.y)):
                game_over(level)
                game_exit=True
                game_restart=True
        points(level)
        pygame.display.update()
        clock.tick(60)

game_restart = True
while(game_restart):
    game_loop()
pygame.quit()
quit()