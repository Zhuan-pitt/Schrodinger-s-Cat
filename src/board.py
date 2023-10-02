from src.const import *
from src.square import Square
from src.piece import *
from src.move import Move
from src.sound import Sound
import copy
import os

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self.cat = Cat('white',[4,4])
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    
    def superposition_move(self,piece,move): 
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = piece
        self.squares[final.row][final.col].piece = piece
        # move
        piece.moved = True
        # set last move
        self.last_move = move   
        
    def collapse(self):
        # console board move update
        
        p_new = self.cat.state[1]**2/(np.linalg.norm(self.cat.state))**2
        if np.random.random()<=p_new:
            self.squares[ self.cat.last_location[0]][ self.cat.last_location[1]].piece = None
            self.cat.state = np.array([0,1])
        else:
            self.squares[ self.cat.location[0]][ self.cat.location[1]].piece = None
            self.cat.state = np.array([1,0])
            self.cat.location =  self.cat.last_location
        # clear valid moves
        self.cat.clear_moves()
    
    def measure(self):
        p_new = self.cat.state[1]**2/(np.linalg.norm(self.cat.state))**2
        if np.random.random()<=p_new:
            self.squares[ self.cat.last_location[0]][ self.cat.last_location[1]].piece = None
            self.cat.state = np.array([0,1])
        else:
            self.squares[ self.cat.location[0]][ self.cat.location[1]].piece = None
            self.cat.state = np.array([1,0])
            
            
    
    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        # move
        piece.moved = True
        self.cat.stepcount += 1
        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves


    
    def calc_moves(self, piece, row, col, bool=True):
        '''
            Calculate all the possible (valid) moves of an specific piece on a specific position
        '''
        
      
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        piece.add_move(move)


        def cat_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potencial checks
                        if bool:
                            piece.add_move(move)
                            
                        else:
                            # append new move
                            piece.add_move(move)
        

        if isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Cat): 
            cat_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        
        self.squares[self.cat.location[0]][self.cat.location[1]] = Square(self.cat.location[0],self.cat.location[1], self.cat)
            