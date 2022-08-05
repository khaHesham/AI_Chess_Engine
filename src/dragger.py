

from const import *
import pygame
from piece import *

class Dragger:

    def __init__(self):
        self.mouse_X=0
        self.mouse_Y=0
        self.initial_row=0
        self.initial_col=0
        self.piece=None
        self.dragging=False


    def update_mouse(self,pos):
        self.mouse_X,self.mouse_Y=pos

    def save_initial(self,pos):
        self.initial_row=pos[1]//SQSIZE
        self.initial_col=pos[0]//SQSIZE

    def drag_piece(self,piece):
        self.piece=piece
        self.dragging=True

    def undrag_piece(self):
        self.piece=None
        self.dragging=False

    def update_blit(self,surface):
        self.piece.set_image(size=128)
        image=self.piece.image
        img=pygame.image.load(image)
        img_center=(self.mouse_X,self.mouse_Y)
        self.piece.image_rect=img.get_rect(center=img_center)
        surface.blit(img,self.piece.image_rect)



