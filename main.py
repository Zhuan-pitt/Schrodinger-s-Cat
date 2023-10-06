import pygame
import numpy as np
import sys
from src.const import *
from src.game import Game
from src.square import Square
from src.move import Move
from src.button import Button
import json

class Main:

    def __init__(self):
        
        pygame.init()
        self.level = 1
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT))
        pygame.display.set_caption('Cat')
        
        with open("assets/wall_list.json", 'r') as f:
            self.wall_list = json.load(f)
        self.game = Game(self.level,self.wall_list[0])
        self.cat_captured = False
        self.maximum_level = 3
    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        
        game_state = "start_pic"
        

        tutorial=True
      

        while True:
            if game_state == 'start_pic':
                pygame.display.update()
                game.show_start(main.screen)
                pygame.display.update()
                pygame.time.wait(2000)
                game_state = 'start_menu'

            if game_state == 'start_menu':
                pygame.display.update()
                game.show_start(main.screen)
                game.show_starttext(screen)
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_state = 'background'
                        if event.key == pygame.K_q:
                            sys.exit()
                            

            if game_state == "background":
                pygame.display.update()
                game.show_back(screen)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_state = 'started'
                    
            
            elif game_state == 'started':
                
                if tutorial :
                    pygame.display.update()
                    game.show_tutorial(screen)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                tutorial = False
                else:
                    
                
             
                    board.add_gate()
                    board.add_e()
                    game.show_bg(screen)
                    game.show_last_move(screen)
                    game.show_moves(screen)
                    game.show_pieces(screen)
                    game.show_wall(screen)
                    game.show_hover(screen)
                    game.show_state(screen)
                

                    if game.next_player == 'white' and self.cat_captured == False:
                        game.show_bg(screen)  
                        game.show_pieces(screen)
                        game.show_wall(screen) 
                        game.show_state(screen)
                        pygame.display.update()
                        pygame.time.wait(400)
                        if abs(board.cat.state[1])!=1 and abs(board.cat.state[0])!=1:
                            game.config.collapse_sound.play()
                        board.collapse()  
                        
                        game.show_bg(screen)  
                        game.show_pieces(screen)
                        game.show_wall(screen) 
                        
                        pygame.display.update()
                        pygame.time.wait(600)
                        pygame.display.update()
                        piece = board.cat
                        board.calc_moves(piece, board.cat.location[0],board.cat.location[1], bool=True)
                            
                        random_move = piece.moves[np.random.randint(len(piece.moves))]
                        board.superposition_move(piece, random_move)
                        board.cat.location = [random_move.final.row,random_move.final.col]
                        board.cat.last_location = [random_move.initial.row,random_move.initial.col]
                        
                        if np.random.random()<0.5:    
                            board.cat.state = np.sqrt(1/2)*np.array([1,1])
                        else:
                            board.cat.state = np.sqrt(1/2)*np.array([1,-1])
                            
                        
                        pygame.time.wait(600)
                    
                        game.play_sound(False)            
                        game.show_bg(screen)  
                        game.show_pieces(screen)
                        game.show_wall(screen) 
                        game.show_last_move(screen)  
                        game.next_turn()
                        game.show_state(screen)
                    
                    
                    #game.show_pieces(screen)
                    
                    if dragger.dragging:
                        dragger.update_blit(screen)
                    
                    
                    
                    for event in pygame.event.get():

                        # click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            dragger.update_mouse(event.pos)

                            if dragger.mouseX > HEIGHT or dragger.mouseY > HEIGHT:
                                continue

                            clicked_row = dragger.mouseY // SQSIZE
                            clicked_col = dragger.mouseX // SQSIZE

                            # if clicked square has a piece ?
                            if board.squares[clicked_row][clicked_col].has_piece():
                                piece = board.squares[clicked_row][clicked_col].piece
                                # valid piece (color) ?
                                if piece.color == game.next_player:
                                    board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(piece)
                                    # show methods 
                                    game.show_bg(screen)  
                                    game.show_pieces(screen)
                                    game.show_wall(screen)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_state(screen)
                                    #game.show_pieces(screen)
                                    #pygame.display.update()
                        
                        # mouse motion
                        elif event.type == pygame.MOUSEMOTION:
                            motion_row = event.pos[1] // SQSIZE
                            motion_col = event.pos[0] // SQSIZE
                                                
                            if motion_row <=9 and motion_col <=9:
                                game.set_hover(motion_row, motion_col)

                                if dragger.dragging:
                                    dragger.update_mouse(event.pos)
                                    # show methods
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)
                                    game.show_wall(screen)
                                    game.show_hover(screen)
                                    game.show_state(screen)
                                    dragger.update_blit(screen)
                        
                        
                        # click release
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if max(motion_row,motion_col)>9:
                                [motion_row,motion_col] =  [round(motion_row/max(motion_row,motion_col)*9),\
                                    round(motion_col/max(motion_row,motion_col)*9)]
                            
                            if motion_row <=9 and motion_col <=9:
                                if dragger.dragging:
                                    dragger.update_mouse(event.pos)

                                    released_row = dragger.mouseY // SQSIZE
                                    released_col = dragger.mouseX // SQSIZE

                                    # create possible move
                                    initial = Square(dragger.initial_row, dragger.initial_col)
                                    final = Square(released_row, released_col)
                                    move = Move(initial, final)

                                    # valid move ?
                                    if board.valid_move(dragger.piece, move):
                                        
                                        # capture cat
                                        
                                        if [released_row , released_col] == board.cat.location: 
                                            if np.random.random()<= abs(board.cat.state[1])**2:
                                                self.cat_captured = True
                                                game.config.cat_sound.play()
                                                board.squares[board.cat.last_location[0]][board.cat.last_location[1]].piece = None
                                                
                                            else:
                                                board.cat.location = board.cat.last_location
                                                board.cat.state = np.array([1,0])
                                            
                                            game.show_bg(screen)  
                                            game.show_pieces(screen)
                                            game.show_wall(screen) 
                                            game.show_state(screen)
                                            pygame.display.update()
                                            
                                        elif [released_row , released_col] == board.cat.last_location: 
                                            if np.random.random()<= abs(board.cat.state[0])**2:
                                                self.cat_captured = True
                                                game.config.cat_sound.play()
                                                board.squares[board.cat.location[0]][board.cat.location[1]].piece = None
                                            
                                            else:
                                                board.cat.last_location = board.cat.location
                                                board.cat.state = np.array([0,1])
                                            game.show_bg(screen)  
                                            game.show_pieces(screen)
                                            game.show_wall(screen) 
                                            game.show_state(screen)
                                            pygame.display.update()
                                        
                                        
                                                
                                        else:
                                        
                                            # normal capture (gates)
                                            captured = board.squares[released_row][released_col].has_piece()
                                            
                                            if captured:    
                                                gate =  board.squares[released_row][released_col].piece
                                                
                                                if gate.name == 'S':
                                                    game.buttonS.num = game.buttonS.num+1
                                                    board.gate_onboard -=1
                                                if gate.name == 'M':
                                                    game.buttonM.num = game.buttonM.num+1
                                                    board.gate_onboard -=1
                                                if gate.name == 'X':
                                                    game.buttonX.num = game.buttonX.num+1
                                                    board.gate_onboard -=1
                                                if gate.name == 'Z':
                                                    game.buttonZ.num = game.buttonZ.num+1
                                                    board.gate_onboard -=1
                                                if gate.name == 'H':
                                                    game.buttonH.num = game.buttonH.num+1
                                                    board.gate_onboard -=1
                                                if gate.name == 'E':
                                                    game.board.e_num = game.board.e_num+1
                                                    board.e_onboard -=1
                                                game.show_bg(screen)  
                                            game.show_pieces(screen)
                                            game.show_wall(screen) 
                                            game.show_state(screen)
                                            pygame.display.update()
                                                    
                                        
                                            # sounds
                                        game.play_sound(captured)
                                        
                                        board.move(dragger.piece, move)
                                        
                                        # show methods
                                        game.show_bg(screen)
                                        game.show_last_move(screen)
                                        game.show_pieces(screen)
                                        game.show_wall(screen)
                                        game.show_state(screen)
                                        # next turn
                                        game.next_turn()
                            
                            dragger.undrag_piece()
                        
                        # key press
                        elif event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                                

                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    
                    if self.cat_captured == True:
                        if self.level < self.maximum_level:
                            
                            game.nextlevel(screen)
                            
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_r:
                                        self.level += 1
                                
                                
                                
                                        tutorial = True
                                        game.reset(self.level,self.wall_list[self.level-1])
                                        game = self.game
                                        
                                        board = self.game.board
                                        if self.level == 2:
                                            self.game.buttonX.num =0
                                            self.game.buttonZ.num =0
                                            self.game.buttonM.num =0
                                        dragger = self.game.dragger
                                        self.cat_captured = False
                            
                            
                        else:
                            game.gameover(screen)
                    pygame.display.update()    
                    
                    if self.level == 3 and (self.game.maximum_step - self.game.board.cat.stepcount)<=0:
                        game_state = 'lose'
                        
            if game_state == 'lose':
                
                pygame.display.update()
                game.lose(screen)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()


main = Main()

main.mainloop()