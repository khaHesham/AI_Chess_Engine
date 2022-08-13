import pygame
import os
from sound import Sound
from theme import Theme



class Config:
    def __init__(self):
        self.themes=[]
        self._add_themes()
        self.idx=0
        self.theme=self.themes[self.idx]
        self.moved_sound=Sound(os.path.join('D:/GITHUB/Chess_Engine/assets/sounds/move.wav'))
        self.capture_sound=Sound(os.path.join('D:/GITHUB/Chess_Engine/assets/sounds/capture.wav'))
        self.font=pygame.font.SysFont('monospace',18,bold=True)
    def change_theme(self):
        self.idx +=1
        self.idx %= len(self.themes)
        self.theme=self.themes[self.idx]

    def _add_themes(self):  
        brown_me=Theme((242, 231, 191),(80, 48, 30),(204,255,147),(172,195,51),'#90EE90','#e60000')
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#90EE90', '#e60000')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#90EE90', '#e60000')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#90EE90', '#e60000')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#90EE90', '#e60000')

        self.themes=[brown_me,green,brown,blue,gray]