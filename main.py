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
red = (255, 0, 0)
screen_width = 400
screen_height = 400
game_running = False

CHANGE_UP = pygame.USEREVENT + 1
CHANGE_RIGHT = pygame.USEREVENT + 2
CHANGE_DOWN = pygame.USEREVENT + 3
CHANGE_LEFT = pygame.USEREVENT + 4

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def voice_recognition():
    global game_running

    while True:
        with sr.Microphone() as source:
            print("Listening for voice commands...")
            audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                print("You said:", command)

                if game_running:
                    # Process the command and control the Snake
                    if "up" in command:
                        # Move the Snake up
                        pygame.event.post(pygame.event.Event(CHANGE_UP))
                        pass
                    elif "down" in command:
                        # Move the Snake down
                        pygame.event.post(pygame.event.Event(CHANGE_DOWN))
                        pass
                    elif "left" in command:
                        # Move the Snake left
                        pygame.event.post(pygame.event.Event(CHANGE_LEFT))
                        pass
                    elif "right" in command:
                        # Move the Snake right
                        pygame.event.post(pygame.event.Event(CHANGE_RIGHT))
                        pass
                    else:
                        print("Unrecognized command")
                else:
                    if "start" in command:
                        game_running = True
                    else:
                        print("Unrecognized command") 

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


def start_screen():
    global game_running
    
    while not game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_running = True
                    return

        screen.fill(white)
        titleFont = pygame.font.Font(None, 72)
        titleText = titleFont.render("Snake Game", True, black)
        titleRect = titleText.get_rect()
        titleRect.center = (screen_width // 2, screen_height // 2)

        instructionFont = pygame.font.Font(None, 36)
        instructionText = instructionFont.render("Say 'start' to play", True, black)
        instructionRect = instructionText.get_rect()
        instructionRect.center = (screen_width // 2, screen_height // 2 + 50)

        screen.blit(titleText, titleRect)
        screen.blit(instructionText, instructionRect)
        pygame.display.update()

def play_screen():

    def move_snake():
        
        prevVal = snake[0][:]
        for x in range(1,len(snake)):
            temp = snake[x][:]
            snake[x] = prevVal
            prevVal = temp
        
        if currentDirection == Direction.RIGHT:
            snake[0][0] += 10
        elif currentDirection == Direction.DOWN:
            snake[0][1] += 10
        elif currentDirection == Direction.LEFT:
            snake[0][0] -= 10
        elif currentDirection == Direction.UP:
            snake[0][1] -= 10
    
    def generate_pie():
        pie = [random.randrange(1, screen_width), random.randrange(20, screen_height)]
        while pie in snake:
            pie = [random.randrange(1, screen_width), random.randrange(20, screen_height)]
        pie = [pie[0] // 10 * 10, pie[1] // 10 * 10]
        return pie

    def add_tail():
        # should eventually account for if adding to tail would cause to cross border
        currentEnd = snake[-1]
        if currentDirection == Direction.RIGHT:
            snake.append([currentEnd[0] - 10, currentEnd[1]])
        elif currentDirection == Direction.DOWN:
            snake.append([currentEnd[0], currentEnd[1] - 10])
        elif currentDirection == Direction.LEFT:
            snake.append([currentEnd[0] + 10, currentEnd[1]])
        elif currentDirection == Direction.UP:
            snake.append([currentEnd[0], currentEnd[1] + 10])


    # color will eventually be changeable
    color = green
    score = 0
    currentDirection = Direction.RIGHT
    snake = [
        [screen_width // 2, screen_height // 2],
        [screen_width // 2 - 10, screen_height // 2],
        [screen_width // 2 - 20, screen_height // 2]
    ]
    clock = pygame.time.Clock()
    # pie = generate_pie()
    pie = [screen_width // 2 + 40, screen_height // 2]

    while game_running:
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
        
        screen.fill(black)

        for coord in snake:
            pygame.draw.rect(screen, color, pygame.Rect(coord[0], coord[1], 10, 10))
        
        pygame.draw.rect(screen, red, pygame.Rect(pie[0], pie[1], 10, 10))
        
        move_snake()

        if snake[0][0] < 0 or snake[0][0] > screen_width or snake[0][1] < 0 or snake[0][1] > screen_height:
            # snake reached wall, end game
            print('game ended')
        elif snake[0][0] in snake[1:]:
            # snake hit itself, end game
            print('game ended')
        
        if snake[0] == pie:
            # snake has eaten pie
            score += 1
            add_tail()
            pie = generate_pie()
        
        scoreFont = pygame.font.Font(None, 30)
        scoreText = scoreFont.render("Score: " + str(score), True, white)
        scoreRect = scoreText.get_rect()
        scoreRect.center = (screen_width // 2, 10)

        commandFont = pygame.font.Font(None, 30)
        commandText = commandFont.render(currentDirection.name, True, white)
        commandRect = commandText.get_rect()
        commandRect.topleft = (0, 0)

        pygame.draw.rect(screen, red, (0, 20, screen_width, screen_height - 20), 1)
        
        clock.tick(1)

        screen.blit(scoreText, scoreRect)
        screen.blit(commandText, commandRect)
        pygame.display.update()



voice_thread = threading.Thread(target=voice_recognition)
voice_thread.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_running:
        play_screen()
    else:
        start_screen()

    pygame.display.update()



