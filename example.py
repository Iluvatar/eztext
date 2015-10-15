# EzText example
from pygame.locals import *
import pygame, sys, eztext

def main():
    # initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((640,240), pygame.RESIZABLE)
    # fill the screen w/ white
    screen.fill((255,255,255))
    # here is the magic: making the text input
    # create an input with a max length of 45,
    # and a red color and a prompt saying 'type here: '
    txtbx1 = eztext.Input(max_length=30, prompt='', x=10, y=10, font=pygame.font.SysFont('monospace', 24), input_width=420, default_text="First Name")
    txtbx2 = eztext.Input(max_length=10, prompt='', x=10, y=44, font=pygame.font.SysFont('monospace', 24), input_width=140, default_text="Last Name")
    # create the pygame clock
    clock = pygame.time.Clock()
    # main loop!

    while 1:
        # make sure the program is running at 30 fps
        clock.tick(30)

        # events for txtbx
        events = pygame.event.get()
        # process other events
        for event in events:
            # close it x button si pressed
            if event.type == QUIT: return
            if event.type == pygame.VIDEORESIZE:
                txtbx2.set_width(event.size[0] / 2)
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        # clear the screen
        screen.fill((255,255,255))
        # update txtbx
        txtbx1.update(events)
        txtbx1.draw(screen)
        txtbx2.update(events)
        txtbx2.draw(screen)
        # refresh the display
        pygame.display.flip()

if __name__ == '__main__': main()
