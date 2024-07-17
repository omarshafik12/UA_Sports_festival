import numpy as np
import sys, time, random, pygame, os, math, cv2, random
from pathlib import Path
from drop_off_mechanics import Drop_off

#webcam_input import
file_path = Path('webcam_input.py').absolute()

sys.path.append(file_path.parent.as_posix())

try:
    from webcam_input import Prerequisites
except ModuleNotFoundError as e:
    print(f"Error: {e}")


pygame.init()
pygame.display.set_caption("Yaoyorozu VS Midoriya")
FPS = 60
clock = pygame.time.Clock()
setup = Prerequisites(1000,1000)

def main(window):
    game_mechanics = Drop_off(window)
    clock = pygame.time.Clock()

    #drop_off_items
    game_mechanics.generate_items()

    #player/shigi stance
    player_stance = pygame.image.load("games\Decay Invaders\Items\mid_movement\mid_stance.png").convert_alpha()


    shigi_stance = pygame.image.load("games\Drop Off\Items\momo_character.png").convert_alpha()

    #player/shigi run
    player_run = pygame.image.load("games\Decay Invaders\Items\mid_movement\mid_run.png").convert_alpha()
    frame = 0

    
    #background music
    bm_songs = [
        "games\Decay Invaders\Background\MY HEROACADEMIA 6th season ED.mp3",
    ]

    pygame.mixer.music.load(bm_songs[0])
    pygame.mixer.music.play(-1,0,0)

    setup.hands = setup.mp_hands.Hands(max_num_hands=1)

    #Game timer
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    counter_momo = 150

    counter, text = 150, '150'.rjust(3)
    font = pygame.font.SysFont('Consolas', 40)


    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: 
                counter_momo -= 1
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'Win'
            if event.type == pygame.QUIT:
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        #OpenCV & Mediapipe utilization with reconfig of surfarray to suit requirements
        setup.webcam_ai(setup.hands, max_hands = 1)
        pygame.surfarray.blit_array(setup.screen, setup.img)
        
        #Running game Mechanics
        frame, level_start, player_x, player_mask,sub_rect, text_x = game_mechanics.player_move(window, setup.x, setup.y, player_run, frame, player_stance)
        window.blit(font.render(text, True, (255, 255, 255)), (text_x - 10, 960))
        counter_momo = game_mechanics.shoot_projectile_mid(counter_momo,player_x, player_mask, sub_rect, shigi_stance)
        game_mechanics.creation_animation()

        
        pygame.display.update()
        pygame.display.flip()

if __name__ == "__main__":
    main(setup.screen)