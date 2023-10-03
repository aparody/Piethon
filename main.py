import pygame
import sys
import speech_recognition as sr
import threading

pygame.init()

recognizer = sr.Recognizer()
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
screen_width = 400
screen_height = 400
game_running = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

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
                        pass
                    elif "down" in command:
                        # Move the Snake down
                        pass
                    elif "left" in command:
                        # Move the Snake left
                        pass
                    elif "right" in command:
                        # Move the Snake right
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

    #Nothing is implemented here yet, just needed something for testing
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)
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



