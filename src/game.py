
import pygame
from pyparsing import col
from const import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger=Dragger()

    # show methods
    def show_backgnd(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row+col) % 2 == 0:
                    color = (242, 231, 191)  # light green
                else:
                    color = (80, 48, 30)  # dark green

                # start from ,end to , width of rect, height of rect
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece


                    #all piecec except the one iam dragging
                    if piece is not self.dragger.piece:
                        piece.set_image(size=80)
                        img = pygame.image.load(piece.image)
                        img_center = col*SQSIZE+SQSIZE//2, row*SQSIZE+SQSIZE//2
                        piece.image_rect = img.get_rect(center=img_center)
                        surface.blit(img,piece.image_rect)

    def show_moves(self,surface):
        if self.dragger.dragging:
            piece=self.dragger.piece
            #loop over all valid moves to blit them
            
            for move in piece.moves:
                if self.board.squares[move.final_square().row][move.final_square().col].isempty():
                    color='#90EE90'
                    pygame.draw.circle(surface,color,(move.final.col*SQSIZE+SQSIZE//2,move.final.row*SQSIZE+SQSIZE//2),SQSIZE//6)
                else: #has enemy in it
                    color='#e60000'
                    rect=(move.final.col*SQSIZE, move.final.row*SQSIZE, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)
                