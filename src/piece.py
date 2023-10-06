import os
import numpy as np
class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class H(Piece):
    def __init__(self):
        
        super().__init__('H', 'white', 10000.0)

class X(Piece):
    def __init__(self):
        
        super().__init__('X', 'white', 10000.0)

class Z(Piece):
    def __init__(self):
        
        super().__init__('Z', 'white', 10000.0)

class S(Piece):
    def __init__(self):
        
        super().__init__('S', 'white', 10000.0)

class M(Piece):
    def __init__(self):
        
        super().__init__('M', 'white', 10000.0)
        
class E(Piece):
    def __init__(self):
        
        super().__init__('E', 'white', 10000.0)
    


class Cat(Piece):
    def __init__(self, color,locaton,stepcount=0):
        self.state = np.array([1,0],dtype = complex)
        self.last_location = locaton
        self.location = locaton
        self.stepcount = stepcount
        super().__init__('cat', 'white', 10000.0)
    
    
        

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)