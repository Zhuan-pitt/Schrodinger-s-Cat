import pygame
import numpy as np


def update_piece(game):
    state = game.board.cat.state
    if np.linalg.norm(state-np.array([1,0])) <=1e-10:
            game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece =game.board.cat
            game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = None

    elif np.linalg.norm(state-np.array([0,1])) <=1e-10:
            game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = None
            game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat
    elif np.linalg.norm(state-np.sqrt(1/2)*np.array([1,1])) <=1e-10:
            game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = game.board.cat
            game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat

    elif np.linalg.norm(state-np.sqrt(1/2)*np.array([1,-1])) <=1e-10:
            game.board.squares[ game.board.cat.last_location[0]][ game.board.cat.last_location[1]].piece = game.board.cat
            game.board.squares[ game.board.cat.location[0]][ game.board.cat.location[1]].piece = game.board.cat




class Button():

    def __init__(self, x, y, width, height, buttonText='Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.font = pygame.font.SysFont('calibri', 25)
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))
        self.pressed = 1


    def process(self, surface,input):
        
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.command(surface,input)
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1
        
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        surface.blit(self.buttonSurface, self.buttonRect)
    

class ButtonS(Button):
    def command(self,surface1,game):
        S = np.array([[1,0],[0,1]])
        print('SSS')
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