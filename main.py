import numpy as np
import sys, time, random, pygame, os, math, cv2, random, subprocess
from webcam_input import Prerequisites
from moviepy.editor import VideoFileClip
import mediapipe as mp




pygame.init()
pygame.display.set_caption("The UA Sports Festival")
FPS = 60
intro_vid_fps = 30
clock = pygame.time.Clock()
setup = Prerequisites(1565,1000)

class Menu_Functions():
    def __init__(self,window):
        self.setup_x = None
        self.setup_y = None
        self.font = pygame.font.SysFont("arialblack", 40)
        self.text_col = (255,255,255)
        self.reinitialize_camera = False

        self.box_color = (0,0,0)

        #game intro
        self.clip = VideoFileClip("menu\items\sports festival opener.mp4")
        self.stop_trailer = False


        # play_page
        self.hole_in_wall_result,self.cracks_in_the_shield_result,self.ice_cutter_result,self.air_hockey_result, self.drop_off_result, self.decay_invaders_result = False, False, False, False, False, False
        self.games = [
            pygame.image.load("menu/items/Tokoyami_game.jpg").convert_alpha(),
            pygame.image.load("menu/items/kirishima_game.jpg").convert_alpha(),
            pygame.image.load("menu/items/todoroki_game.jpg").convert_alpha(),
            pygame.image.load("menu/items/bakugo_game.jpg").convert_alpha(),
            pygame.image.load("menu/items/momo_game.png").convert_alpha(),
            pygame.image.load("menu/items/my-hero-academia-season-6-villains-shigaraki-anime-characters.png").convert_alpha()
        ]

        for i in range(6):
            self.games[i] = pygame.transform.scale(self.games[i], (400, 350))

        self.games_played = [
            pygame.image.load("menu/items/games_played/Tokoyami_game.png").convert_alpha(),
            pygame.image.load("menu/items/games_played/kirishima_game.png").convert_alpha(),
            pygame.image.load("menu/items/games_played/todoroki_game.png").convert_alpha(),
            pygame.image.load("menu/items/games_played/bakugo_game.png").convert_alpha(),
            pygame.image.load("menu/items/games_played/momo_game.png").convert_alpha(),
            pygame.image.load("menu/items/games_played/my-hero-academia-season-6-villains-shigaraki-anime-characters.png").convert_alpha()
        ]

        for i in range(6):
            self.games_played[i] = pygame.transform.scale(self.games_played[i], (400, 350))

        #how_to page
        self.how_to_selector_temp = 0
        self.how_to_selector = 0
        self.how_to_images = [
            pygame.image.load("menu/how_to/how_to_images/tokoyami.jpg").convert_alpha(),
            pygame.image.load("menu\how_to\how_to_images\kiri.jpg").convert_alpha(),
            pygame.image.load("menu/how_to/how_to_images/todoroki.png").convert_alpha(),
            pygame.image.load("menu/buttons/button-5.png").convert_alpha(),
            pygame.image.load("menu\how_to\how_to_images\momo.jpg").convert_alpha(),
            pygame.image.load("menu\how_to\how_to_images\shigi_how_to.png").convert_alpha()
        ]

        for i in range(6):
            self.how_to_images[i] = pygame.transform.scale(self.how_to_images[i], (904, 665))

        self.how_to_text = [
            pygame.image.load("menu/how_to/how_to_text/tokoyami_text.png").convert_alpha(),
            pygame.image.load("menu/how_to/how_to_text/Kirishima_text.png").convert_alpha(),
            pygame.image.load("menu/how_to/how_to_text/todoroki_text.png").convert_alpha(),
            pygame.image.load("menu/how_to/how_to_text/Bakugo_text.png").convert_alpha(),
            pygame.image.load("menu/how_to/how_to_text/Momo_text.png").convert_alpha(),
            pygame.image.load("menu/how_to/how_to_text/shigi_text.png").convert_alpha()
        ]



    def draw_text(self, text, font, text_col, x,y):
        img = font.render(text, True, text_col)
        setup.screen.blit(img, (x,y))
    
    def game_trailer(self, x, y, t, srf=None):
        frame = self.clip.get_frame(t=t)

        frame = cv2.resize(frame, (1565, 1000))

        if x != None and y != None:
            self.setup_x = 1565 - (x * 1565)
            self.setup_y = int(y * 1000) 
        else:
            if self.setup_x != None:
                if 1215 < self.setup_x < 1535 and 875 < self.setup_y < 975:
                    return 0

        if srf is None:
            return pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        else:
            pygame.surfarray.blit_array(srf, frame.swapaxes(0, 1))
            return srf
    
    def home_page(self, x, y): 
        background_1 = pygame.image.load("menu/items/bg-4.png").convert_alpha()
        background_1 = pygame.transform.scale(background_1, (1565, 1000))

        mha_logo = pygame.image.load("menu\items\logo.png").convert_alpha()
        mha_logo = pygame.transform.scale(mha_logo, (184, 83))

        button_1 = pygame.image.load("menu/buttons/button-1.jpg").convert_alpha()
        button_1 = pygame.transform.scale(button_1, (522, 200))

        button_2 = pygame.image.load("menu/buttons/button-3.jpg").convert_alpha()
        button_2 = pygame.transform.scale(button_2, (522, 200))

        button_3 = pygame.image.load("menu/buttons/button-4.jpg").convert_alpha()
        button_3 = pygame.transform.scale(button_3, (522, 200))

        button_4 = pygame.image.load("menu/buttons/button-9.jpg").convert_alpha()
        button_4 = pygame.transform.scale(button_4, (522, 200))

        charac_1 = pygame.image.load("menu\characters\All_Might_standing.webp").convert_alpha()

        charac_2 = pygame.image.load("menu\characters\mid_1.webp").convert_alpha()
        #text definition
        setup.screen.blit(background_1, (0,0))
        setup.screen.blit(mha_logo, (690, 50))
        setup.screen.blit(button_1, (522,200))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(522,200, 522, 200),  5)
        self.draw_text("Play", self.font, self.text_col,725,260)
        setup.screen.blit(button_2, (522,450))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(522,450, 522, 200),  5)
        self.draw_text("How To", self.font, self.text_col,690,510)
        setup.screen.blit(button_3, (522,700))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(522,700, 522, 200),  5)
        self.draw_text("Quit", self.font, self.text_col, 737, 760)
        setup.screen.blit(charac_1, (50,200))
        setup.screen.blit(charac_2, (1100,200))

        #alter this based on game.
        if x != None and y != None:
            self.setup_x = 1565 - (x * 1565)
            self.setup_y = int(y * 1000) 
        else:
            if 522 < self.setup_x < 1044 and 200 < self.setup_y < 400:
                return 1, True
            elif 522 < self.setup_x < 1044 and 450 < self.setup_y < 650:
                return 2, False
            elif 522 < self.setup_x < 1044 and 700 < self.setup_y < 900:
                return 3, False
        
        return 0, False
    
    def play_page(self, x, y, timer_interval):
        background_1 = pygame.image.load("menu/items/bg-2.png").convert_alpha()
        background_1 = pygame.transform.scale(background_1, (1565, 1000))
        setup.screen.blit(background_1, (0,0))
        if self.hole_in_wall_result == False:
            setup.screen.blit(self.games[0], (133, 150))
        else:
            setup.screen.blit(self.games_played[0], (133, 150))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(133, 150, 400, 350),  5)

        if self.cracks_in_the_shield_result == False:
            setup.screen.blit(self.games[1], (583,150))
        else:
            setup.screen.blit(self.games_played[1], (583,150))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(583,150, 400, 350),  5)

        if self.ice_cutter_result == False:
            setup.screen.blit(self.games[2], (1033,150))
        else:
            setup.screen.blit(self.games_played[2], (1033,150))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(1033,150, 400, 350),  5)
        #self.draw_text("Quit", self.font, self.box_color, 652, 750)
        if self.drop_off_result == False:
            setup.screen.blit(self.games[4], (333,600))
        else:
            setup.screen.blit(self.games_played[4], (333,600))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(333,600, 400, 350),  5)
        if self.decay_invaders_result == False:
            setup.screen.blit(self.games[5], (783,600))
        else:
            setup.screen.blit(self.games_played[5], (783,600))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(783,600, 400, 350),  5)
        self.draw_text("Hole in the wall", self.font, self.text_col,153,285)
        self.draw_text("Cracks in the Shield", pygame.font.SysFont("arialblack", 30), self.text_col,620,289)
        self.draw_text("Ice Cutter", self.font, self.text_col,1133,285)
        self.draw_text("Drop Off", self.font, self.text_col,433,735)
        self.draw_text("Decay Invaders", self.font, self.text_col,820,735)
        self.draw_text("Make a fist outside the boxes to return Home", self.font, self.text_col,300,50)
        
        if x != None and y != None:
            self.setup_x = 1565 - (x * 1565)
            self.setup_y = int(y * 1000) 
        else:
            if 133 < self.setup_x < 533 and 150 < self.setup_y < 500:
                pygame.mixer.music.pause()
                clock.tick_busy_loop(0)

                # Release resources that might interfere with subprocess
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.display.quit()
                self.hole_in_wall_result = None

                self.hole_in_wall_result = subprocess.run(['python', 'games\Hole in the Wall\hole_in_the_wall.py'], capture_output=True, text=True)
                if self.hole_in_wall_result.stdout.strip() == "True":
                    self.hole_in_wall_result == True
                else:
                    self.hole_in_wall_result == False
                pygame.init()
                self.reinitialize_camera = True
                pygame.mixer.music.unpause()  # Resume background music
                clock.tick(FPS)  # Resume Pygame clock

            elif 583 < self.setup_x < 983 and 150 < self.setup_y < 500 and timer_interval <= 0:
                pygame.mixer.music.pause()
                clock.tick_busy_loop(0)

                # Release resources that might interfere with subprocess
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.display.quit()
                self.cracks_in_the_shield_result = None

                self.cracks_in_the_shield_result = subprocess.run(['python', 'games\Cracks in the Shield\kirishima.py'], capture_output=True, text=True)
                if self.cracks_in_the_shield_result.stdout.strip() == "True":
                    self.cracks_in_the_shield_result == True
                else:
                    self.cracks_in_the_shield_result == False
                pygame.init()
                self.reinitialize_camera = True
                pygame.mixer.music.unpause()
                clock.tick(FPS)

            elif 1033 < self.setup_x < 1433 and 150 < self.setup_y < 500:
                pygame.mixer.music.pause()
                clock.tick_busy_loop(0)

                # Release resources that might interfere with subprocess
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.display.quit()

                self.ice_cutter_result = None

                # Run the external script
                self.ice_cutter_result = subprocess.run(['python', 'games/Ice cutter/shota.py'], capture_output=True, text=True)
                if self.ice_cutter_result.stdout.strip() == "True":
                    self.ice_cutter_result = True
                else:
                    self.ice_cutter_result = False

                pygame.init()
                self.reinitialize_camera = True
                pygame.mixer.music.unpause()  # Resume background music
                clock.tick(FPS)  # Resume Pygame clock

            elif 333 < self.setup_x < 733 and 600 < self.setup_y < 950:
                pygame.mixer.music.pause()
                clock.tick_busy_loop(0) 

                # Release resources that might interfere with subprocess
                setup.webcam.release()
                cv2.destroyAllWindows() 
                pygame.display.quit()
                self.drop_off_result = None

                self.drop_off_result = subprocess.run(['python', 'games\Drop Off\momo.py'], capture_output=True, text=True)
                if self.drop_off_result.stdout.strip() == "True":
                    self.drop_off_result == True
                else:
                    self.drop_off_result == False
                pygame.init()
                self.reinitialize_camera = True
                pygame.mixer.music.unpause()
                clock.tick(FPS) 

            elif 783 < self.setup_x < 1183 and 600 < self.setup_y < 950:
                pygame.mixer.music.pause()
                clock.tick_busy_loop(0)

                # Release resources that might interfere with subprocess
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.display.quit()
                self.decay_invaders_result = None

                self.decay_invaders_result = subprocess.run(['python', 'games\Decay Invaders\shigaraki.py'], capture_output=True, text=True)
                if self.decay_invaders_result.stdout.strip() == "True":
                    self.decay_invaders_result == True
                else:
                    self.decay_invaders_result == False
                pygame.init()
                self.reinitialize_camera = True
                pygame.mixer.music.unpause()
                clock.tick(FPS)
            
            else:
                if timer_interval <= 0:
                    return 0
        
        return 1

    def how_to_page(self, x, y):
        background_1 = pygame.image.load("menu/items/bg-5.png").convert_alpha()
        background_1 = pygame.transform.scale(background_1, (1565, 1000)) 

        back_button = pygame.image.load("menu/buttons/button-12.jpg").convert_alpha()
        back_button = pygame.transform.scale(back_button, (320, 180))

        shigi = pygame.image.load("menu\characters\shigiraki.webp").convert_alpha()


        setup.screen.blit(background_1, (0,0))
        setup.screen.blit(back_button, (50, 770))
        setup.screen.blit(shigi, (50, 100))
        pygame.draw.rect(setup.screen, self.box_color, pygame.Rect(50, 770, 320,180), 5)
        if self.how_to_selector_temp == self.how_to_selector + 1:
            self.how_to_selector = int(self.how_to_selector_temp)
        setup.screen.blit(self.how_to_images[self.how_to_selector], (622, 100))
        setup.screen.blit(self.how_to_text[self.how_to_selector], (622, 100))

        self.draw_text("Make a Fist to scroll through Instructions", self.font, self.text_col,622,770)

        self.draw_text("< Home", self.font, self.text_col,125,825)

        
        #alter this.
        if x != None and y != None:
            self.setup_x = 1565 - (x * 1565)
            self.setup_y = int(y * 1000) 
        else:
            if 50 < self.setup_x < 370 and 770 < self.setup_y < 950:
                return 0
            else:
                if self.how_to_selector_temp <= 5 :
                    self.how_to_selector_temp += 0.2
                    self.how_to_selector_temp = round(self.how_to_selector_temp, 1)
                else:
                    self.how_to_selector = 0
                    self.how_to_selector_temp = 0
        
        return 2


