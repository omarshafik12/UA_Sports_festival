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
pygame.display.set_caption("Kirishima VS Midoriya")
FPS = 60
clock = pygame.time.Clock()
setup = Prerequisites(1000,1375)

class Bullets(pygame.sprite.Sprite):
    #initialization of created bullets:
        #x,y = bullet location
        #damage - accounts for varied impact of bullets especially the Fa Jin Bullet
        #identifier - allows for the indexing of the bullet for certain actions
        #direction - solely accounted for the purpose of the smoke screen 
    def __init__(self, x=0, y=0, damage=0, identifier=0, image=None, direction = 1):
        super().__init__()
        self.image = image
        if image != None:
            self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = damage
        self.identifier = identifier
        self.direction = direction
    
    #moves mid bullets up and shigi down unless a collision with smoke occurs
    def update(self, speed):
        self.rect.y -= speed * self.direction
    
    #the detection and record of collisions between three various items: Mid bullets, shigi bullets, smokescreen
        #returned to the bullet_collisions() function within Decay_Invaders()
    def check_collisions(self, smoke_screen, mid_bullet_list, shigi_bullet_list):
        mid_collision_list = []
        shigi_collision_list = []
        smoke_mid_collision_list = []
        smoke_shigi_collision_list = []
        collisions = pygame.sprite.groupcollide(mid_bullet_list, shigi_bullet_list, False, False)
        smoke_collisons_shigi = pygame.sprite.groupcollide(smoke_screen, shigi_bullet_list, False, False)
        smoke_collisons_mid = pygame.sprite.groupcollide(smoke_screen, mid_bullet_list, False, False)
        if collisions:
            for mid_bullet, shigi_bullets in collisions.items():
                for shigi_bullet in shigi_bullets:
                    mid_collision_list.append(mid_bullet.identifier)
                    shigi_collision_list.append(shigi_bullet.identifier)
                    #print(f"Mid bullet {mid_bullet.identifier} collided with Shigi bullet {shigi_bullet.identifier}")
        if smoke_collisons_shigi:
            for smoke_screen, shigi_bullets in smoke_collisons_shigi.items():
                for shigi_bullet in shigi_bullets:
                    smoke_shigi_collision_list.append(shigi_bullet.identifier)
                    #print(f"Mid bullet {mid_bullet.identifier} collided with Shigi bullet {shigi_bullet.identifier}")
        if smoke_collisons_mid:
            for smoke_screen, mid_bullets in smoke_collisons_mid.items():
                for mid_bullet in mid_bullets:
                    smoke_mid_collision_list.append(mid_bullet.identifier)
                    #print(f"Mid bullet {mid_bullet.identifier} collided with Shigi bullet {shigi_bullet.identifier}")
        return mid_collision_list, shigi_collision_list, smoke_shigi_collision_list, smoke_mid_collision_list



