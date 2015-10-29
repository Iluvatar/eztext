# EzText example
from pygame.locals import *
import pygame

import eztext


def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 240), pygame.RESIZABLE)
    screen.fill((255, 255, 255))

    # create an input with purple text at (100, 100) that takes at most 7 characters
    txtbx1 = eztext.Input(pos=(100, 100), text_color=(180, 20, 180), max_length=7)

    # create an input that only takes numbers
    txtbx2 = eztext.Input(input_width=150, allowed_chars=eztext.Input.NUMS, default_text="numbers only",
                          set_key_repeat_speed=True)

    # create the pygame clock
    clock = pygame.time.Clock()

    while 1:
        clock.tick(30)

        # events for the inputs
        events = pygame.event.get()

        # process other events
        for event in events:
            if event.type == QUIT:
                return
            if event.type == pygame.VIDEORESIZE:
                txtbx2.input_width = event.size[0] / 2
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill((255, 255, 255))

        # update inputs
        txtbx1.update(events)
        txtbx1.draw(screen)
        txtbx2.update(events)
        txtbx2.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
