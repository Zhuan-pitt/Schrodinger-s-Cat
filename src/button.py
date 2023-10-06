import pygame
import numpy as np
from src.config import Config
import os
# def update_piece(game):
#     state = game.board.cat.state
#     if np.linalg.norm(state-np.array([1,0])) <=1e-10:
#             game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece =game.board.cat
#             game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = None

#     elif np.linalg.norm(state-np.array([0,1])) <=1e-10:
#             game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = None
#             game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat
#     elif np.linalg.norm(state-np.sqrt(1/2)*np.array([1,1])) <=1e-10:
#             game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = game.board.cat
#             game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat

#     elif np.linalg.norm(state-np.sqrt(1/2)*np.array([1,-1])) <=1e-10:
#             game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = game.board.cat
#             game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat

def update_piece(game):
    state = game.board.cat.state
    if abs(state[1]) <=1e-3:
        game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece =game.board.cat
        game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = None

    elif abs(state[0]) <=1e-10:
        game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = None
        game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat
    else:
        game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = game.board.cat
        game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat

class Button():

    def __init__(self, x, y, width, height, num=0, name='Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.font = pygame.font.SysFont('calibri', 25)
        self.num = num
        self.config = Config()
        self.fillColors = {
            'normal': [252,236,165],
            'border_normal': [0,0,0],
            'border_hover': [79, 158, 226],
            'pressed': [203,167,55],
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.buttonSurf = self.font.render(name, True, (20, 20, 20))

        self.numSurface = pygame.Surface((40, 40))
        
        
        self.numRect = pygame.Rect(self.x+self.width, self.y+40, 40, 40)
        
        self.pressed = 1

    def process(self, surface,input):

        
        

        self.numSurf = self.font.render(f'{int(self.num)}', True, (10, 10, 10))
        self.numSurface.blit(self.numSurf, [
            self.numRect.width/2 - self.numSurf.get_rect().width/2,
            self.numRect.height/2 - self.numSurf.get_rect().height/2
        ])
        surface.blit(self.numSurface, self.numRect)
        
        
        

        # border of buttons

        # border_coords = ((self.x, self.y), (self.x+self.width, self.y), (self.x+self.width, self.y+self.height), (self.x, self.y+self.height))
        # border_thickness = 5
        # pygame.draw.lines(surface, '#666666', True, (border_coords), border_thickness)

        self.buttonSurface.blit(self.buttonSurf, [
                    self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                    self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
                ])
        
        surface.blit(self.buttonSurface, self.buttonRect)

        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        self.numSurface.fill(self.fillColors['normal'])
        pygame.draw.rect(surface, self.fillColors['border_normal'], (self.x, self.y, self.width, self.height), width=3)

        if self.buttonRect.collidepoint(mousePos):
            # self.buttonSurface.fill(self.fillColors['hover'])
            pygame.draw.rect(surface, self.fillColors['border_hover'], (self.x, self.y, self.width, self.height), width=3)

            if pygame.mouse.get_pressed()[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.config.button_sound.play()
                if self.pressed == 1 and self.num>0:
                    self.command(surface,input)
                    self.pressed = 0
                    self.num -= 1

            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1

        
        

class ButtonS(Button):
    def command(self,surface1,game):
        S = np.array([[1,0],[0,1j]],dtype = complex)
        game.board.cat.state = S@game.board.cat.state 
        game.show_pieces(surface1) 

class ButtonX(Button):
    def command(self,surface,game):
        X = np.array([[0,1],[1,0]])
        
        game.board.cat.state = X@game.board.cat.state  
        update_piece(game)      
        game.show_pieces(surface) 

class ButtonZ(Button):
    def command(self,surface,game):
        Z= np.array([[1,0],[0,-1]])
        game.board.cat.state = Z@game.board.cat.state
        game.show_pieces(surface) 



class ButtonH(Button):
    def command(self,surface,game):
        H = np.sqrt(1/2)*np.array([[1,1],[1,-1]])
        
        game.board.cat.state = H@game.board.cat.state
        update_piece(game)  
        game.show_pieces(surface) 

       
    
class ButtonM(Button):
    def command(self,surface,game):
        game.board.measure()