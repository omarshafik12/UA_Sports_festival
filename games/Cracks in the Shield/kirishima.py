import sys, time, random, pygame, os, math, cv2
import numpy as np
from pathlib import Path
from cracks_in_the_shield_mechanics import Cracks_in_the_shield

# webcam_input import
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
setup = Prerequisites(1000,1000)


def main(window):
    clock = pygame.time.Clock()
    w, h = pygame.display.get_surface().get_size()

    #player
    player = pygame.image.load("games\Cracks in the Shield\Items\midoriya_arm.png").convert_alpha()
    player = pygame.transform.scale(player, (200, 200))
    player_frame = player.get_rect(center = ((w//2) + 250,h//2))
    player_mask = pygame.mask.from_surface(player)
    player_mask_frame = player_mask.get_rect()

    game_mechanics = Cracks_in_the_shield(window, player, player_frame, player_mask_frame)

    kirishima_stage_1 = pygame.image.load("games\Cracks in the Shield\Items\kirishima_stage_1.webp").convert_alpha()
    kirishima_stage_1 = pygame.transform.scale(kirishima_stage_1, (603, 876)) #(700,700)

    stage_1_list = game_mechanics.weak_point_generation(kirishima_stage_1, 5, 603, 876, 200,50)


    kirishima_stage_2 = pygame.image.load("games\Cracks in the Shield\Items\kirishima_stage_2.webp").convert_alpha()
    kirishima_stage_2 = pygame.transform.scale(kirishima_stage_2, (461, 790)) #(700,700)

    stage_2_list = game_mechanics.weak_point_generation(kirishima_stage_2, 10, 603, 876, 275,75)

    kirishima_stage_3 = pygame.image.load("games\Cracks in the Shield\Items\kirishima_stage_3.png").convert_alpha()
    kirishima_stage_3 = pygame.transform.scale(kirishima_stage_3, (700, 700)) #(700,700)

    stage_3_list = game_mechanics.weak_point_generation(kirishima_stage_3, 15, 700, 700, 175,150)

    weak_point = pygame.image.load("games\Cracks in the Shield\Items\weak_point.png").convert_alpha()
    weak_point = pygame.transform.scale(weak_point, (51, 50)) #(700,700)
    weak_point_mask = pygame.mask.from_surface(weak_point)

    level = 0
    new = True
    
    #background music
    bm_songs = [
        "games/Cracks in the Shield/Sound/My Hero Academia - Official Opening.mp3"
    ]

    setup.hands = setup.mp_hands.Hands(max_num_hands=1)

    pygame.mixer.music.load(bm_songs[0])
    pygame.mixer.music.play(-1,0,0)
    counter = 10
    point_counter = 0

    COUNTER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(COUNTER_EVENT, 1000)

    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == COUNTER_EVENT: 
                counter -= 1
            if event.type == pygame.QUIT:
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()


        setup.webcam_ai(setup.hands, max_hands = 1)
        pygame.surfarray.blit_array(setup.screen, setup.img)

        if level == 0:
            window.blit(kirishima_stage_1, (200,50))
            if point_counter != 4:
                if new == True:#runs code for new point
                    weak_point_mask_frame = weak_point.get_rect(center = stage_1_list[point_counter])
                    #window.blit(weak_point, weak_point_mask_frame)
                    counter = 7
                    new = False
                window.blit(weak_point, weak_point_mask_frame)
                if new == False: 
                    result = game_mechanics.collision(player_mask, weak_point_mask, player_frame, weak_point_mask_frame)
                    if result == True and counter > 0:
                        new = True
                        point_counter += 1
                    elif counter <= 0:
                        level = -1
            else:
                level += 1
                point_counter = 0


        elif level == 1:
            window.blit(kirishima_stage_2, (275,75))
            if point_counter != 9:
                if new == True:#runs code for new point
                    weak_point_mask_frame = weak_point.get_rect(center = stage_2_list[point_counter])
                    #window.blit(weak_point, weak_point_mask_frame)
                    counter = 4
                    new = False
                window.blit(weak_point, weak_point_mask_frame)
                if new == False: 
                    result = game_mechanics.collision(player_mask, weak_point_mask, player_frame, weak_point_mask_frame)
                    if result == True and counter > 0:
                        new = True
                        point_counter += 1
                    elif counter <= 0:
                        level = -1
                    else:
                        pass
            else:
                level += 1
                point_counter = 0
        
        
        elif level == 2: 
            window.blit(kirishima_stage_3, (175,150))
            if point_counter != 14:
                if new == True:#runs code for new point
                    weak_point_mask_frame = weak_point.get_rect(center = stage_3_list[point_counter])
                    #window.blit(weak_point, weak_point_mask_frame)
                    counter = 2
                    new = False
                window.blit(weak_point, weak_point_mask_frame)
                if new == False: 
                    result = game_mechanics.collision(player_mask, weak_point_mask, player_frame, weak_point_mask_frame)
                    if result == True and counter > 0:
                        new = True
                        point_counter += 1
                    elif counter <= 0:
                        level = -1
                    else:
                        pass
            else:
                level += 1
                point_counter = 0
        
        elif level == 3:
            print(True)
            setup.webcam.release()
            cv2.destroyAllWindows()
            pygame.quit()

        elif level == -1:
            print(False)
            setup.webcam.release()
            cv2.destroyAllWindows()
            pygame.quit()
        

        game_mechanics.move_draw(w, h, setup.x, setup.y)
        game_mechanics.rotate_player_movement(player, player_frame)



        pygame.display.update()
        pygame.display.flip()

if __name__ == "__main__":
    main(setup.screen)
