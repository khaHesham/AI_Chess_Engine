
from tkinter.tix import ROW
import pygame
from pyparsing import col
from const import *
from board import Board
from dragger import Dragger
from square import Square
from config import Config

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger=Dragger()
        self.next_player='white'
        self.hovered_sqr=None
        self.config=Config()
    # show methods
    def show_backgnd(self, surface):
        theme=self.config.theme

        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row+col) % 2 == 0:
                  color = theme.bg.light  
                else:
                  color = theme.bg.dark  

                # start from ,end to , width of rect, height of rect
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                if col==0:
                    color=theme.bg.dark if row%2==0 else theme.bg.light
                    lbl=self.config.font.render(str(ROWS-row),1,color)
                    lbl_pos=(5,5+row*SQSIZE)
                    surface.blit(lbl,lbl_pos)

                if row==7:
                    color=theme.bg.dark if (row+col)%2==0 else theme.bg.light
                    lbl=self.config.font.render(Square.get_alphacol(col),1,color)
                    lbl_pos=(col*SQSIZE+SQSIZE-18,HEIGHT-25)
                    surface.blit(lbl,lbl_pos)

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
        theme=self.config.theme

        if self.dragger.dragging:
            piece=self.dragger.piece
            #loop over all valid moves to blit them
            
            for move in piece.moves:
                if self.board.squares[move.final_square().row][move.final_square().col].isempty():
                    color=theme.moves.light
                    pygame.draw.circle(surface,color,(move.final.col*SQSIZE+SQSIZE//2,move.final.row*SQSIZE+SQSIZE//2),SQSIZE//6)
                else: #has enemy in it
                    color=theme.moves.dark
                    rect=(move.final.col*SQSIZE, move.final.row*SQSIZE, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self,surface):
        theme=self.config.theme
        if self.board.last_move:
            initial=self.board.last_move.initial
            final=self.board.last_move.final

            for pos in [initial, final]:
                color=theme.trace.light if (pos.row + pos.col)%2==0 else theme.trace.dark
                rect=(pos.col*SQSIZE,pos.row*SQSIZE,SQSIZE,SQSIZE)
                pygame.draw.rect(surface,color,rect)

    def show_hover(self,surface):
        color=(180,180,100) 
        rect=(self.hovered_sqr.col*SQSIZE,self.hovered_sqr.row*SQSIZE,SQSIZE,SQSIZE)
        pygame.draw.rect(surface,color,rect,width=5)

    def set_hover(self,row,col):
        if Square.in_range(row,col):
            self.hovered_sqr=self.board.squares[row][col]

    def next_turn(self):
        self.next_player='white' if self.next_player=='black' else 'black'

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self,captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.moved_sound.play()

    def reset(self):
        self.__init__()