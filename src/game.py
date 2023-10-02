import pygame

from src.const import *
from src.board import Board
from src.dragger import Dragger
from src.config import Config
from src.square import Square
from src.button import *

demo_col = (255,255,210)
txt_col = (18,18,18)

def command_S():
    print("Command S")

def command_X():
    print("Command X")

def command_Z():
    print("Command Z")

def command_H():
    print("Command H")

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
        self.buttonS = ButtonS(900,400,80,80, 'S')
        self.buttonX = ButtonX(1050,400,80,80, 'X')
        self.buttonZ = ButtonZ(900,550,80,80, 'Z')
        self.buttonH = ButtonH(1050,550,80,80, 'H')   

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
        
        draw_text(surface, f'Current cat\'s state: {self.board.cat.state}' , pygame.font.SysFont('calibri', 25), txt_col,20+COLS*SQSIZE, 10)
          
        self.buttonS.process(surface)
        self.buttonX.process(surface)
        self.buttonZ.process(surface)
        self.buttonH.process(surface)
	    #draw_text(f'Paddel type: { player_paddle.species }', pygame.font.SysFont('calibri', 20), text_col, \
     #20+play_width, 40)

    


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