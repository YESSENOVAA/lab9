import datetime
import pygame
import datetime
import time
from time import strftime
from random import randint, randrange

pygame.init()

WIDTH, HEIGHT = 300, 400
FPS = 10
cell = 20

bg= pygame.image.load('background.jpg')
pygame.mixer.music.load('sieben tage lang.mp3')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (221,160,221)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
pygame.mixer.music.play(-1)
finished = False
clock = pygame.time.Clock()

class Food:
    def init(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, cell, cell)) 
    def redraw(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)        
class FoodS:
    def init(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)
    def draw(self):
        pygame.draw.rect(screen, (123, 189, 0), (self.x, self.y, cell, cell)) 
    def redraw(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)

class Wall:
    def init(self, x, y):
        self.x, self.y = x, y
    
    def load_wall(self, level=1):
        with open(f'level{level}.txt', 'r') as f:
            f = f.readlines()

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, cell, cell))

class Snake:
    def init(self):
        self.score=0
        self.speed = cell
        self.body = [[0, 0]]
        self.dx = self.speed
        self.dy = 0
        self.destination = ''
        self.color = GREEN
    
    def move(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.destination != 'right':
                    self.dx = -self.speed
                    self.dy = 0
                    self.destination = 'left'
                if event.key == pygame.K_RIGHT and self.destination != 'left':
                    self.dx = self.speed
                    self.dy = 0
                    self.destination = 'right'
                if event.key == pygame.K_UP and self.destination != 'down':
                    self.dx = 0
                    self.dy = -self.speed
                    self.destination = 'up'
                if event.key == pygame.K_DOWN and self.destination != 'up':
                    self.dx = 0
                    self.dy = self.speed
                    self.destination = 'down'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                 
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]

        self.body[0][0] += self.dx
        self.body[0][1] += self.dy
        # бір жақтан кіріп басқа жақтан кіру үшін
        self.body[0][0] %= WIDTH
        self.body[0][1] %= HEIGHT

    def draw(self):
        for block in self.body:
            pygame.draw.rect(screen, self.color, (block[0], block[1], cell, cell))
    
    def collide_food(self, f:Food):
        if self.body[0][0] == f.x and self.body[0][1] == f.y:
            self.score+=1       
            self.body.append([8000,8000])
            return 1
        return 0
    def collide_foodS(self, f:FoodS):
        if self.body[0][0] == f.x and self.body[0][1] == f.y:
            self.score+= 5       
            self.body.append([5000, 5000])
            return 1
        return 0
       
    def collide_self(self):
        global finished
        if self.body[0] in self.body[1:]:
            finished = True

    def check_food(self, f:Food):
        if [f.x, f.y] in self.body:
            f.redraw()
    
    def check_foodS(self, f:FoodS):
        if [f.x, f.y] in self.body:
            f.redraw()
    

text = pygame.font.SysFont('arial', 36)

s = Snake()
f = Food()
sf=FoodS()
score = 1
score1=-1

SCORE= 0
level = 0

while not finished:

    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            finished = True
     
    # клетки для передвижения, чтобы было легко
    # for i in range(0, WIDTH, cell):
    #     for j in range(0, HEIGHT, cell):
    #      pygame.draw.rect(screen, BLACK, (i, j, cell, cell), 1)

    screen.blit(bg, (0,0))
    f.draw()
    
    s.draw()
    s.move(events)
    score += s.collide_food(f)
    score1 += (s.collide_foodS(sf)*8)
    SCORE= score+score1
    s.collide_self()
    s.check_food(f)
    s.check_foodS(sf)
    # score counting
    x = datetime.datetime.now()
    second= x.strftime('%S')
    second=int(second)
    walls_coor = open(f'level{0}.txt', 'r').readlines()
    walls = []
    walls_coor1 = open(f'level{1}.txt', 'r').readlines()
    walls1=[]
    for i, line in enumerate(walls_coor1):
        for j, each in enumerate(line):
            if each == "#":
                walls1.append(Wall(j * cell, i * cell))
        if SCORE%6==0 and SCORE!=0:
            sf.draw()
    for wall1 in walls1:
        
        if sf.x == wall1.x and sf.y == wall1.y:
             sf.redraw()
        if SCORE >= 15:
            wall1.draw()
            if f.x == wall1.x and f.y == wall1.y:
             f.redraw()
            
            if s.body[0][0] == wall1.x and s.body[0][1] == wall1.y:
              finished = True
              

    font= pygame.font.Font(None, 30)
    text1= font.render(f'Score: {SCORE}', True, pygame.Color('Orange') )
    screen.blit(text1, (0, 0))
    pygame.display.update()
    pygame.display.flip()
pygame.quit()