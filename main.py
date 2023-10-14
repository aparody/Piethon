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

#Keeps track of current scene. 0 is start, 1 is play, 2 is end, and 3 is instructions screen
scene_index = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

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
                if scene_index == 1:
                    if "up" in command:
                        pass
                    elif "down" in command:
                        pass
                    elif "left" in command:
                        pass
                    elif "right" in command:
                        pass
                    #Used for testing purposes
                    elif "next" in command:
                        scene_index = 2
                    else:
                        print("Unrecognized command")
                
                #End screen commands
                if scene_index == 2:
                    if "retry" in command:
                        scene_index = 1
                    elif "exit" in command:
                        pygame.quit()

                #Instruction commands
                if scene_index == 3:
                    if "continue" in command:
                        scene_index = 0
                    else:
                        print("Unrecognized command")
                
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


def start_screen():
    global scene_index
    
    while scene_index == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         scene_index = 1
            #         return

        screen.fill(white)
        titleFont = pygame.font.Font(None, 72)
        titleText = titleFont.render("Piethon", True, black)
        titleRect = titleText.get_rect()
        titleRect.center = (screen_width // 2, screen_height // 2)

        instructionFont = pygame.font.Font(None, 36)
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
    #Nothing is implemented here yet, just needed something for testing
    while scene_index == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)
        pygame.display.update()

def end_screen():
    while scene_index == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(green)
        titleFont = pygame.font.Font(None, 72)
        titleText = titleFont.render("Game over", True, black)
        titleRect = titleText.get_rect()
        titleRect.center = (screen_width // 2, screen_height // 2)

        instructionFont = pygame.font.Font(None, 36)
        instructionText1 = instructionFont.render("Say 'retry' to try again", True, black)
        instructionText2 = instructionFont.render("Say 'exit' to quit", True, black)

        instructionRect1 = instructionText1.get_rect()
        instructionRect2 = instructionText2.get_rect()

        instructionRect1.center = (screen_width // 2, screen_height // 2 + 50)
        instructionRect2.center = (screen_width // 2, screen_height // 2 + 90)

        screen.blit(titleText, titleRect)
        screen.blit(instructionText1, instructionRect1)
        screen.blit(instructionText2, instructionRect2)
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if scene_index == 0:
        start_screen()
    elif scene_index == 1:
        play_screen()
    elif scene_index == 2:
        end_screen()
    elif scene_index == 3:
        instruction_screen()
    
    pygame.display.update()



