import pygame
import numpy as np
import sys
from src.const import *
from src.game import Game
from src.square import Square
from src.move import Move
from src.button import Button


class Main:

    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
          
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if game.next_player == 'white':
                pygame.display.update()
                pygame.time.wait(600)
                
                board.collapse()  
                game.show_bg(screen)  
                game.show_pieces(screen) 
                pygame.display.update()
                pygame.time.wait(600)
                
                
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
                game.show_last_move(screen)    
                game.show_pieces(screen)
                game.next_turn()
            
            
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
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
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
                            game.show_hover(screen)
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
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)

                                # sounds
                                game.play_sound(captured)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()
                    
                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    

                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                    
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()


main = Main()
main.mainloop()