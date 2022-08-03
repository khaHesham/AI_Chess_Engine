
import pygame
from const import *
from board import Board


class Game:

    def __init__(self):
        self.board = Board()

    # show methods
    def show_backgnd(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row+col) % 2 == 0:
                    color = (234, 235, 200)  # light green
                else:
                    color = (119, 154, 88)  # dark green

                # start from ,end to , width of rect, height of rect
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    img = pygame.image.load(piece.image)
                    img_center = col*SQSIZE+SQSIZE//2, row*SQSIZE+SQSIZE//2
                    piece.image_rect = img.get_rect(center=img_center)
                    surface.blit(img,piece.image_rect)
