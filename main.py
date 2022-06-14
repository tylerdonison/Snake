import pygame as p
import random as r
import sys

p.init()

CELL_SIZE = 40
CELL_NUMBER = 18
WIDTH = CELL_NUMBER*CELL_SIZE
HEIGHT = WIDTH

#SPEED will determine difficulty
SPEED = [1,2,3]
#colors:
WHITE =  (255,  255,  255)
BLACK =  (0,    0,    0)
GREEN =  (0,    255,  0) 
BLUE =   (0,    0,    255)
TEAL =   (0,    255,  255)
PURPLE = (255,  0,    255)

WIN = p.display.set_mode((WIDTH, HEIGHT))

FPS = 60
class Fruit():

    def __init__(self):
        self.x = r.randint(1, CELL_NUMBER-1)
        self.y = r.randint(1, CELL_NUMBER-1)
    
    def draw_fruit(self):
        fruit_rect = p.Rect((self.x * CELL_SIZE)+5, (self.y * CELL_SIZE)+5, CELL_SIZE-10, CELL_SIZE-10)
        #WIN.blit(apple, fruit_rect)
        p.draw.rect(WIN, PURPLE, fruit_rect)


    def randomize(self):
        self.__init__()

class Snake():

    def __init__(self):
        self.body = [[5, 10], [6,10], [7,10]]
        self.direction_x = -1
        self.direction_y = 0
        self.last_pos = [8,10]

    def draw_snake(self):
        for block in self.body:
            snek_rect = p.Rect(block[0]*CELL_SIZE, block[1]*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            p.draw.rect(WIN, (BLUE), snek_rect)
    
    def check_wrap(self, head):
        if head[0] < 0:
            head[0] = CELL_NUMBER
        elif head[0] > CELL_NUMBER:
            head[0] = 0
        if head[1] < 0:
            head[1] = CELL_NUMBER
        elif head[1] > CELL_NUMBER:
            head[1] = 0
        return head
    
    def move_snake(self):
        body_copy = self.body[:-1]
        new_head = [body_copy[0][0] + self.direction_x, body_copy[0][1] + self.direction_y]
        new_head = self.check_wrap(new_head)
        body_copy.insert(0, new_head)        
        last_index = len(self.body) - 1
        self.last_pos = self.body[last_index]
        self.body = body_copy[:]
        
    def add_block(self):
        self.body.append(self.last_pos)

class Main():
    def __init__(self):
        self.snek = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snek.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_element(self):
        self.fruit.draw_fruit()
        self.snek.draw_snake()

    def check_collision(self):
        fruit_pos = [self.fruit.x, self.fruit.y]
        if fruit_pos == self.snek.body[0]:
            self.fruit.randomize()
            self.snek.add_block()
        if fruit_pos in self.snek.body:
            self.fruit.randomize()
    
    def check_fail(self):
        for block in self.snek.body[1:]:
            if block == self.snek.body[0]:
                self.game_over()
    
    def game_over(self):
        p.quit()
        sys.exit()

main = Main()
WIN.fill(TEAL)

SCREEN_UPDATE = p.USEREVENT
p.time.set_timer(SCREEN_UPDATE, 200)

while True:
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == p.KEYDOWN:
            if event.key == p.K_UP:
                if main.snek.direction_y != 1:
                    main.snek.direction_y = -1
                    main.snek.direction_x = 0
            elif event.key == p.K_DOWN:
                if main.snek.direction_y != -1:
                    main.snek.direction_y = 1
                    main.snek.direction_x = 0
            elif event.key == p.K_LEFT:
                if main.snek.direction_x != 1:
                    main.snek.direction_y = 0
                    main.snek.direction_x = -1
            elif event.key == p.K_RIGHT:
                if main.snek.direction_x != -1:
                    main.snek.direction_y = 0
                    main.snek.direction_x = 1
    WIN.fill(TEAL)
    
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = p.Rect(x, y, CELL_SIZE, CELL_SIZE)
            p.draw.rect(WIN, BLACK, rect, 1)
    clock = p.time.Clock()
    clock.tick(FPS)
    main.draw_element()
    p.display.update()