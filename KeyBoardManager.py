import sys

import pygame


class KeyBoard:
    key_pressed = []
    key_up = []
    key_down = []

    @staticmethod
    def init():
        KeyBoard.key_pressed = pygame.key.get_pressed()
        KeyBoard.key_up = [KeyBoard.key_pressed[i] for i in range(len(KeyBoard.key_pressed))]
        KeyBoard.key_down = [KeyBoard.key_pressed[i] for i in range(len(KeyBoard.key_pressed))]

    @staticmethod
    def update_key():
        k = pygame.key.get_pressed()
        KeyBoard.key_up = [not k[i] and KeyBoard.key_pressed[i] for i in range(len(KeyBoard.key_pressed))]
        KeyBoard.key_down = [k[i] and not KeyBoard.key_pressed[i] for i in range(len(KeyBoard.key_pressed))]
        KeyBoard.key_pressed = k

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
