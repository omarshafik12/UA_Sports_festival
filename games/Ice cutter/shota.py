import sys, time, random, pygame, os, math, cv2
import numpy as np
from pathlib import Path
from ice_cutter_mechanics import Squid_game_mechanics

# Webcam input import
file_path = Path('webcam_input.py').absolute()

sys.path.append(file_path.parent.as_posix())

try:
    from webcam_input import Prerequisites
except ModuleNotFoundError as e:
    print(f"Error: {e}")

pygame.init()
pygame.display.set_caption("Ice Cutter")
FPS = 60
clock = pygame.time.Clock()
setup = Prerequisites(1000, 1000)
cookie = pygame.image.load("games/Ice cutter/Background/ice_back.png").convert_alpha()
cookie = pygame.transform.scale(cookie, (500, 500))
w, h = pygame.display.get_surface().get_size()
cookie_rect = cookie.get_rect(center=(w//2, h//2))

# Player creation
col = (255, 0, 0)
player = pygame.Surface((20, 20))
player.fill(col)
player_frame = player.get_rect(center=(0, 0))
player_mask = pygame.mask.from_surface(player)
player_mask_frame = player_mask.get_rect()

#Switches between each cookie
def load_new_item(item_number):
    pygame.mixer.music.pause()
    if item_number == 11:
        item_path = "games/Ice cutter/Items/icon_bonus.png"
    else:
        item_path = f"games/Ice cutter/Items/icon-{str(item_number)}.png"
    
    cookie_drawing = pygame.image.load(item_path).convert_alpha()
    cookie_drawing = pygame.transform.scale(cookie_drawing, (300, 300))
    cookie_drawing_rect = cookie_drawing.get_rect(center=(w // 2, h // 2))
    cookie_mask = pygame.mask.from_surface(cookie_drawing)
    cookie_mask_rect = cookie_drawing.get_rect(center=(w // 2, h // 2))

    return cookie_drawing, cookie_drawing_rect, cookie_mask, cookie_mask_rect


def main(window):
    clock = pygame.time.Clock()
    item_number = 1
    cookie_drawing, cookie_drawing_rect, cookie_mask, cookie_mask_rect = load_new_item(item_number)
    game_mechanics = Squid_game_mechanics(window, cookie_mask, player, player_frame, player_mask_frame)
    level_start = True

    # Background music
    bm_songs = [
        "games/Ice cutter/Background/My Hero Academia - Opening 6  Polaris.mp3",
        "games/Ice cutter/Background/My Hero Academia Season 6 - Ending 2  North Wind  SIX LOUNGE.mp3",
        "games/Ice cutter/Background/My Hero Academia Season 6 - Opening 2  Bokurano.mp3",
        "games/Ice cutter/Background/My Hero Academia Season 7 (OP 12) TV SIZE誰我為 Tagatame僕のヒーローアカデミア (COVER).mp3"
    ]
    bm_counter = 0
    music_changer = 1
    setup.hands = setup.mp_hands.Hands(max_num_hands=1)

    pygame.mixer.music.load(bm_songs[bm_counter])
    pygame.mixer.music.play(0, 0, 0)

    wait_counter = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    game_status = False

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if wait_counter > 0:
                    wait_counter -= 1
            if event.type == pygame.QUIT:
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        # Webcam and display config
        setup.webcam_ai(setup.hands, max_hands=1)
        pygame.surfarray.blit_array(setup.screen, setup.img)

        # Initial blits
        window.blit(cookie, cookie_rect)
        window.blit(cookie_drawing, cookie_drawing_rect)

        # Move player and check collisions only if wait_counter is 0
        if wait_counter == 0:
            game_mechanics.move_draw(w, h, setup.x, setup.y)
            if game_status == False:
                game_mechanics.lines.clear()

            game_status = game_mechanics.check_collision(player_mask, cookie_mask_rect)

            # Draw lines and circles
            for points in game_mechanics.lines:
                if len(points) > 1:
                    pygame.draw.lines(setup.screen, (3, 252, 252), False, points, 20)
                    for p in points:
                        pygame.draw.circle(setup.screen, (3, 252, 252), p, 10)

            if game_status:
                pygame.mixer.music.unpause()
                level_start = False
        else:
            game_mechanics.move_draw(w, h, setup.x, setup.y)

        if level_start == False and wait_counter == 0:
            sub = game_mechanics.grab_screen(350, 350, 300, 300, window)
            if sub:
                item_number += 1
                game_mechanics.lines.clear()
                wait_counter = 3  #Setting the wait counter for 3 seconds

                if item_number == 12:
                    print(True)
                    setup.webcam.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                else:
                    cookie_drawing, cookie_drawing_rect, cookie_mask, cookie_mask_rect = load_new_item(item_number)
                    game_mechanics.cookie_mask = cookie_mask

                # Music alternator
                if bm_counter == 0:
                    music_changer = 1
                elif bm_counter == len(bm_songs) - 1:
                    music_changer = -1
                bm_counter += music_changer
                pygame.mixer.music.load(bm_songs[bm_counter])
                pygame.mixer.music.play(0, 0, 0)
                level_start = True

            if game_mechanics.check_collision(player_mask, cookie_mask_rect) == False and len(game_mechanics.lines) > 1:
                print(False)
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                break
        if wait_counter > 0:
            level_start = True
            game_mechanics.lines.clear()
            game_status == False

        pygame.display.update()
        pygame.display.flip()


if __name__ == "__main__":
    main(setup.screen)
