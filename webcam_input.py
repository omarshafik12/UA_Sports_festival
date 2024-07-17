import sys, time, random, pygame
import cv2
import mediapipe as mp

class Prerequisites(): 
    #don' forget that you want to add width and heigh since not all game will have the same.
    def __init__(self, width, height):
    # MediaPipe hands initialization
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        #drawing_spec = mp_drawing.DrawingSpec(thickness = 1, circle_radius = 1)

        # Webcam initialization
        # Omar the problem you were having was that it took so long to load, you thought it wasn't working. 
            #The way to fix this is that you leave 0 for when you deliver it to people, but as you test you figure out what videocapture API starts the program instantly and doesn't cause the video to be slow. 
            #I think the reason that it takes a long time is that it is trying to find the best option from all the potential API backends.
            #https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga023786be1ee68a9105bf2e48c700294d
            #cv2.CAP_MSMF
        self.webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        #this is where you would add your sprites, 13:28
        self.game_clock = time.time()
        self.game_is_running = True
        self.hands = None
        self.x = 0
        self.y = 0
        self.l_0 = []
        self.l_1 = []
    

    def webcam_ai(self, hands, max_hands, capture = False):
        #with self.mp_hands.Hands(max_num_hands=1) as hands:
        success, img = self.webcam.read()
        if not success:
            print("Frame not Appearing")

        
        self.screen.fill((255,255,255))
        img.flags.writeable = False

        #hand tracking
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = hands.process(img_rgb)
        img.flags.writeable = True
        #inputting finger point data to move character. 22:02

        if max_hands == 1:
        
            if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
                marker = results.multi_hand_landmarks[0].landmark[8]
                self.x = marker.x
                self.y = marker.y

                #this is how you would move an object with this.
                #bird_frame.centery = (y) 

                #this is to make sure that the object doesn't go off screen !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! This can be your zoning. Manipulate this conditoinal
            
        if max_hands >= 1 and capture:
            if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0: #https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
                #so I am going to have it be imported into a list and when the timer reaches a point it will for loop and see if the point is on the mask
                #capture waits until the hole in the wall timer stops and it makes it true so that this loop only happens once, else it will consume unneeded energy
                #I have capture set to default cause I can't be asked to write it each time.
                try:
                    for i in range(21): 
                        marker = results.multi_hand_landmarks[0].landmark[i]
                        self.l_0.append([marker.x, marker.y])
                except IndexError:
                    self.l_0 = []
                if max_hands == 2:
                    try:    
                        for i in range(21):
                            marker = results.multi_hand_landmarks[1].landmark[i]
                            self.l_1.append([marker.x, marker.y])
                    except IndexError:
                        self.l_1 = []


        #drawing the hand tracking, unneccessary for now and will only slow down the program
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(img_rgb, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        img_rgb = cv2.resize(img_rgb, (self.width, self.height))
        self.img = cv2.flip(img_rgb, 1).swapaxes(0,1)
    
    def webcam_menu(self, hands, max_hands, capture = False):
        #with self.mp_hands.Hands(max_num_hands=1) as hands:
        success, img = self.webcam.read()
        if not success:
            print("Frame not Appearing")

        
        self.screen.fill((255,255,255))
        
        img.flags.writeable = False

        #hand tracking
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = hands.process(img_rgb)
        img.flags.writeable = True
        #inputting finger point data to move character. 22:02

        if max_hands == 1:
        
            if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
                marker = results.multi_hand_landmarks[0].landmark[8]
                self.x = marker.x
                self.y = marker.y

                #thumb location
                #thumb_marker = results.multi_hand_landmarks[0].landmark[4]
                #thumb_x = thumb_marker.x
                #thumb_y = thumb_marker.y

                #pinky location
                thumb_marker = results.multi_hand_landmarks[0].landmark[20]
                pinky_x = thumb_marker.x
                pinky_y = thumb_marker.y

                distance_index_pinky = ((marker.x - pinky_x) ** 2 + (marker.y - pinky_y) ** 2) ** 0.5

                if distance_index_pinky < 0.13:  # Threshold for rock gesture, justchaange the 0.15
                    self.x = None
                    self.y = None


        
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(img_rgb, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        img_rgb = cv2.resize(img_rgb, (self.width, self.height))
        self.img = cv2.flip(img_rgb, 1).swapaxes(0,1)