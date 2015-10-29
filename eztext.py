from pygame.locals import *
import pygame


class Input(object):
    """ A text input for pygame apps """

    unshifted_keys = {K_a: 'a', K_b: 'b', K_c: 'c', K_d: 'd', K_e: 'e', K_f: 'f', K_g: 'g', K_h: 'h', K_i: 'i',
                      K_j: 'j', K_k: 'k', K_l: 'l', K_m: 'm', K_n: 'n', K_o: 'o', K_p: 'p', K_q: 'q', K_r: 'r',
                      K_s: 's', K_t: 't', K_u: 'u', K_v: 'v', K_w: 'w', K_x: 'x', K_y: 'y', K_z: 'z', K_0: '0',
                      K_1: '1', K_2: '2', K_3: '3', K_4: '4', K_5: '5', K_6: '6', K_7: '7', K_8: '8', K_9: '9',
                      K_BACKQUOTE: '`', K_MINUS: '-', K_EQUALS: '=', K_LEFTBRACKET: '[', K_RIGHTBRACKET: ']',
                      K_BACKSLASH: '\\', K_SEMICOLON: ';', K_QUOTE: '\'', K_COMMA: ',', K_PERIOD: '.', K_SLASH: '/',
                      K_SPACE: ' '}

    shifted_keys = {K_a: 'A', K_b: 'B', K_c: 'C', K_d: 'D', K_e: 'E', K_f: 'F', K_g: 'G', K_h: 'H', K_i: 'I', K_j: 'J',
                    K_k: 'K', K_l: 'L', K_m: 'M', K_n: 'N', K_o: 'O', K_p: 'P', K_q: 'Q', K_r: 'R', K_s: 'S', K_t: 'T',
                    K_u: 'U', K_v: 'V', K_w: 'W', K_x: 'X', K_y: 'Y', K_z: 'Z', K_0: ')', K_1: '!', K_2: '@', K_3: '#',
                    K_4: '$', K_5: '%', K_6: '^', K_7: '&', K_8: '*', K_9: '(', K_BACKQUOTE: '~', K_MINUS: '_',
                    K_EQUALS: '+', K_LEFTBRACKET: '{', K_RIGHTBRACKET: '}', K_BACKSLASH: '|', K_SEMICOLON: ':',
                    K_QUOTE: '"', K_COMMA: '<', K_PERIOD: '>', K_SLASH: '?', K_SPACE: ' '}

    ALPHA = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    NUMS = "0123456789"
    ALPHA_NUMS = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    ALL_CHARS = " !\"#$%&\\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

    def __init__(self, pos=(0, 0), text_color=(0, 0, 0), input_width=100, max_length=-1, allowed_chars=ALL_CHARS,
                 prompt="", default_text="", set_key_repeat_speed=False, font=None):
        """ Options: x, y, font, color, unrestricted, max_length, prompt """

        pygame.init()

        self._pos = pos
        self.text_color = text_color
        self.input_width = input_width
        self.max_length = max_length
        self.allowed_chars = set(allowed_chars)
        self.prompt = prompt
        self.default_text = default_text
        if set_key_repeat_speed:
            pygame.key.set_repeat(150, 30)
        if font is None:
            self.font = pygame.font.Font(None, 32)
        else:
            self.font = font

        self.rendered_prompt = self.font.render(self.prompt, 1, self.text_color)
        self.prompt_size = self.rendered_prompt.get_size()
        self.input_pad = self.font.render(' ', 1, self.text_color).get_width() / 2
        self.input_box = None
        self.focus_area = None
        self._recalculate_boxes()

        self.focused = False
        self.text = ""
        self.shifted = 0
        self.alt = 0
        self.meta = 0
        self._locked = False

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._recalculate_boxes()

    def _recalculate_boxes(self):
        self.input_box = pygame.Rect(self.x + self.prompt_size[0], self.y, self.input_width + self.input_pad * 2,
                                     self.prompt_size[1])
        self.focus_area = pygame.Rect(self.x, self.y, self.input_width + self.input_pad * 2 + self.prompt_size[0],
                                      self.prompt_size[1])

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = value
        if self._locked:
            self.focused = False

    def toggle_lock(self):
        self.locked = not self.locked

    def draw(self, surface):
        """ Draw the text input to a surface """

        surface.blit(self.rendered_prompt, (self.x, self.y))

        # background
        if not self.locked:
            pygame.draw.rect(surface, (252, 252, 252), self.input_box)
        else:
            pygame.draw.rect(surface, (235, 235, 235), self.input_box)

        if self.focused:
            pygame.draw.rect(surface, (58, 117, 255), self.input_box, 1)
        else:
            pygame.draw.rect(surface, (208, 208, 208), self.input_box, 1)
            pygame.draw.line(surface, (169, 169, 169), (self.x + self.prompt_size[0], self.y),
                             (self.x + self.prompt_size[0] + self.input_width + self.input_pad * 2 - 2, self.y))

        if self.text == "" and not self.focused:
            rendered_text = self.font.render(self.default_text, 1, (180, 180, 180))
        else:
            rendered_text = self.font.render(self.text, 1, self.text_color)

        surface.blit(rendered_text, (self.x + self.prompt_size[0] + self.input_pad, self.y))

    def update(self, events):
        """ Update the input based on passed events """

        if self.locked:
            return

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.focused = self.focus_area.collidepoint(event.pos)
            elif event.type == KEYUP:
                self._update_modifier_level(event, -1)
            elif event.type == KEYDOWN:
                self._update_modifier_level(event, 1)

                if not self.focused:
                    continue

                self._handle_backspace(event)

                self._add_key(event)

    def _update_modifier_level(self, event, delta):
        if event.key == K_LSHIFT or event.key == K_RSHIFT:
            self.shifted += delta
            self.shifted = max(self.shifted, 0)
        elif event.key == K_LALT or event.key == K_RALT:
            self.alt += delta
            self.alt = max(self.alt, 0)
        elif event.key == K_LMETA or event.key == K_RMETA:
            self.meta += delta
            self.meta = max(self.meta, 0)

    def _handle_backspace(self, event):
        if event.key == K_BACKSPACE and self.meta > 0:
            self.text = ""
        elif event.key == K_BACKSPACE and self.alt > 0:
            self.text = self.text.rstrip()
            self.text = self.text[:self.text.rfind(' ') + 1]
        elif event.key == K_BACKSPACE and self.meta == 0:
            self.text = self.text[:-1]

    def _add_key(self, event):
        if len(self.text) == self.max_length >= 0:
            return

        if self.shifted:
            key = self.shifted_keys.get(event.key, '')
        else:
            key = self.unshifted_keys.get(event.key, '')

        if key in self.allowed_chars:
            self.text += key
