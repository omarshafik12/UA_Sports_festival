import numpy as np
import sys, time, random, pygame, os, math, cv2, random
from pathlib import Path

# Print the absolute path to ensure the file exists
file_path = Path('webcam_input.py').absolute()

# Add the directory to the Python path
sys.path.append(file_path.parent.as_posix())

try:
    from webcam_input import Prerequisites
except ModuleNotFoundError as e:
    print(f"Error: {e}")


pygame.init()
FPS = 60
clock = pygame.time.Clock()
setup = Prerequisites(1000,1000)


class Drop_off:
    def __init__(self, window):
        self.window = window

        #initial postioning
        self.player_pos = 500
        self.float_x = 500
        self.shigi_pos = 500
        self.shigi_x = 500

        #item & player setup
        self.shigi_regular_bullets = []
        self.shigi_masks = []
        self.player_h = 0
        self.speed = 15
        self.shigi_damage = 100

        #power up timers
        self.cooldown = 10
        self.gearshift_timer = 50
        self.subtractor = 0
        
        #level decider
        self.leveler = 120
        self.level = 5
        self.bullet_timer = 145

        #items
        self.momo_items = []
        self.items = []

        #animation
        self.clock = pygame.time.Clock()
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_delay = 1000
        self.animations = []
        self.creation_image = pygame.image.load("games\Drop Off\Items\momo_quirk.png").convert_alpha()
    
    #generates the list of possible items Momo can drop
    def generate_items(self):
        scale = (1/2)
        for i in range(20):
            i +=1
            item = pygame.image.load(f"games\Drop Off\Items\dropping_items\item_{i}.png").convert_alpha()
            x = 500
            y = 500
            while x > 200 or y > 200:
                x,y = item.get_width(), item.get_height()
                if x > 200 or y > 200:
                    item = pygame.transform.scale(item, (x*scale, y*scale))


            self.momo_items.append(item)

    #updates animations list that is neccessary for sprite animations to execute correctly
    def start_sprite_animation(self, x):
        self.animations.append((x, pygame.time.get_ticks(), 0))

    #draws the sprite animation for item creation
    def creation_animation(self):
        SPRITE_WIDTH, SPRITE_HEIGHT = 62.7, 55
        SPRITES_PER_ROW = 9
        TOTAL_FRAMES = 9  # Only 9 frames in total

        current_time = pygame.time.get_ticks()

        for animation in self.animations[:]:
            x, start_time, frame = animation

            if current_time - start_time > frame * 100:  # Adjust the speed (100 ms per frame here)
                col = frame % SPRITES_PER_ROW

                sprite_x = col * SPRITE_WIDTH
                sprite_y = 0  # Since there's only one row

                self.window.blit(self.creation_image, (x + 25 , 50), (sprite_x, sprite_y, SPRITE_WIDTH, SPRITE_HEIGHT))

                frame += 1
                if frame >= TOTAL_FRAMES:
                    self.animations.remove(animation)
                else:
                    self.animations[self.animations.index(animation)] = (x, start_time, frame)



    #blits frames of spritesheet depending on positioning & direction for Mid
    def get_image(self, sheet, frame, width, scale, player_place, flip,adjustment, who):
        player_w, self.player_h = sheet.get_size()
        player_w, self.player_h = player_w * scale, self.player_h * scale
        sheet = pygame.transform.scale(sheet, (player_w, self.player_h))
        if who == "mid":
            frac = (1/8)
        else:
            frac = (1/6)
        player_w = int(player_w * frac)
        sub_rect = pygame.Rect((frame * player_w) + adjustment, 0, width, self.player_h)
        if flip == False:
            self.window.blit(sheet, (player_place, 1000 - (self.player_h + 40)), ((frame * player_w) + adjustment,0, width, self.player_h))
            mask = pygame.mask.from_surface(sheet.subsurface(sub_rect))
            mask_rect = mask.get_rect(topleft=(player_place, 1000 - (self.player_h + 40)))
        else:
            flipped_image = pygame.transform.flip(sheet, True, False)
            self.window.blit(flipped_image, (player_place, 1000 - (self.player_h + 40)), ((frame * player_w) + adjustment,0, width, self.player_h))
            sub_rect = pygame.Rect((frame * player_w) - adjustment, 0, width, self.player_h)
            mask = pygame.mask.from_surface(flipped_image.subsurface(sub_rect))
            mask_rect = mask.get_rect(topleft=(player_place, 1000 - (self.player_h + 40)))
        return mask, mask_rect, player_place
    
    #blits standing sprite for players
    def get_image_mid_stance(self, sheet, width, height, player_pos):
        sheet = pygame.transform.scale(sheet, (44, 100))
        text_x = (player_pos - 29)
        self.window.blit(sheet, (text_x, 1000 - (height + 40) ), (0,0, width, height))
        
        mask = pygame.mask.from_surface(sheet)
        mask_rect = mask.get_rect(topleft = (text_x, 1000 - (height + 40)))
        return mask, mask_rect, text_x   
     
    def get_image_shigi_stance(self, sheet, width, height, player_pos):
        sheet = pygame.transform.scale(sheet, (58, 134))
        self.window.blit(sheet, (player_pos - 29, 20), (0,0, width, height))
    
    #intakes values regarding position and decides whether to blit running animation or stance and moves the player to inputted location
    def player_move(self, window, finger_x, finger_y, mid_run_list,frame, player_stance):
        w, h = pygame.display.get_surface().get_size()
        self.float_x = w - (finger_x * w)
        self.float_y = int(finger_y * h) 

        if frame > 7:
            frame = 0
        
        if self.player_pos == self.float_x:
            if self.float_x == 1000:
                mask, subrect,text_x = self.get_image_mid_stance(player_stance, 44, 100, 500)
            else:
                mask, subrect,text_x = self.get_image_mid_stance(player_stance, 44, 100, self.player_pos)

        elif self.player_pos < self.float_x: #moving right
            mask, subrect,text_x = self.get_image(mid_run_list, frame, 75, 2, self.player_pos, False, 15, "mid")
            self.player_pos = self.float_x
            frame += 1

        elif self.player_pos > self.float_x: #moving left
            mask, subrect,text_x = self.get_image(mid_run_list, frame, 80, 2, self.player_pos, True, -5, "mid")
            self.player_pos = self.float_x
            frame += 1
        return frame, True, self.float_x, mask, subrect, text_x
    
    #Uses masks for pixel perfect collision with items and Midoriya
    def bullet_collisions(self, player, enemy, player_frame, enemy_frame):
        offset_x = enemy_frame.left - player_frame.left
        offset_y = enemy_frame.top - player_frame.top
        if player.overlap(enemy, (offset_x, offset_y)):
            return True
        else:
            return False
    
    #Initiates sprite animation and adds items to the falling list
    def shoot_projectile_mid(self, time, player_pos_x, mask, subrect, shigi_stance): 
        if time == self.bullet_timer:
            item_picker = random.randrange(0,20)
            self.shigi_x = random.randrange(0,901)
            bullet = self.momo_items[item_picker]
            self.items.append(bullet)
            self.shigi_regular_bullets.append([self.shigi_x, 30 , self.shigi_damage])
            self.shigi_masks.append([self.shigi_pos, 0 + (134 + 30)])
            self.bullet_timer -= self.level

        positive_check_1 = player_pos_x + 200
        negative_check_2 = player_pos_x - 200

        shigi_mask_index = -1
        index = -1
        for points in self.shigi_regular_bullets:
            if points[1] == 30:
                self.start_sprite_animation(self.shigi_x)
            points[1] = points[1] + 10 #controls speed
            shigi_mask_index += 1
            self.shigi_masks[shigi_mask_index][1] = points[1]
            if points[1] > 1000: 
                shigi_index = self.shigi_regular_bullets.index(points)
                self.shigi_regular_bullets.pop(shigi_index)
                self.items.pop(shigi_index)
            index +=1
            self.window.blit(self.items[index], (points[0], points[1]))
            if negative_check_2 < points[0] < positive_check_1:
                momo_shot_mask = pygame.mask.from_surface(self.items[index])
                momo_shot_rect = momo_shot_mask.get_rect(topleft=(points[0], points[1]))
                result = self.bullet_collisions(mask, momo_shot_mask, subrect, momo_shot_rect)
                if result == True and time > 0:
                    print(False)
                    setup.webcam.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
        
        self.get_image_shigi_stance(shigi_stance, 58, 134, self.shigi_x)   

        self.difficulty_increase(time)  

        return time
    
    #for every 30 seconds the interval between item creation decreases by a second until at the final 30 seconds a new item will generate every second
    def difficulty_increase(self, time):
        if time == self.leveler and time != 0:
            self.leveler -= 30
            self.level -= 1
        if time == 0: 
            print(True)
            setup.webcam.release()
            cv2.destroyAllWindows()
            pygame.quit()