# pyform example
from pygame.locals import *
import pygame

import pyform


def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
    screen.fill((255, 255, 255))

    # returns a function that prints the value of the given form
    # used for on_change
    def p(this):
        def ret():
            print this.value
        return ret

    # allows repeats when holding down a key
    pyform.set_key_repeat(True)

    # checkbox group with 4 options
    checkgroup = pyform.CheckBoxGroup("checkgroup")
    checkgroup.add_checkbox(pyform.CheckBox("test1", "Test Pod 14", pos=(10, 130), text_color=(120, 20, 120)))
    checkgroup.add_checkbox(pyform.CheckBox("test2", "Test Pod 15", pos=(10, 170), text_color=(120, 20, 120)))
    checkgroup.add_checkbox(pyform.CheckBox("test3", "Test Pod 16", pos=(10, 210), text_color=(120, 20, 120)))
    checkgroup.add_checkbox(pyform.CheckBox("test4", "Test Pod 17", pos=(10, 250), text_color=(120, 20, 120)))

    # radio button group with 4 options
    radiogroup = pyform.RadioGroup("radiogroup")
    radiogroup.add_button(pyform.RadioButton("c1", "Choice 1", pos=(400, 10), text_color=(120, 20, 120)))
    radiogroup.add_button(pyform.RadioButton("c2", "Choice 2", pos=(400, 50), text_color=(120, 20, 120)))
    radiogroup.add_button(pyform.RadioButton("c3", "Choice 3", pos=(400, 90), text_color=(120, 20, 120)))
    radiogroup.add_button(pyform.RadioButton("c4", "Choice 4", pos=(400, 130), text_color=(120, 20, 120)))

    # form object for holding all the elements
    form = pyform.Form("main")

    # adding text boxes to the form directly
    form.add_form_object(pyform.TextInput("txt1", pos=(10, 10), default_text="First name", input_width=360,
                                          max_length=16))
    form.add_form_object(pyform.TextInput("txt2", pos=(10, 50), default_text="Last name", input_width=360,
                                          max_length=16))
    form.add_form_object(pyform.TextInput("txt3", pos=(10, 90), default_text="Age", input_width=360, max_length=4,
                                          allowed_chars=pyform.TextInput.NUMS))

    # add checkbox and radio groups
    form.add_form_object(checkgroup)
    form.add_form_object(radiogroup)
    form.on_change = p(form)

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
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill((255, 255, 255))

        # update the form
        form.update(events)
        form.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
