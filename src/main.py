
from turtle import Screen
import pygame
import sys

from game import Game
from const import *
from square import Square
from move import Move

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
        while True:
            game.show_backgnd(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

             
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row=dragger.mouse_Y//SQSIZE
                    clicked_col=dragger.mouse_X//SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece=board.squares[clicked_row][clicked_col].piece
                        board.calc_move(piece,clicked_row,clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                        #show methods
                        game.show_backgnd(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)



                elif event.type==pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_backgnd(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
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
                            board.move(dragger.piece,move)
                            #show it
                            game.show_backgnd(screen)
                            game.show_pieces(screen)

                    dragger.undrag_piece()

                elif event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
        

main=Main()
main.mainloop()