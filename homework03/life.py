import pygame
import random
import time
from pprint import pprint as pp
from pygame.locals import *


class GameOfLife:
    def __init__(self, width = 640, height = 480, cell_size = 10, speed = 1):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed


    def draw_grid(self):
        tf = (0, 255, 0)
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))
        

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        ss = self.cell_list()
        pp(ss)
        self.draw_cell_list(ss)
        
        
        x = self.height // self.cell_size
        y = self.width // self.cell_size

        '''vv = self.take_form_file()'''

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            temp = self.cell_list1()
            '''self.draw_cell_list1(temp)'''
            pp(ss)
            for i in range(x):
                for j in range(y):
                    jj = self.get_neighbours(ss,i,j)  
                    
                    
                    if ((len(jj) > 3) or (len(jj) <2)):
                        temp[i][j] = 0 

                    elif (len(jj) == 3):
                        temp[i][j] = 1
                    else:
                        temp[i][j] = ss[i][j]
            ss = temp.copy()
                        
            self.screen.fill(pygame.Color('white'))
            self.draw_grid()
            self.draw_cell_list(ss)
            pygame.display.flip()
            
            clock.tick(self.speed)
        pygame.quit()


    def take_form_file(self):
        f = open('file.txt')
        grid = f.read()
        grid = list(grid)
        try:
            for i in range(len(grid)):
                vg = grid.index('\n',i)
                grid.pop(vg)
        except:
            pass
        
        print(grid)
            


    def cell_list(self):
        x = self.height // self.cell_size
        y = self.width // self.cell_size
        a = []
        for i in range(x+1):
            if i == 0:
                pass
            else:
                a.append(b)
            b = []
            for j in range(y):
                b.append(random.randrange(0,2))


        return a  

    def cell_list1(self):
        x = self.height // self.cell_size
        y = self.width // self.cell_size
        a = []
        for i in range(x+1):
            if i == 0:
                pass
            else:
                a.append(b)
            b = []
            for j in range(y):
                b.append(0) 
        
        return a 



    def draw_cell_list(self, rects):
        tf = (0, 255, 0)
        x = self.cell_height
        y = self.cell_width
        
        for i in range(x):
            for j in range(y):
                
                if rects[i][j] == 1:
                    print(i,j)
                    h1 = i*self.cell_size
                    w1 = j*self.cell_size    
                    pygame.draw.rect(self.screen, tf, (w1+1, h1+1, self.cell_size-1, self.cell_size-1))

    def draw_cell_list1(self, rects):
        tf = (0, 0,0)
        x = self.cell_height
        y = self.cell_width
        for i in range(x):
            for j in range(y):
                h1 = j*self.cell_size
                w1 = i*self.cell_size    
                pygame.draw.rect(self.screen, tf, (h1, w1, self.cell_size, self.cell_size))





    def get_neighbours(self, rects, cellh, cellw):
        lists = []
        
        try:
            if rects[cellh+1][cellw] == 1:
                lists.append([cellh+1,cellw])
        except:
            pass
            
        try:
            if (rects[cellh-1][cellw] == 1) and (cellh-1 > 0):
                lists.append([cellh-1,cellw])
        except:
            pass
        try:
            if rects[cellh][cellw+1] == 1:
                lists.append([cellh,cellw+1])
        except:
            pass
        try:
            if (rects[cellh][cellw-1] == 1) and (cellw-1 > 0):
                lists.append([cellh,cellw-1])
        except:
            pass
        try:
            if (rects[cellh+1][cellw-1] == 1) and (cellw-1 > 0):
                lists.append([cellh+1,cellw-1])
        except:
            pass
        try:
            if (rects[cellh-1][cellw+1] == 1) and (cellh-1 > 0):
                lists.append([cellh-1,cellw+1])
        except:
            pass
        try:
            if rects[cellh+1][cellw+1] == 1:
                lists.append([cellh+1,cellw+1])
        except:
            pass
        try:
            if (rects[cellh-1][cellw-1] == 1) and (cellh-1 > 0) and (cellw-1 > 0):
                lists.append([cellh-1,cellw-1])
        except:
            pass
        return lists


if __name__ == '__main__':
    game = GameOfLife(600, 600, 20)
    game.run()