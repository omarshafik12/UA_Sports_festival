import sys, time, random, pygame, os, math, cv2
from pathlib import Path

#webcam_input import
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
setup = Prerequisites(1500,1070)
w, h = pygame.display.get_surface().get_size()

class hole_in_the_wall():
    def __init__(self):
        pass

    #for each drawn point by Mediapipe, this function checks each point to see if it is on the image
    def collision(self, l_0, l_1,mask_image):
        if l_0 == [] and l_1 ==[]:
            return False
    
        for i in l_0:
            x = w-(w * i[0])
            y = h * i[1]
            is_on_mask = mask_image.get_at((x, y))
            if is_on_mask:
                return False

        if l_1 == []:
            return True
        else:
            for i in l_1:
                x = w * i[0]
                y = h * i[1]
                is_on_mask = mask_image.get_at((x, y))
                if is_on_mask:
                    return False
        return True




def main(window):
    hitw = hole_in_the_wall()
    clock = pygame.time.Clock()
    item_number = 1
    initial_wall = pygame.image.load(f"games/Hole in the Wall/Items/icon-{str(item_number)}.png").convert_alpha()
    wall_rect = initial_wall.get_rect(center=(w//2, h//2))
    wall_mask = pygame.mask.from_surface(initial_wall)
    setup.hands = setup.mp_hands.Hands(max_num_hands=2)

    counter, text = 10, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 60)

    #background music
    pygame.mixer.music.load("games/Hole in the Wall/Background/My Hero Academia OST - MightU.mp3")
    pygame.mixer.music.play(-1,0,0)

    while True:
        #exiting the game
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: 
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'boom!'
            if event.type == pygame.QUIT:
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
        if item_number == 3:
            setup.webcam_ai(setup.hands, max_hands = 2, capture = False)
        else:
            setup.webcam_ai(setup.hands, max_hands = 1, capture = False)
        pygame.surfarray.blit_array(setup.screen, setup.img)

        #window.blit(initial_wall, wall_rect)
        window.blit(initial_wall, wall_rect)
        window.blit(font.render(text, True, (255, 255, 255)), (w//2, h-100))
        
        #once the counter reaches zero, it checks for collision and depending on result, it goes to the next level, it then restarts the counter
        if counter == 0:
            if item_number == 3:
                setup.webcam_ai(setup.hands, max_hands = 2, capture = True)
            else:
                setup.webcam_ai(setup.hands, max_hands = 1, capture = True)
            result = hitw.collision(setup.l_0, setup.l_1, wall_mask)
            if result:
                item_number += 1
                if item_number == 5:
                    print(True)
                    setup.webcam.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                initial_wall = pygame.image.load(f"games/Hole in the Wall/Items/icon-{str(item_number)}.png").convert_alpha()
                wall_rect = initial_wall.get_rect(center=(w//2, h//2))
                wall_mask = pygame.mask.from_surface(initial_wall)
                counter, text = 10, '10'.rjust(3)
            
            else:
                print(False)
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                break
            

        pygame.display.update()
        pygame.display.flip()

if __name__ == "__main__":
    main(setup.screen)
