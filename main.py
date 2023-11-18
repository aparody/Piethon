import random
import pygame
import sys
import speech_recognition as sr
import threading
from enum import Enum

pygame.init()
recognizer = sr.Recognizer()
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (249, 113, 110)
blueberry = (42, 65, 111)
cherry = (204, 0, 0)
apple = (141, 182, 0)
pumpkin = (255, 117, 24)
pecan = (193, 176, 148)
lemon = (255, 243, 79)
blackberry = (77, 1, 52)
screen_width = 600
screen_height = 600
scene_index = 0     #Keeps track of current scene. 0 is start, 1 is play, 2 is end, and 3 is instructions screen
color_menu = 0
color = blueberry

start_bg = pygame.image.load("images\startscreen.jpg")
start_bg = pygame.transform.scale(start_bg, (screen_width, screen_height))
play_bg = pygame.image.load("images/play-background.jpeg")
play_bg = pygame.transform.scale(play_bg, (screen_width, screen_height))
end_bg = pygame.image.load("images\endscreen.jpg")
end_bg = pygame.transform.scale(end_bg, (screen_width, screen_height))
instr_bg = pygame.image.load("images\instructionscreen.jpg")
instr_bg = pygame.transform.scale(instr_bg, (screen_width, screen_height))
pie_img = pygame.image.load("images/pie.png")
pie_img = pygame.transform.scale(pie_img, (40, 40))

CHANGE_UP = pygame.USEREVENT + 1
CHANGE_RIGHT = pygame.USEREVENT + 2
CHANGE_DOWN = pygame.USEREVENT + 3
CHANGE_LEFT = pygame.USEREVENT + 4
PAUSE_GAME = pygame.USEREVENT + 5
RESUME_GAME = pygame.USEREVENT + 6

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def voice_recognition():
    global scene_index
    global color_menu
    global color

    while True:
        with sr.Microphone() as source:
            recognizer.pause_threshold = 1.5
            # recognizer.adjust_for_ambient_noise(source)
            print("Listening for voice commands...")
            audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                print("You said:", command)

                 #Start screen commands
                if scene_index == 0:
                    if "start" in command:
                        scene_index = 1
                    elif "instructions" in command:
                        scene_index = 3
                    elif "customize" in command:
                        color_menu = 1
                    elif "back" in command:
                        color_menu = 0
                    elif color_menu == 1 and "apple" in command:
                            color = apple
                    elif color_menu == 1 and "blackberry" in command:
                        color = blackberry
                    elif color_menu == 1 and "blueberry" in command:
                        color = blueberry
                    elif color_menu == 1 and "cherry" in command:
                        color = cherry
                    elif color_menu == 1 and "lemon" in command:
                        color = lemon
                    elif color_menu == 1 and "pecan" in command:
                        color = pecan
                    elif color_menu == 1 and "pumpkin" in command:
                        color = pumpkin
                    else:
                        print("Unrecognized command") 
                
                #Play screen commands
                elif scene_index == 1:
                    if "up" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_UP))
                    elif "down" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_DOWN))
                    elif "left" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_LEFT))
                    elif "right" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_RIGHT))
                    elif "pause" in command:
                        pygame.event.post(pygame.event.Event(PAUSE_GAME))
                    elif "resume" in command:
                        pygame.event.post(pygame.event.Event(RESUME_GAME))
                    #'Next' command is used for testing the end screen quickly
                    elif "next" in command:
                        scene_index = 2
                    else:
                        print("Unrecognized command")
                
                #End screen commands
                elif scene_index == 2:
                    if "retry" in command:
                        scene_index = 1
                    elif "menu" in command:
                        scene_index = 0
                    elif "exit" in command:
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()
                    else:
                        print("Unrecognized command")

                #Instruction commands
                elif scene_index == 3:
                    if "begin" in command:
                        scene_index = 0
                    else:
                        print("Unrecognized command")
                  
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