class Decay_invaders:
    def __init__(self, window):
        self.window = window
        
        #initial positioning
        self.player_pos = 100
        self.float_x = 500
        self.shigi_pos = 100
        self.shigi_x = 500

        #extra detail
        self.player_h = 0
        self.animations = []
        self.first_bullet_x = 500

        #health bar initializations & logic
        self.image = pygame.Surface((40,40))
        self.image.fill((200,30,30))
        self.rect = self.image.get_rect(center = (400,400))
        self.current_health = 1000
        self.target_health = 1000
        self.max_health = 1000

        self.mid_current_health = 1000
        self.mid_target_health = 1000
        self.mid_max_health = 1000

        self.health_bar_length_mid = 350
        self.health_ratio_mid = self.mid_max_health / self.health_bar_length_mid

        self.health_bar_length = 350
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

        #This is one of my failed attempts, left because I might try to implement later
            #grid for bullet collisions, this is meant to segment objects so python doesn't have to do so many checks. 
            #The input will be [#number of list, x, y], this makes it easier to find the list when it comes to popping
            #I will put a conditional that once shigi is > 575, then if it is in list 1, pop and append in list 5. 2 is 6. 3 is 7. 4 is 8.
            #at the end it will just pop it out of 5,6,7, or 8, depending on if it is 1,2,3,4 
            #the temp get the indexes from the for loop of everthing that needs to be removed since it is more less than 175 or more than 1175
            #self.identifier is so that bullet_collision can change stuff in the orginal bullet list
        
        #bullet & collision initializations
        self.mid_regular_bullets = pygame.sprite.Group()
        self.shigi_regular_bullets = pygame.sprite.Group()
        self.smoke_screen = pygame.sprite.Group()
        self.speed = 15
        self.mid_damage = 50
        self.shigi_damage = 150
        self.bullets_class = Bullets()
        self.mid_col, self.shigi_col, self.shigi_smoke, self.mid_smoke = [], [], [], []
        self.identifier_mid = -1
        self.identifier_shigi = -1
        self.explosion = pygame.image.load("games\Decay Invaders\Items\explosions.png").convert_alpha()


        #power ups: initial img & amount of uses per game
        self.bwhip_image, self.blackwhip_number = pygame.image.load("games/Decay Invaders/Items/mid_powerups/blackwhip_icon.png").convert_alpha(), 1
        self.fa_jin, self.fa_jin_number = pygame.image.load("games/Decay Invaders/Items/mid_powerups/fa_jin_icon.png").convert_alpha(), 1
        self.float, self.float_number = pygame.image.load("games/Decay Invaders/Items/mid_powerups/float_icon.png").convert_alpha(), 1
        self.gearshift_icon, self.gearshift_number = pygame.image.load("games\Decay Invaders\Items\mid_powerups\gearshift_icon.png").convert_alpha(), 3
        self.smokescreen, self.smokescreen_number = pygame.image.load("games\Decay Invaders\Items\mid_powerups\smokescreen_icon.png").convert_alpha(), 4

        self.fa_jin_indicator = 0
        self.float_indicator = 0
        self.float_counter = 0
        self.smoke_counter = 0
        self.stop_running = False
        self.new_smoke = False
        self.blackwhip_completed = False

        #timers
        self.counter_mid = -1
        self.counter_shigi = -1
        self.song_counter = 0
        self.cooldown = 10
        self.gearshift_timer = 50
        self.subtractor = 0
        
    #updates health as bullet's hit players
    def get_damage(self,amount, person, shigi_amount):
        if person == "shigi": #shigi because it is saying when mid hits shigi, shigi gets damage.
            if self.target_health > 0:
                self.target_health -= amount
            if self.target_health <= 0:
                self.target_health = 0
                print(True)
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
        if person == "mid":
            if self.mid_target_health > 0:
                self.mid_target_health -= shigi_amount
            if self.mid_target_health <= 0:
                self.mid_target_health = 0
                print(False)
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()                

    #constantly updates health bars
    def update(self):
        self.advanced_health()
        self.advanced_health_mid()

    #constantly blits shigiraki's health through update()
    def advanced_health(self):
        target_health_width = int(self.target_health / self.health_ratio)
        red_bar = pygame.Rect(85, 61, target_health_width, 25)

        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            if self.current_health < self.target_health:
                self.current_health = self.target_health
            transition_width = int((self.current_health - self.target_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        current_health_width = int(self.current_health / self.health_ratio)
        transition_bar_start = min(target_health_width, current_health_width)
        transition_bar_width = abs(current_health_width - target_health_width)
        transition_bar = pygame.Rect(85 + transition_bar_start, 61, transition_bar_width, 25)

        pygame.draw.rect(self.window, (255, 0, 0), red_bar)
        if transition_width > 0:
            pygame.draw.rect(self.window, transition_color, transition_bar)
        pygame.draw.rect(self.window, (255, 255, 255), (85, 61, self.health_bar_length, 25), 4)	
    
    #constantly blits Midoriya's health through update()
    def advanced_health_mid(self):
        target_health_width = int(self.mid_target_health / self.health_ratio_mid)
        red_bar = pygame.Rect(565, 61, target_health_width, 25)

        transition_width = 0
        transition_color = (255, 0, 0)

        if self.mid_current_health > self.mid_target_health:
            self.mid_current_health -= self.health_change_speed
            if self.mid_current_health < self.mid_target_health:
                self.mid_current_health = self.mid_target_health
            transition_width = int((self.mid_current_health - self.mid_target_health) / self.health_ratio_mid)
            transition_color = (255, 255, 0)

        current_health_width = int(self.mid_current_health / self.health_ratio_mid)
        transition_bar_start = min(target_health_width, current_health_width)
        transition_bar_width = abs(current_health_width - target_health_width)
        transition_bar = pygame.Rect(565 + transition_bar_start, 61, transition_bar_width, 25)

        pygame.draw.rect(self.window, (255, 0, 0), red_bar)
        if transition_width > 0:
            pygame.draw.rect(self.window, transition_color, transition_bar)
        pygame.draw.rect(self.window, (255, 255, 255), (565, 61, self.health_bar_length_mid, 25), 4)	

    #blits frames of spritesheet depending on positioning & direction for both Mid and Shigi
    def get_image(self, sheet, frame, width, scale, player_place, flip,adjustment, who):
        player_w, self.player_h = sheet.get_size()
        player_w, self.player_h = player_w * scale, self.player_h * scale
        sheet = pygame.transform.scale(sheet, (player_w, self.player_h))
        if who == "mid":
            frac = (1/8)
        else:
            frac = (1/6)
        player_w = int(player_w * frac)
        if flip == False:
            if who == "mid":
                self.window.blit(sheet, (player_place, 1000 - (self.player_h + 20) + 175), ((frame * player_w) + adjustment,0, width, self.player_h))
            else: 
                self.window.blit(sheet, (player_place, 175), ((frame * player_w) + adjustment,0, width, self.player_h)) #shigi image
        else:
            flipped_image = pygame.transform.flip(sheet, True, False)
            if who == "mid":
                self.window.blit(flipped_image, (player_place, 1000 - (self.player_h + 20) + 175), ((frame * player_w) + adjustment,0, width, self.player_h))
            else:
                self.window.blit(flipped_image, (player_place, 175), ((frame * player_w) + adjustment,0, width, self.player_h))# shigi image

    #blits standing sprite for players
    def get_image_mid_stance(self, sheet, width, height, player_pos):
        sheet = pygame.transform.scale(sheet, (44, 100))
        self.window.blit(sheet, (player_pos - 29, 1000 - (height + 20) + 175), (0,0, width, height))
    def get_image_shigi_stance(self, sheet, width, height, player_pos):
        sheet = pygame.transform.scale(sheet, (58, 134))
        self.window.blit(sheet, (player_pos - 29, 175), (0,0, width, height))
    
    #intakes values regarding position and decides whether to blit running animation or stance and moves the player to inputted location
    def shigi_move(self, finger_x, finger_y, shigi_run_list,frame, player_stance):
        w, h = pygame.display.get_surface().get_size()
        #self.float_x = w - (finger_x * w)
        self.float_x = finger_x
        self.float_y = int(finger_y * h) + 175
        if self.float_x > 950:
            self.float_x = 950
        elif self.float_x < 10:
            self.float_x = 10
        if frame >= 6:
            frame = 0
        
        if self.shigi_pos == self.float_x:
            if self.float_x == 1000:
                self.get_image_shigi_stance(player_stance, 58, 134, 500)
            else:
                self.get_image_shigi_stance(player_stance, 58, 134, self.shigi_pos)

        elif self.shigi_pos < self.float_x: #moving right
            self.get_image(shigi_run_list, frame, 134, 2, self.shigi_pos, False, -6, "shigi")
            self.shigi_pos = self.float_x
            frame += 1
        elif self.shigi_pos > self.float_x: #moving left
            self.get_image(shigi_run_list, frame, 134, 2, self.shigi_pos, True, 10, "shigi")
            self.shigi_pos = self.float_x
            frame += 1
        return frame
    
    #intakes values regarding position and decides whether to blit running animation or stance and moves the player to inputted location
    def player_move(self, finger_x, finger_y, mid_run_list,frame, player_stance):
        w, h = pygame.display.get_surface().get_size()
        self.float_x = w - (finger_x * w)
        self.float_y = int(finger_y * h) + 175

        if self.float_x > 950:
            self.float_x = 950
        elif self.float_x < 10:
            self.float_x = 10

        if frame > 7:
            frame = 0
        
        if self.player_pos == self.float_x:
            if self.float_x == 1000:
                self.get_image_mid_stance(player_stance, 44, 100, 500)
            else:
                self.get_image_mid_stance(player_stance, 44, 100, self.player_pos)

        elif self.player_pos < self.float_x: #moving right
            self.get_image(mid_run_list, frame, 75, 2, self.player_pos, False, 15, "mid")
            self.player_pos = self.float_x
            frame += 1
        elif self.player_pos > self.float_x: #moving left
            self.get_image(mid_run_list, frame, 80, 2, self.player_pos, True, -5, "mid")
            self.player_pos = self.float_x
            frame += 1
        return frame, True, self.float_y

    #Dictates the movement of shigi
        #Would have been the AI if I had enough time to implement said AI for shigiraki
    def shigi_choice(self, time):
        if self.mid_regular_bullets and time == 0:
            for bullet in self.mid_regular_bullets:
                self.first_bullet_x = bullet.rect.x  
                break
        else:
            if time == 1:
                for bullet in self.mid_regular_bullets:
                    self.first_bullet_x = bullet.rect.x  
                    break
                if self.shigi_pos < self.first_bullet_x:
                    self.first_bullet_x -= self.first_bullet_x // 4
                else:
                    self.first_bullet_x += self.first_bullet_x // 4
            if time == 2:
                for bullet in self.mid_regular_bullets:
                    self.first_bullet_x = bullet.rect.x  
                    break
                if self.shigi_pos < self.first_bullet_x:
                    self.first_bullet_x = self.first_bullet_x // 2
                else:
                    self.first_bullet_x = self.first_bullet_x - (self.first_bullet_x // 2)
            
        return self.first_bullet_x

    #updates animations list that is neccessary for sprite animations to execute correctly
    def start_sprite_animation(self, x, y):
        self.animations.append((x, y, pygame.time.get_ticks(), 0))

    #draws the sprite animation for bullet colllisions
    def sprite_animations(self):
        SPRITE_WIDTH, SPRITE_HEIGHT = 64, 64
        SPRITES_PER_ROW = 8
        TOTAL_FRAMES = 32

        current_time = pygame.time.get_ticks()

        for animation in self.animations[:]:
            x, y, start_time, frame = animation

            if current_time - start_time > frame * 5:
                col = frame % SPRITES_PER_ROW
                row = frame // SPRITES_PER_ROW

                sprite_x = col * SPRITE_WIDTH
                sprite_y = row * SPRITE_HEIGHT

                self.window.blit(self.explosion, (x, y - 20), (sprite_x, sprite_y, SPRITE_WIDTH, SPRITE_HEIGHT))

                frame += 1
                if frame >= TOTAL_FRAMES:
                    self.animations.remove(animation)
                else:
                    self.animations[self.animations.index(animation)] = (x, y, start_time, frame)

    #collects the updates from check_collisions() function    
    def bullet_collisions(self):
        self.mid_col, self.shigi_col, self.shigi_smoke, self.mid_smoke = self.bullets_class.check_collisions(self.smoke_screen, self.mid_regular_bullets, self.shigi_regular_bullets)

    #Unless hindered by conditions such as Fa Jin, bullets accustomed to Bullets() requirements are shot every 2 seconds for mid and every 4 for shigi
        #Secondly every bullet is accounted for and if their position or collision status meets a certain condition then updates occur based on the collision   
    def shoot_projectile_mid(self, time, bullet_image, mid_shot_mask, who):
        if self.blackwhip_completed == True and self.stop_running == True:
            self.stop_running = False
        if self.fa_jin_indicator == 1 and who == "mid":
            time = 5
            self.fa_jin_indicator = 2

        if time == 0:
            if who == "mid":
                self.identifier_mid += 1
                if self.fa_jin_indicator == 2:
                    bullet_image = pygame.image.load("games\Decay Invaders\Items\mid_movement\power_shot.png").convert_alpha()
                    bullet = Bullets(self.player_pos, 1000 - (self.player_h + 10) + 175, 450, self.identifier_mid, bullet_image)
                    self.mid_regular_bullets.add(bullet)
                    self.fa_jin_indicator = 0
                else:
                    bullet = Bullets(self.player_pos, 1000 - (self.player_h + 10) + 175, 50, self.identifier_mid, bullet_image)
                    self.mid_regular_bullets.add(bullet)
                time = 2
            elif who == "shigi":
                self.identifier_shigi += 1
                bullet = Bullets(self.shigi_pos, 0 + 134 + 175, self.shigi_damage, self.identifier_shigi, bullet_image)
                self.shigi_regular_bullets.add(bullet)
                time = 4

        self.counter_mid = -1
        if who == "mid": #only need to have bullet collisions called on one of them. 
            for bullet in self.mid_regular_bullets:
                if bullet.identifier in self.mid_smoke:
                    bullet.image = pygame.transform.rotate(bullet.image, 180)
                    bullet.direction = -1 #makes the image start going backward
                    self.mid_smoke.remove(bullet.identifier)
                bullet.update(self.speed)
                if bullet.rect.y < 175:
                    bullet.kill()
                    self.get_damage(bullet.damage, "shigi", self.mid_damage)
                if bullet.rect.y > 1175:
                    bullet.kill()
                    self.get_damage(bullet.damage, "mid", self.mid_damage)
                if bullet.identifier in self.mid_col:
                    if self.float_indicator == 0:
                        bullet.damage -= 150
                        if bullet.damage < 1:
                            self.start_sprite_animation(bullet.rect.x, bullet.rect.y)
                            bullet.kill()
                    else:
                        self.mid_col.remove(bullet.identifier)
                        self.shigi_col.clear()
                        if self.float_counter <= 0:
                            self.float_indicator = 0
                self.window.blit(bullet.image, bullet.rect)

        if who == "shigi":
            for bullet in self.shigi_regular_bullets:
                if bullet.identifier in self.shigi_smoke:
                    bullet.image = pygame.transform.rotate(bullet.image, 180)
                    bullet.direction = -1 #makes the image start going backward
                    self.shigi_smoke.remove(bullet.identifier)
                bullet.update(-10)
                if bullet.rect.y > 1175:
                    bullet.kill()
                    self.get_damage(bullet.damage, "mid", bullet.damage)
                
                if bullet.rect.y < 175:
                    bullet.kill()
                    self.get_damage(bullet.damage, "shigi", bullet.damage)
                if bullet.identifier in self.shigi_col:
                    bullet.damage -= 50
                    if bullet.damage < 1:
                        bullet.kill()
                self.window.blit(bullet.image, bullet.rect)
        return time
    
    #power ups

    #essentially briefly stops the game and removes all bullets
    def blackwhip_function(self, func_image):
        self.stop_running = True
        #functionality
        self.mid_regular_bullets.empty()
        self.shigi_regular_bullets.empty()
        self.blackwhip_completed = True 

    #randomly blits smoke and adds it to the bullets class
    def smoke_function(self, image):
        if self.new_smoke == True:
            x = random.randrange(0,733)
            y = random.randrange(300,800)
            smoke = Bullets(x,y,0,0,image)
            self.smoke_screen.add(smoke)
            self.new_smoke = False
        for i in self.smoke_screen:
            self.window.blit(i.image, i.rect)
        
    #Blits all the button and dictates powers ups: Fa Jin, Float, Gearshift, Smokescreen slightly
    def mid_power_ups(self, x, player_y):
        x = 1000 - (x * 1000)
        player_y = player_y - 175
        #blits
        self.window.blit(self.bwhip_image, (0, 1175))
        self.window.blit(self.fa_jin, (200, 1175))
        self.window.blit(self.float, (400, 1175))
        self.window.blit(self.gearshift_icon, (600, 1175))
        self.window.blit(self.smokescreen, (800, 1175))
        if self.cooldown > 0:
            self.cooldown -= 1
        self.gearshift_timer -= self.subtractor
        if self.gearshift_timer < 1:
            self.gearshift_timer = 50
            self.speed = 10
            self.subtractor = 0

        if x < 200 and self.blackwhip_number > 0 and player_y > 1185  and self.cooldown == 0:
            self.blackwhip_number -= 1
            if self.cooldown == 0:
                self.cooldown = 5
            self.bwhip_image= pygame.image.load("games/Decay Invaders/Items/mid_powerups/blackwhip_bw.png").convert_alpha()
            self.blackwhip_midoriya= pygame.image.load("games\Decay Invaders\Items\mid_movement\midoriya_blackwhip.png").convert_alpha()
            self.blackwhip_function(self.blackwhip_midoriya)
        elif 200 < x < 400 and self.fa_jin_number > 0  and player_y > 1185  and self.cooldown == 0:
            self.fa_jin_number -= 1
            if self.cooldown == 0:
                self.cooldown = 5
            self.fa_jin = pygame.image.load("games/Decay Invaders/Items/mid_powerups/fa_jin_bw.png").convert_alpha()
            self.fa_jin_indicator = 1
        elif 400 < x < 600 and self.float_number > 0  and player_y > 1185  and self.cooldown == 0:
            self.float_number -= 1
            if self.cooldown == 0:
                self.cooldown = 5
            self.float = pygame.image.load("games/Decay Invaders/Items/mid_powerups/float_bw.png").convert_alpha()
            self.float_indicator = 1
            self.float_counter = 7
        elif 600 < x < 800 and self.gearshift_number > 0  and player_y > 1185  and self.cooldown == 0:
            self.gearshift_number -= 1
            if self.cooldown == 0:
                self.cooldown = 5
            if self.gearshift_number == 0:
                self.gearshift_icon = pygame.image.load("games/Decay Invaders/Items/mid_powerups/gearshift_bw.png").convert_alpha()
            if self.gearshift_timer > 0:
                self.speed = 20
                self.subtractor = 1


        elif 800 < x < 1000 and self.smokescreen_number > 0  and player_y > 1185 and self.cooldown == 0:
            self.smokescreen_number -= 1
            if self.cooldown == 0:
                self.cooldown = 5
            if self.smokescreen_number == 0:
                self.smokescreen = pygame.image.load("games/Decay Invaders/Items/mid_powerups/smokescreen_bw.png").convert_alpha()
            self.smoke_counter = 12
            self.new_smoke = True