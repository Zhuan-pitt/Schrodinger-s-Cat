import pygame

from src.const import *
from src.board import Board
from src.dragger import Dragger
from src.config import Config
from src.square import Square
from src.button import *

demo_col = (255,255,210)
demo_col1 = (223,182,1)
txt_col = (18,18,18)
wall_col = (100,50,0)

def draw_text(surface,text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))


class Game:
    
    def __init__(self, level,wall_list):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.level = level
        self.board = Board(self.level,wall_list)
        self.dragger = Dragger()
        self.config = Config()
        self.maximum_step = 10      # Only apply to Level 3
        # Initial number of each gate = 0
        self.buttonS = ButtonS(885,450,80,80, 1, 'S')
        self.buttonH = ButtonH(1035,450,80,80,1,'H')   
        self.buttonX = ButtonX(1035,550,80,80,1, 'X')
        self.buttonZ = ButtonZ(885,550,80,80,1, 'Z')
        
        self.buttonM = ButtonM(885,650,230,80,1, 'M')
        self.board.e_num = 1
        
           

    # blit methods


    def show_bg(self, surface):
        

        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
        
        
        demo = pygame.Rect(COLS*SQSIZE, 0, WIDTH - COLS*SQSIZE, HEIGHT)            
        pygame.draw.rect(surface, demo_col, demo)
        

        
        
        
        draw_text(surface, f'Level: {self.level}', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 40)
        draw_text(surface, 'Current cat\'s state:' , pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 240)
        if abs(self.board.cat.state[0])<=1e-3:
            draw_text(surface, f"|1>", pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 280)
        elif abs(self.board.cat.state[1])<=1e-3:
            draw_text(surface, f"|0>", pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 280)
        
        else:
            b=''
            r = self.board.cat.state[1]/self.board.cat.state[0]
            if r==1 or r==1j:
                draw_text(surface, f"|0> + "+ \
                    f"{r if r.imag else b}|1> ", pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 280)
            if r==-1 or r==-1j:
                draw_text(surface, f"|0> - "+ \
                    f"{-r+0 if r.imag else b}|1> ", pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 280)
            
        demo1 = pygame.Rect(885,350,230,80)            
        pygame.draw.rect(surface, demo_col1, demo1)
        draw_text(surface, f'E-capsule: {self.board.e_num}', pygame.font.SysFont('calibri', 25), txt_col,920,375)
        
        
        
        if self.level < 3:
            draw_text(surface, 'Schrödinger\'s cat is on large for:', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 120)
            draw_text(surface, f'{self.board.cat.stepcount} days', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 160)
            
        elif self.level == 3:
            draw_text(surface, 'You have to catch Schrödinger\'s', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 120)
            draw_text(surface, f'cat in: {self.maximum_step - self.board.cat.stepcount} days', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 160)
            


        self.buttonS.process(surface,self)
        self.buttonX.process(surface,self)
        self.buttonZ.process(surface,self)
        self.buttonH.process(surface,self)
        self.buttonM.process(surface,self)
        

    def gameover(self,surface):   # When all levels are completed
        
        img_file ='assets/images/imgs-80px/end.png'
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img,(800,600))
        img_center = 400,400
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)

    
    def lose(self, surface):
        img_file ='assets/images/imgs-80px/paper.png'
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img,(9*SQSIZE,3*SQSIZE))
        img_center = 400,260
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)
        draw_text(surface, 'You lose! Press Q to quit.' ,\
        pygame.font.SysFont('calibri', 40), txt_col,55+COLS//6*SQSIZE, COLS//5*SQSIZE+70)

    def nextlevel(self,surface):
        
        img_file ='assets/images/imgs-80px/paper.png'
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img,(9*SQSIZE,3*SQSIZE))
        img_center = 400,260
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)
        
        draw_text(surface, f'You captured Schrödinger\'s cat in {self.board.cat.stepcount} days!' ,\
            pygame.font.SysFont('calibri', 30), txt_col,15+COLS//6*SQSIZE, COLS//5*SQSIZE+40)
        draw_text(surface, f'Press R to enter next level ' ,\
            pygame.font.SysFont('calibri', 30), txt_col,COLS//3*SQSIZE, COLS//3*SQSIZE+60)
        

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size= 80)
                        img = pygame.image.load(piece.texture)
                        img = pygame.transform.scale(img,(SQSIZE,SQSIZE))
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_state(self,surface):
        if self.board.cat.location == self.board.cat.last_location:
            return 
        draw_text(surface, f"|0>", pygame.font.SysFont('calibri', 20), txt_col,self.board.cat.last_location[1]*SQSIZE+53,\
                  self.board.cat.last_location[0]*SQSIZE+4)
        draw_text(surface, f"|1>", pygame.font.SysFont('calibri', 20), txt_col,self.board.cat.location[1]*SQSIZE+53,\
                  self.board.cat.location[0]*SQSIZE+4)

    
    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
            
    def show_wall(self, surface):
        for hwall in self.board.wall_list[0]:
            wall_rec = pygame.Rect(hwall[1]*SQSIZE-SQSIZE/10, hwall[0]*SQSIZE-SQSIZE/10, SQSIZE*1.2,SQSIZE/5) 
            pygame.draw.rect(surface,wall_col, wall_rec)
        for vwall in self.board.wall_list[1]:
            wall_rec = pygame.Rect(vwall[1]*SQSIZE-SQSIZE/10, vwall[0]*SQSIZE-SQSIZE/10, SQSIZE/5,SQSIZE*1.2) 
            pygame.draw.rect(surface,wall_col, wall_rec)
    

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def show_start(self,surface):
        img_file ='assets/images/imgs-80px/start.jpeg'
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img,(WIDTH,HEIGHT))
        img_center = WIDTH // 2, HEIGHT // 2
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)

    def show_starttext(self, surface):
        img_file ='assets/images/imgs-80px/starttext.png'
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img,(WIDTH,HEIGHT))
        img_center = WIDTH // 2, HEIGHT // 2
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)
        
        
    def show_tutorial(self,surface):
        self.show_bg(surface)
        if self.level == 1:
            img_file ='assets/images/imgs-80px/level1.png'
        if self.level ==2:
            img_file ='assets/images/imgs-80px/level2.png'
        if self.level ==3:
            img_file ='assets/images/imgs-80px/level3.png'    
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img,(800,600))
        img_center = WIDTH // 2, HEIGHT // 2
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)
        
    def show_back(self,surface):
        img_file ='assets/images/imgs-80px/readme.png'
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img,(800,600))
        img_center = WIDTH // 2, HEIGHT // 2
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    def reset(self, level,wall_list):
        self.__init__(level,wall_list)