def start_screen(high_score):
    global scene_index
    global color_menu

    colors = [
    "apple", "blackberry", "blueberry", "cherry", 
    "lemon", "pecan", "pumpkin"
    ]

    color_dict = {
    "apple": apple,
    "blackberry": blackberry,
    "blueberry": blueberry,
    "cherry": cherry,
    "lemon": lemon,
    "pecan": pecan,
    "pumpkin": pumpkin,
    }
    
    while scene_index == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(start_bg, (0, 0))

        instruction_font = pygame.font.Font(None, 45)
        customize_font = pygame.font.Font(None, 30)
        
        instruction_text1 = instruction_font.render("Say 'start' to play", True, black)
        instruction_text2 = instruction_font.render("Say 'instructions' for instructions", True, black)
        score_text = instruction_font.render(str(high_score), True, black)
        customize_text = customize_font.render("Customize", True, black)

        instruction_rect1 = instruction_text1.get_rect()
        instruction_rect2 = instruction_text2.get_rect()
        score_rect = score_text.get_rect()
        customize_rect = customize_text.get_rect()

        instruction_rect1.center = (screen_width // 2, screen_height // 2 + 225)
        instruction_rect2.center = (screen_width // 2, screen_height // 2 + 255)
        score_rect.center = (75, 375)
        customize_rect.center = (520, 80)

        screen.blit(instruction_text1, instruction_rect1)
        screen.blit(instruction_text2, instruction_rect2)
        screen.blit(score_text, score_rect)
        screen.blit(customize_text, customize_rect)

        color_font = pygame.font.Font(None, 35)
        if color_menu == 1:
            color_instructions1 = color_font.render("Say an option to change snake colors", True, black)
            color_instructions2 = color_font.render("Say back to close the color menu", True, black)
            color_rect1 = color_instructions1.get_rect()
            color_rect2 = color_instructions2.get_rect()
            color_rect1.center = (220, 140)
            color_rect2.center = (220, 170)
            screen.blit(color_instructions1, color_rect1)
            screen.blit(color_instructions2, color_rect2)

            for i, color_name in enumerate(colors):
                color_text = color_font.render(color_name, True, color_dict[color_name])
                color_rect = color_text.get_rect()
                color_rect.center = (520, 120 + i * 40)
                screen.blit(color_text, color_rect)

        pygame.display.update()

def play_screen():
    global scene_index

    def move_snake():
        
        prevVal = snake[0][:]
        for x in range(1,len(snake)):
            temp = snake[x][:]
            snake[x] = prevVal
            prevVal = temp
        
        if currentDirection == Direction.RIGHT:
            snake[0][0] += 30
        elif currentDirection == Direction.DOWN:
            snake[0][1] += 30
        elif currentDirection == Direction.LEFT:
            snake[0][0] -= 30
        elif currentDirection == Direction.UP:
            snake[0][1] -= 30
    
    def generate_pie():
        pie = [random.randrange(30, screen_width - 30), random.randrange(60, screen_height - 30)]
        while pie in snake:
            pie = [random.randrange(30, screen_width - 30), random.randrange(60, screen_height - 30)]
        pie = [pie[0] // 30 * 30, pie[1] // 30 * 30]
        return pie

    def add_tail():
        # should eventually account for if adding to tail would cause to cross border
        currentEnd = snake[-1]
        if currentDirection == Direction.RIGHT:
            snake.append([currentEnd[0] - 30, currentEnd[1]])
        elif currentDirection == Direction.DOWN:
            snake.append([currentEnd[0], currentEnd[1] - 30])
        elif currentDirection == Direction.LEFT:
            snake.append([currentEnd[0] + 30, currentEnd[1]])
        elif currentDirection == Direction.UP:
            snake.append([currentEnd[0], currentEnd[1] + 30])

    
    score = 0
    currentDirection = Direction.RIGHT
    snake = [
        [screen_width // 2, screen_height // 2],
        [screen_width // 2 - 30, screen_height // 2],
        [screen_width // 2 - 60, screen_height // 2]
    ]
    clock = pygame.time.Clock()
    # NOTE: The below is temporary because otherwise it is impossible to get the pie :(
    # pie = generate_pie()
    pie = [screen_width // 2 + 60, screen_height // 2]
    isPaused = False

    while scene_index == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == CHANGE_UP:
                if currentDirection != Direction.DOWN:
                    currentDirection = Direction.UP
            if event.type == CHANGE_DOWN:
                if currentDirection != Direction.UP:
                    currentDirection = Direction.DOWN
            if event.type == CHANGE_RIGHT:
                if currentDirection != Direction.LEFT:
                    currentDirection = Direction.RIGHT
            if event.type == CHANGE_LEFT:
                if currentDirection != Direction.RIGHT:
                    currentDirection = Direction.LEFT
            if event.type == PAUSE_GAME:
                isPaused = True
            if event.type == RESUME_GAME:
                isPaused = False
        
        screen.blit(play_bg, (0, 0))
        for x in range(30,screen_width - 30, 30):
            for y in range(60,screen_height - 30, 30):
                checkColor = red if (x / 30) % 2 != (y / 30) % 2 else white
                pygame.draw.rect(screen, checkColor, pygame.Rect(x, y, 30, 30))

        for coord in snake:
            pygame.draw.circle(screen, color, (coord[0] + 15, coord[1] + 15), 15)
        
        screen.blit(pie_img, (pie[0] - 5, pie[1] - 5))
        
        if not isPaused:
            move_snake()

        if snake[0][0] < 0 or snake[0][0] > screen_width - 30 or snake[0][1] < 30 or snake[0][1] > screen_height - 30:
            # snake reached wall, end game
            print('game ended')
            scene_index = 2
            return score
        elif snake[0][0] in snake[1:]:
            # snake hit itself, end game
            print('game ended')
            scene_index = 2
            return score
        if snake[0] == pie:
            # snake has eaten pie
            score += 1
            add_tail()
            pie = generate_pie()
        
        scoreFont = pygame.font.Font(None, 30)
        scoreText = scoreFont.render("Score: " + str(score), True, black)
        scoreRect = scoreText.get_rect()
        scoreRect.topright = (screen_width, 0)

        commandFont = pygame.font.Font(None, 30)
        commandText = commandFont.render(currentDirection.name, True, black)
        commandRect = commandText.get_rect()
        commandRect.topleft = (0, 0)

        pygame.draw.rect(screen, black, (30, 60, screen_width - 60, screen_height - 90), 1)

        screen.blit(scoreText, scoreRect)
        screen.blit(commandText, commandRect)
        pygame.display.update()

        clock.tick(1)
        
    return score

def end_screen(score):
    while scene_index == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(end_bg, (0, 0))

        instruction_font = pygame.font.Font(None, 30)
        instruction_text1 = instruction_font.render("Please say 'retry' to try again", True, white)
        instruction_text2 = instruction_font.render("say 'menu' to return to the start", True, white)
        instruction_text3 = instruction_font.render("or say 'exit' to quit", True, white)
        score_text = instruction_font.render("Score: " + str(score), True, white)

        instruction_rect1 = instruction_text1.get_rect()
        instruction_rect2 = instruction_text2.get_rect()
        instruction_rect3 = instruction_text3.get_rect()
        score_rect = score_text.get_rect()

        instruction_rect1.center = (150, 60)
        instruction_rect2.center = (165, 90)
        instruction_rect3.center = (105, 120)
        score_rect.center = (405, 150)

        screen.blit(instruction_text1, instruction_rect1)
        screen.blit(instruction_text2, instruction_rect2)
        screen.blit(instruction_text3, instruction_rect3)
        screen.blit(score_text, score_rect)
        pygame.display.update()

def instruction_screen():

    while scene_index == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(instr_bg, (0, 0))

        pygame.display.update()

voice_thread = threading.Thread(target=voice_recognition)
voice_thread.start()
high_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if scene_index == 0:
        start_screen(high_score)
    elif scene_index == 1:
        score = play_screen()
    elif scene_index == 2:
        if score > high_score:
            high_score = score
        end_screen(score)
    elif scene_index == 3:
        instruction_screen()
    
    pygame.display.update()



