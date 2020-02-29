import string
import time

import pygame
import pygame.draw
import pygame.event
import pygame.font
from pygame.locals import *


def get_key():
    t = time.time() + 10
    while time.time() < t:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        elif event.type == QUIT:
            exit()
        else:
            pass
    return None

def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None, 30)
    pygame.draw.rect(screen, (0,0,0),
                    (125, 438 - 10, 300, 20), 0)
    pygame.draw.rect(screen, (255,255,255),
                    (125 - 2, 438 - 12, 304, 24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                    (125, 438 - 10))
    pygame.display.flip()


def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + "".join(current_string))
    while 1:
        inkey = get_key()
        if inkey is None:
            break
        elif inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            break
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + ''.join(current_string))
    return "".join(current_string)

def main():
    screen = pygame.display.set_mode((320,240))
    print(ask(screen, "Name") + " was entered")

if __name__ == '__main__': main()
