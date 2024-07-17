import sys, time, random, pygame, os, math, cv2
import numpy as np
from pathlib import Path

#webcam_input import
file_path = Path('webcam_input.py').absolute()

sys.path.append(file_path.parent.as_posix())

try:
    from webcam_input import Prerequisites
except ModuleNotFoundError as e:
    print(f"Error: {e}")

pygame.init()
FPS = 60
clock = pygame.time.Clock()
setup = Prerequisites(1000,1000)

#player creation
col = (255, 0, 0)
player = pygame.Surface((20,20))
player.fill(col)
player_frame = player.get_rect(center = (0,0))
player_mask = pygame.mask.from_surface(player)
player_mask_frame = player_mask.get_rect()

class Squid_game_mechanics():
    def __init__(self, window, cookie_mask, player, player_frame, player_mask):
        self.window = window
        self.player = player
        self.player_frame = player_frame
        self.player_x = self.player_frame.x
        self.player_y = self.player_frame.y
        self.cookie_mask = cookie_mask
        self.player_mask_frame = player_mask
        self.lines = []
        self.temp_line = []
        self.counter = 0
    
    #aligns the players rectangle with the player's index finger
    def move_draw(self,w,h, x, y):
        self.x = x
        self.y = y
        temp = self.x * w
        self.player_frame.centerx = w - temp
        self.player_frame.centery = self.y * h
        self.player_mask_frame.centerx = self.player_frame.centerx
        self.player_mask_frame.centery = self.player_frame.centery
        self.window.blit(self.player, self.player_frame)
        return self.player_mask_frame

    #checks collision and appends list that draws lines
    def check_collision(self, player_mask, cookie_mask_rect):
        offset_x = self.player_frame.left - cookie_mask_rect.left
        offset_y = self.player_frame.top - cookie_mask_rect.top
        if self.cookie_mask.overlap(player_mask, (offset_x, offset_y)):
            col = (3, 252, 252)
            self.player.fill(col)
            self.temp_line.append([self.player_frame.x, self.player_frame.y])
            if len(self.temp_line) == 2:
                self.lines.append([self.temp_line[0], self.temp_line[1]])
                self.temp_line.clear()
            return True
        else:
            col = (255, 0, 0)
            self.player.fill(col)
            return False
    
    #Grabs portion of screen and checks ratios to determine level continuation
    def grab_screen(self,x,y,w,h, window):
        width = 300
        height= 300
        total_pixels = 90000
        
        rect = pygame.Rect(x,y,w,h)
        sub = window.subsurface(rect).copy()

        green_count = 0
        black_count = 0

        for x in range(width):
            for y in range(height):
                color = sub.get_at((x, y))[:3]
                if color == (3, 252, 252):
                    green_count += 1
                elif color == (0, 0, 0):
                    black_count += 1
        if black_count == 0:
            return True

        green_to_black_ratio = green_count / black_count
        if green_to_black_ratio > 10:
            return True
        else:
            return False