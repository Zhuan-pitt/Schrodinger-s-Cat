import pygame

from src.const import *
from src.board import Board
from src.dragger import Dragger
from src.config import Config
from src.square import Square
from src.button import *

demo_col = (255,255,210)
txt_col = (18,18,18)


def draw_text(surface,text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))


class Game:
    
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

        # Initial number of each gate = 10 [test]
        self.buttonS = ButtonS(885,400,80,80, 1, 'S')
        self.buttonX = ButtonX(1035,400,80,80,1, 'X')
        self.buttonZ = ButtonZ(885,500,80,80,1, 'Z')
        self.buttonH = ButtonH(1035,500,80,80, 1,'H')   
        self.buttonM = ButtonM(885,600,230,80,1, 'M')   

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
        
        draw_text(surface, 'Current cat\'s state:' , pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 120)
        draw_text(surface, f'{np.round(self.board.cat.state, 2)}', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 160)

        draw_text(surface, 'Schrödinger\'s cat is on large for:', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 10)
        draw_text(surface, f'{self.board.cat.stepcount} days', pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 50)

        self.buttonS.process(surface,self)
        self.buttonX.process(surface,self)
        self.buttonZ.process(surface,self)
        self.buttonH.process(surface,self)
        self.buttonM.process(surface,self)


    def gameover(self,surface):
        demo = pygame.Rect(COLS//6*SQSIZE, COLS//5*SQSIZE,COLS//5*SQSIZE*4, HEIGHT//4) 
        pygame.draw.rect(surface, demo_col, demo)
        draw_text(surface, f'You capture Schrödinger\'s cat in {self.board.cat.stepcount} days!' ,\
            pygame.font.SysFont('calibri', 30), txt_col,15+COLS//6*SQSIZE, COLS//5*SQSIZE+40)
        draw_text(surface, f'Press r to restart' ,\
            pygame.font.SysFont('calibri', 30), txt_col,10+COLS//3*SQSIZE, COLS//3*SQSIZE+60)
        


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


    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()