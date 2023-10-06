from src.const import *
from src.square import Square
from src.piece import *
from src.move import Move
from src.sound import Sound
from src.config import Config
import copy
import os

class Board():

    def __init__(self, level, wall_list=[[[3,3],[3,4],[3,5],[3,8]],[[3,3],[4,3],[5,3]]]):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self.cat = Cat('white',[4,6])
        self._create()
        #self._add_pieces('white')
        self.config = Config()
        self._add_pieces('black')
        self.e_num = 1
        self.e_onboard = 0
        self.gate_onboard = 0
        self.level = level
        self.wall_list = wall_list #[horizontal,vertical],[row, col]
        
        for hwall in self.wall_list[0]:
            self.squares[hwall[0]][hwall[1]].has_hwall = True
        for vwall in self.wall_list[1]:
            self.squares[vwall[0]][vwall[1]].has_vwall = True
    
    
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
        
        p_new = abs(self.cat.state[1])**2/(np.linalg.norm(self.cat.state))**2
        if np.random.random()<=p_new and self.cat.last_location != self.cat.location:
            self.squares[ self.cat.last_location[0]][ self.cat.last_location[1]].piece = None
            self.cat.state = np.array([0,1])
        elif self.cat.last_location != self.cat.location:
            self.squares[ self.cat.location[0]][ self.cat.location[1]].piece = None
            self.cat.state = np.array([1,0])
            self.cat.location =  self.cat.last_location
        # clear valid moves
        self.cat.clear_moves()
    
    def measure(self):
        p_new = abs(self.cat.state[1])**2/(np.linalg.norm(self.cat.state))**2
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
        if not self.not_blocked([initial.row,initial.col],[final.row,final.col]):
                self.e_num=self.e_num-1
                self.config.collapse_sound.play()
            

    def valid_move(self, piece, move):
        return move in piece.moves

    def add_gate(self,list=[H(),S(),X(),Z(),M()]):
        while self.gate_onboard <= 3 :
            x = np.random.randint(ROWS)
            y = np.random.randint(COLS)
            if self.squares[x][y].isempty() == True:
                if self.level == 1 or self.level > 2:
                    p = np.random.randint(len(list))   # All gates are available in Level 1 and Level 3
                elif self.level == 2:
                    p = np.random.randint(2)    # Only H gate and S gate are available in Level 2
                self.squares[x][y] = Square(x,y, (list[p]))
                self.gate_onboard +=1

            else:
                self.add_gate(list=list)
        
    def add_e(self):
        while  self.e_onboard <2:
            x = np.random.randint(ROWS)
            y = np.random.randint(COLS)
            if self.squares[x][y].isempty() == True:
                self.squares[x][y] = Square(x,y, E())
                self.e_onboard +=1

            else:
                self.add_e()
    
    
    def not_blocked(self,start,end):
        row_move = end[0]-start[0]
        col_move = end[1]-start[1]
        
        #knight has two ways to move to the same position
        
        path1 = True # first row, then col
        
        if row_move>0:
            for i in range(abs(row_move)):
                path1 = path1 and not self.squares[start[0]+i+1][start[1]].has_hwall
        if row_move<0:
            for i in range(abs(row_move)):
                
                path1 = path1 and not self.squares[start[0]-i][start[1]].has_hwall        
        if col_move>0:
            for i in range(abs(col_move)):
                path1 = path1 and not self.squares[start[0]+row_move][start[1]+i+1].has_vwall
        if col_move<0:
            for i in range(abs(col_move)):
                path1 = path1 and not self.squares[start[0]+row_move][start[1]-i].has_vwall
            
        
        
        path2 = True
        
        if col_move>0:
            for i in range(abs(col_move)):
                path2 = path2 and not self.squares[start[0]][start[1]+i+1].has_vwall
        if col_move<0:
            for i in range(abs(col_move)):
                path2 = path2 and not self.squares[start[0]][start[1]-i].has_vwall
        
        if row_move>0:
            for i in range(abs(row_move)):
                path2 = path2 and not self.squares[start[0]+i+1][start[1]+col_move].has_hwall
        if row_move<0:
            for i in range(abs(row_move)):
                path2 = path2 and not self.squares[start[0]-i][start[1]+col_move].has_hwall
        
        return path1 or path2
        
        
        
    
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
                    
                    if self.e_num==0:
                        if self.not_blocked([row,col],[possible_move_row,possible_move_col]):
                        
                        
                            if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                                # create squares of the new move
                                initial = Square(row, col)
                                final_piece = self.squares[possible_move_row][possible_move_col].piece
                                final = Square(possible_move_row, possible_move_col, final_piece)
                                # create new move
                                move = Move(initial, final)
                                
                                # check potencial checks
                                piece.add_move(move)
                    if self.e_num>0:
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
                (row-2, col+0), # up
                (row-2, col+2), # up-right
                (row+0, col+2), # right
                (row+2, col+2), # down-right
                (row+2, col+0), # down
                (row+2, col-2), # down-left
                (row+0, col-2), # left
                (row-2, col-2), # up-left
                (row-2, col+1), # up
                (row+1, col+2), # right
                (row+2, col+1), # down
                (row+2, col-2), # down-left
                (row+1, col-2), # left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty():
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
    
        # knights
        self.squares[0][0] = Square(0,0, Knight('black'))
        
        
        self.squares[self.cat.location[0]][self.cat.location[1]] = Square(self.cat.location[0],self.cat.location[1], self.cat)
            