import random
import random
import pygame
import sys
import speech_recognition as sr
import threading
from enum import Enum
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
scene_index = 1     #Keeps track of current scene. 0 is start, 1 is play, 2 is end, and 3 is instructions screen

end_bg = pygame.image.load("images/endscreen.jpg")
end_bg = pygame.transform.scale(end_bg, (screen_width, screen_height))
play_bg = pygame.image.load("images/play-background.jpeg")
play_bg = pygame.transform.scale(play_bg, (screen_width, screen_height))
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

    while True:
        with sr.Microphone() as source:
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
                    else:
                        print("Unrecognized command") 
                
                #Play screen commands
                elif scene_index == 1:
                    if "up" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_UP))
                        pass
                    elif "down" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_DOWN))
                        pass
                    elif "left" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_LEFT))
                        pass
                    elif "right" in command:
                        pygame.event.post(pygame.event.Event(CHANGE_RIGHT))
                        pass
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
                    if "continue" in command:
                        scene_index = 0
                    else:
                        print("Unrecognized command")
                
                
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


def start_screen(high_score):
    global scene_index
    
    while scene_index == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        titleFont = pygame.font.Font(None, 72)
        titleText = titleFont.render("Piethon", True, black)
        titleRect = titleText.get_rect()
        titleRect.center = (screen_width // 2, screen_height // 4)

        instructionFont = pygame.font.Font(None, 30)
        instructionText1 = instructionFont.render("Say 'start' to play", True, black)
        instructionText2 = instructionFont.render("Say 'instructions' for instructions", True, black)

        instructionRect1 = instructionText1.get_rect()
        instructionRect2 = instructionText2.get_rect()

        instructionRect1.center = (screen_width // 2, screen_height // 2 + 50)
        instructionRect2.center = (screen_width // 2, screen_height // 2 + 90)

        screen.blit(titleText, titleRect)
        screen.blit(instructionText1, instructionRect1)
        screen.blit(instructionText2, instructionRect2)
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


    # color will eventually be changeable
    color = blueberry
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

        instructionFont = pygame.font.Font(None, 20)
        instructionText1 = instructionFont.render("Please say 'retry' to try again", True, white)
        instructionText2 = instructionFont.render("say 'menu' to return to the start", True, white)
        instructionText3 = instructionFont.render("or say 'exit' to quit", True, white)
        scoreText = instructionFont.render("Score: " + str(score), True, white)

        instructionRect1 = instructionText1.get_rect()
        instructionRect2 = instructionText2.get_rect()
        instructionRect3 = instructionText3.get_rect()
        scoreRect = scoreText.get_rect()

        instructionRect1.center = (105, 40)
        instructionRect2.center = (110, 60)
        instructionRect3.center = (70, 80)
        scoreRect.center = (270, 100)

        screen.blit(instructionText1, instructionRect1)
        screen.blit(instructionText2, instructionRect2)
        screen.blit(instructionText3, instructionRect3)
        screen.blit(scoreText, scoreRect)
        pygame.display.update()

def instruction_screen():
    instructions = [
        "'Up' 'Left' 'Right' 'Down'",
        "Speak the commands to move",
        "Say 'continue' to return",
    ]
    while scene_index == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)
        titleFont = pygame.font.Font(None, 56)
        titleText = titleFont.render("Instructions", True, black)
        titleRect = titleText.get_rect()
        titleRect.center = (screen_width // 2, 50)

        instructionFont = pygame.font.Font(None, 36)

        for i, text in enumerate(instructions):
            instructionText = instructionFont.render(text, True, black)
            instructionRect = instructionText.get_rect()
            instructionRect.center = (screen_width // 2, screen_height // 2 + 50 + i * 40)
            screen.blit(instructionText, instructionRect)

        screen.blit(titleText, titleRect)

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



