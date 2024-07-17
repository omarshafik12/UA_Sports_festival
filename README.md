                                                    Project Title: U.A. Sports Festival

Project Overview

    This project is a game where a player can choose to play between 6(changed to 5 due to time constraints) games.

    The player, playing as Midoriya can face against characters such as Kirishima, Shoto Todoroki, Shigaraki, Momo, and more,
    with games modeled after traditional games such as Whack a mole, Hole in the wall, Air Hockey, and a few unique ones.


Project Description

    For the specific anatomy and logic behind certains games, please do visit the respective folder and analzye the games text file.
    The structure of each text file is mirrored to the layout of their respective game mechanics class for easier readibility and 
    classification.


How to play

    Github Clone Route:
        - Please do feel free to clone this repository and after pip installing all aspects listed down below to play the game and some fun, good luck beating Shigiraki.
            - pip install pygame
            - pip install numpy
            - pip install opencv-python
            - pip install mediapipe
            - pip install moviepy
            
  - **Most importantly please put this downloaded video clip, [Sports Festival Clip](https://drive.google.com/uc?export=download&id=15qQZQzsBDhgLjMPWwbMjZ1tNuoOyslN5), in this file, The_UA_Visual_Sports_Festival\menu\items\. It was way too large for me to push onto this repo.**





Languages/Tools Used
    
    Python: Python was used to write all instructions, variables, functions, etc.

    Pygame: The pygame framework was chosen due to its compbatibility with OpenCV, for example, the unique capability that I could take a subsurface of the surface in hole in the wall with just a simple method was extremely powerful and useful. 
    Secondly, extensive resources from Pygame's documentation and the vast amount of youtube vid & Stack Overflow solutions provided many answers and how tos to my questions. Lastly, Pygame's ease of use was a great framework for me to start on 
    since the difficulty was less complex.

    OpenCV: This webcam & AI framework was the best option due to its extensive features and capability to manipulate webcam input such as flipping screen, choosing the correct webcam mode, etc. OpenCV's ability to work well in tandem with Mediapipe
    and Pygame allowed those two seperate frameworks to come together and create the game's main unique feature of finger controlled input.

    Mediapipe: Mediapipe provided the simplest transition of the single data point I wanted, The index of certain parts of the finger(index and pinky). With this link it tells you what to index to get the part of the finger you want, 
    https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer?fbclid=IwAR1bfKGZD_4Ebv4j1HvVrsJv1CJxc74iYd0X8TUkHgTCohe8mbhE5WAHC-0. Furthermore Mediapipe provided an easy way to draw points on the hand to give it that cool effect, 
    and if you or I wanted to, the ability to have gesture control which would add futher cool functionality.

Resources

    This is the content that I used to learn Pygame, OpenCv, and Mediapipe:
    
    Pygame:
        - https://www.youtube.com/watch?v=6gLeplbqtqg&ab_channel=freeCodeCamp.org
        - https://www.youtube.com/watch?v=nXOVcOBqFwM&ab_channel=CodingWithRuss
        - https://www.youtube.com/watch?v=IJb6EthAbIc&list=PLCC34OHNcOtpOG96Uwh3VGkmpZ7qTB5dx&index=12&ab_channel=Codemy.com
        - https://www.youtube.com/watch?v=tJiKYMQJnYg&ab_channel=CodingWithRuss
        - https://www.youtube.com/watch?v=tEedb5KiaWY&list=PLCC34OHNcOtpOG96Uwh3VGkmpZ7qTB5dx&index=6&ab_channel=Codemy.com
        - https://stackoverflow.com/questions/68841168/read-pygame-window-with-open-cv
        - https://www.youtube.com/watch?v=Tm7Iy6_YW1w&ab_channel=CodeSavant
        - https://www.youtube.com/watch?v=tx0GKO8_koE&ab_channel=Zenva
        - https://www.tutorialspoint.com/How-can-I-make-one-Python-file-run-another
        - https://stackoverflow.com/questions/21356439/how-to-load-and-play-a-video-in-pygame/76853293#76853293

    OpenCV & Mediapipe:
        - https://www.youtube.com/watch?v=qCR2Weh64h4&list=PLzMcBGfZo4-lUA8uGjeXhBUUzPYc6vZRn&index=2&ab_channel=TechWithTim (All 8 videos in the playlist)
        - https://www.youtube.com/watch?v=v-ebX04SNYM&ab_channel=Koolac 
        - https://www.youtube.com/watch?v=E46B7NPWK38&ab_channel=PaulMcWhorter
        - https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga023786be1ee68a9105bf2e48c700294d 
