import sys, time, random, pygame, os, math, cv2
import numpy as np
from pathlib import Path
from decay_invaders_mechanics import Decay_invaders

#webcam_input import
file_path = Path('webcam_input.py').absolute()

sys.path.append(file_path.parent.as_posix())

try:
    from webcam_input import Prerequisites
except ModuleNotFoundError as e:
    print(f"Error: {e}")


#initilization
pygame.init()
pygame.display.set_caption("Kirishima VS Midoriya")
FPS = 60
setup = Prerequisites(1000,1375)
        

def main(window):
    #game mechanics initialization
    game_mechanics = Decay_invaders(window)
    clock = pygame.time.Clock()


    #player/shigi stance
    player_stance = pygame.image.load("games\Decay Invaders\Items\mid_movement\mid_stance.png").convert_alpha()


    shigi_stance = pygame.image.load("games/Decay Invaders/Items/shigi_movement/shigi_stance.png").convert_alpha()

    #player movement initialization
    player_run = pygame.image.load("games\Decay Invaders\Items\mid_movement\mid_run.png").convert_alpha()
    frame = 0
    shigi_frame = 0

    shigi_run = pygame.image.load("games\Decay Invaders\Items\shigi_movement\shigi_run.png").convert_alpha()

    #game items
    smokescreen = pygame.image.load("games\Decay Invaders\Items\mid_movement\mid_cloud.png").convert_alpha()
    mid_power_shot = pygame.image.load("games\Decay Invaders\Items\mid_movement\mid_power_shot.png").convert_alpha()
    mid_shot = pygame.image.load("games\Decay Invaders\Items\mid_movement\mid_shot.png").convert_alpha()
    mid_shot = pygame.transform.rotate(mid_shot, 90)
    mid_shot_mask = pygame.mask.from_surface(mid_shot)

    shigi_shot = pygame.image.load("games\Decay Invaders\Items\shigi_movement\shigi_hands.png").convert_alpha()
    shigi_shot = pygame.transform.scale(shigi_shot, (75, 57))
    shigi_shot = pygame.transform.rotate(shigi_shot, 90)
    shigi_shot_mask = pygame.mask.from_surface(shigi_shot)

    shigi_face = pygame.image.load("games\Decay Invaders\Items\shigi_face.png").convert_alpha()
    shigi_face = pygame.transform.scale(shigi_face, (100, 148))
    shigi_face_frame = shigi_face.get_rect(topleft= (0,0))


    mid_face = pygame.image.load("games\Decay Invaders\Items\mid_face.png").convert_alpha()
    mid_face = pygame.transform.scale(mid_face, (173, 115))
    mid_face_frame = mid_face.get_rect(topleft= (850,21))
    level_start = False
    
    #background music
    bm_songs = [
        "games\Decay Invaders\Background\MY HEROACADEMIA 6th season ED.mp3",
        "games\Decay Invaders\Background\My Heroacademia 7th season Ending Movie.mp3",
        "games\Decay Invaders\Background\My Hero Academia OST - You Say Run  Jet Set Run (You Say Run v2).mp3"
    ]
    bm_counter = 0
    music_changer = 1
    song = pygame.mixer.Sound(bm_songs[bm_counter])
    game_mechanics.song_counter = song.get_length()

    pygame.mixer.music.load(bm_songs[bm_counter])
    pygame.mixer.music.play(0,0,0)

    setup.hands = setup.mp_hands.Hands(max_num_hands=1)
    
    #timer initialization
    game_mechanics.float_counter = 0
    game_mechanics.smoke_counter = 0
    counter_mid = 2
    counter_shigi = 4
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: 
                counter_mid -= 1
                counter_shigi -= 1
                game_mechanics.song_counter -= 1
                game_mechanics.float_counter -= 1
                game_mechanics.smoke_counter -= 1
            if event.type == pygame.QUIT:
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        #OpenCV & Mediapipe utilization with reconfig of surfarray to suit requirements
        setup.webcam_ai(setup.hands, max_hands = 1)
        pygame.surfarray.blit_array(setup.screen, setup.img)

        #running game mechanisms & features
        if level_start == False:
            game_mechanics.get_image_shigi_stance(shigi_stance, 58, 134, 500)
            pass
        if game_mechanics.stop_running == False:
            frame, level_start, player_y = game_mechanics.player_move(setup.x, setup.y, player_run, frame, player_stance)
            shigi_frame = game_mechanics.shigi_move(game_mechanics.shigi_choice(counter_shigi), setup.y, shigi_run,shigi_frame, shigi_stance)
        else:
            counter_mid = 2
            counter_shigi = 4
        counter_mid = game_mechanics.shoot_projectile_mid(counter_mid, mid_shot, mid_shot_mask, "mid")
        counter_shigi = game_mechanics.shoot_projectile_mid(counter_shigi, shigi_shot, shigi_shot_mask, "shigi")
        game_mechanics.sprite_animations()
        game_mechanics.mid_power_ups(setup.x, player_y)
        game_mechanics.bullet_collisions()
        game_mechanics.update()
        if game_mechanics.smoke_counter >=1:
            game_mechanics.smoke_function(smokescreen)
        else:
            game_mechanics.smoke_screen.empty()
        
        #song changning logic, dictated by a timer counting down the song length
        if game_mechanics.song_counter <= 0:
            bm_counter += music_changer
            if bm_counter == 0:
                music_changer = 1
            elif bm_counter == 3:
                bm_counter = 2
                music_changer = -1
            song = pygame.mixer.Sound(bm_songs[bm_counter])
            if bm_counter == 2:
                game_mechanics.song_counter = song.get_length()
            else:
                game_mechanics.song_counter = song.get_length()
            pygame.mixer.music.load(bm_songs[bm_counter])
            pygame.mixer.music.play(0, 0, 0)
            

        window.blit(shigi_face, shigi_face_frame)
        window.blit(mid_face, mid_face_frame)

        pygame.display.update()
        pygame.display.flip()

if __name__ == "__main__":
    main(setup.screen)