def main(window):
    clock = pygame.time.Clock()
    dt = clock.tick(FPS) / 1000.0 
    frame_increment = dt * intro_vid_fps
    w, h = pygame.display.get_surface().get_size()
    menu_functions = Menu_Functions(window)
    game_paused = False

    #if 0 then home, 1, then play, 2 then how to, 3 then quit, depending on what the buttons press it will return a number
    #this number will direct the page.
    page_number = -1
    mid_cursor = pygame.image.load("menu\items\mid_cursor.png").convert_alpha()
    mid_cursor = pygame.transform.scale(mid_cursor, (139, 121))

    #skip button
    skip_button = pygame.image.load("menu/buttons/button-7.png").convert_alpha()
    skip_button = pygame.transform.scale(skip_button, (320, 100))

    skip_text = pygame.image.load("menu\items\make a fist here to skip.png").convert_alpha()
    skip_text = pygame.transform.scale(skip_text, (276, 42))
    
    #background music
    bm_songs = [
        "menu\items\My Hero Academia Season 2 - Opening 1  Peace Sign.mp3",
        "games\Decay Invaders\Background\My Hero Academia OST - You Say Run  Jet Set Run (You Say Run v2).mp3",
        "games\Decay Invaders\Background\MY HEROACADEMIA 6th season ED.mp3",
        "games\Decay Invaders\Background\ED02MY HEROACADEMIA 6th season ED Movie.mp3"
        "games\Decay Invaders\Background\My Heroacademia 7th season Ending Movie.mp3"
    ]
    bm_counter = 0
    music_changer = 0
    setup.hands = setup.mp_hands.Hands(max_num_hands=1)

    pygame.mixer.music.load(bm_songs[bm_counter])
    pygame.mixer.music.play(-1,0,0)
    t = 0
    surface = menu_functions.game_trailer(None, None, 0)

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    time_between_pages = 0
    play_page_interval = False

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: 
                if play_page_interval == True and time_between_pages > 0:
                    time_between_pages -= 1
                if time_between_pages == 0:
                    play_page_interval = False

            if event.type == pygame.QUIT:
                setup.webcam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        setup.webcam_menu(setup.hands, max_hands = 1)
        pygame.surfarray.blit_array(setup.screen, setup.img)


        if page_number == -1:
            try:
                setup.screen.blit(menu_functions.game_trailer(setup.x, setup.y, t, surface), (0, 0))
                setup.screen.blit(skip_button, (1215, 875))
                setup.screen.blit(skip_text, (1235, 905))
                t += frame_increment - 0.261
            except TypeError:
                page_number = 0


        elif page_number == 0:
            page_number, play_page_interval = menu_functions.home_page(setup.x, setup.y)
            if play_page_interval == True:
                time_between_pages = 3
        elif page_number == 1:
            page_number = menu_functions.play_page(setup.x, setup.y, time_between_pages)
        elif page_number == 2:
            page_number = menu_functions.how_to_page(setup.x, setup.y)
        elif page_number == 3:
            setup.webcam.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

        if setup.x != None:
            mid_cursor_rect = mid_cursor.get_rect(center = (1565 - (setup.x * 1565), int(setup.y * 1000)))
            setup.screen.blit(mid_cursor, mid_cursor_rect)

        if menu_functions.reinitialize_camera:
            menu_functions.reinitialize_camera = False
            setup.mp_hands = mp.solutions.hands
            setup.mp_drawing = mp.solutions.drawing_utils
            setup.mp_drawing_styles = mp.solutions.drawing_styles
            setup.webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            setup.game_clock = time.time()
            setup.game_is_running = True
            setup.hands = None
            setup.x = 0
            setup.y = 0
            setup.l_0 = []
            setup.l_1 = []
            setup.hands = setup.mp_hands.Hands(max_num_hands=1)
            setup.screen = pygame.display.set_mode((1565,1000))
            pygame.display.set_caption("The UA Sports Festival")

            


        pygame.display.update()
        pygame.display.flip()

if __name__ == "__main__":
    main(setup.screen)
