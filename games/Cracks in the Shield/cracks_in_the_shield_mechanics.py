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


class Cracks_in_the_shield():
    #sets up key variables for player
    def __init__(self, window, player, player_frame, player_mask):
        self.window = window
        self.player = player
        self.player_frame = player_frame
        self.player_x = self.player_frame.x
        self.player_y = self.player_frame.y
        self.player_mask_frame = player_mask
        self.track_line = [0,0]
        self.correction_angle = 135
        #   0 - image is looking to the right
        #  90 - image is looking up
        # 180 - image is looking to the left
        # 270 - image is looking down

    #arm movement and direction determination
    def rotate_player_movement(self, player, player_frame):
        self.track_line.append(player_frame.centerx)
        self.track_line.append(player_frame.centery)
        dy,dx = self.track_line[3] - self.track_line[1], self.track_line[2] - self.track_line[0]

        if abs(dy) > 20 or abs(dx) >20:
            angle = math.atan2(-dy, dx)
            angle_degrees = math.degrees(angle) - self.correction_angle
            self.player = pygame.transform.rotate(player, angle_degrees)
        self.track_line.pop(0)
        self.track_line.pop(0)
    
    #moves the arm to match the player's finger
    def move_draw(self,w,h, x, y):
        self.x = x
        self.y = y
        temp = self.x * w
        self.player_frame.centerx = w - temp
        self.player_frame.centery = (self.y * h) - 10
        self.player_mask_frame.centerx = self.player_frame.centerx
        self.player_mask_frame.centery = self.player_frame.centery
        self.window.blit(self.player, self.player_frame)
        return self.player_mask_frame
    
    #Randomly generates weak points on top of kirishima
    def weak_point_generation(self, image, length, width, height, x_adjustment, y_adjustment):
        list = []
        x_result = None
        y_result = None
        while len(list) < length:
            x = random.randint(1, width-1)
            y = random.randint(1, height-1)

            try:
                pixel_value = image.get_at((x,y))
                alpha_value = pixel_value[3]
                
            except IndexError:
                alpha_value = 0

            try:
                #if mask.get_at((x, y)):
                if alpha_value == 255:
                    x_result = x
                    y_result = y
                    list.append((x_result + x_adjustment, y_result + y_adjustment))
            except IndexError:
                pass
        return list

    #Checks for collision between the player and point
    def collision(self, player, enemy, player_frame, enemy_frame):
        offset_x = enemy_frame.left - player_frame.left
        offset_y = enemy_frame.top - player_frame.top
        if player.overlap(enemy, (offset_x, offset_y)):
            return True
        else:
            return False