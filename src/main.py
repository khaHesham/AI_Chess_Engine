
from turtle import Screen
import pygame
import sys

from game import Game
from const import *
from square import Square
from move import Move
import time

class Main:

    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Chess')
        self.game=Game()
        

    def mainloop(self):
        screen=self.screen
        game=self.game
        dragger=self.game.dragger
        board=self.game.board
        Random=False
        
        while True:
            
            game.show_backgnd(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            # generating random moves:
            if Random:
                piece,move_random=board.random_move(game.next_player)
                # print(f'{piece.name}.({move_random.initial.row},{move_random.initial.col}) - > ({move_random.final.row},{move_random.final.col})')
                captured=board.squares[move_random.final.row][move_random.final.col].has_piece()
                board.move(piece,move_random)
                board.set_true_en_passant(piece)
                #playing sounds
                # game.sound_effect(captured)
                #show it
                game.show_backgnd(screen)
                game.show_last_move(screen)
                game.show_pieces(screen)
                game.next_turn()
                time.sleep(0.1)


            if dragger.dragging:
                dragger.update_blit(screen)

             
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    
                    clicked_row=dragger.mouse_Y//SQSIZE
                    clicked_col=dragger.mouse_X//SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece=board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player:
                            board.calc_move(piece,clicked_row,clicked_col,bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            #show methods
                            game.show_backgnd(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)



                elif event.type==pygame.MOUSEMOTION:
                    motion_row=event.pos[1]//SQSIZE
                    motion_col=event.pos[0]//SQSIZE

                    game.set_hover(motion_row,motion_col)
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_backgnd(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                elif event.type==pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row=dragger.mouse_Y//SQSIZE
                        released_col=dragger.mouse_X//SQSIZE

                        initial=Square(dragger.initial_row,dragger.initial_col)
                        final=Square(released_row,released_col)
                        move=Move(initial,final)

                        #check if it is a move
                        if board.valid_move(dragger.piece,move):
                            #normal capture
                            captured=board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece,move)

                            board.set_true_en_passant(dragger.piece)

                            #playing sounds
                            game.sound_effect(captured)
                            #show it
                            game.show_backgnd(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()

                            # if board.is_Game_Over():
                            #     game.reset()
                            #     game=self.game
                            #     dragger=self.game.dragger
                            #     board=self.game.board

                    dragger.undrag_piece()

                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_t:
                        game.change_theme()

                    if event.key==pygame.K_r:
                        game.reset()
                        game=self.game
                        dragger=self.game.dragger
                        board=self.game.board
                    if event.key==pygame.K_u:
                        Random= not Random

                elif event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
        

main=Main()
main.mainloop()