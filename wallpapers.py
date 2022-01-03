import pygame
import pygame_gui as gui
import copy

import sys
import os

from CONSTANTS import *

# Словарь, содержащий все нужные символы в качестве ключей. Первый элемент массива, являющимся значением к ключу -
# это количество пикселей, которое занимает нарисованный вариант символа в ширину.
font = {'A': [3], 'B': [3], 'C': [3], 'D': [3], 'E': [3], 'F': [3], 'G': [3], 'H': [3],
        'I': [3], 'J': [3],
        'K': [3], 'L': [3], 'M': [5], 'N': [3], 'O': [3], 'P': [3], 'Q': [3], 'R': [3],
        'S': [3], 'T': [3],
        'U': [3], 'V': [3], 'W': [5], 'X': [3], 'Y': [3], 'Z': [3],
        'a': [3], 'b': [3], 'c': [3], 'd': [3], 'e': [3], 'f': [3], 'g': [3], 'h': [3],
        'i': [1], 'j': [2],
        'k': [3], 'l': [3], 'm': [5], 'n': [3], 'o': [3], 'p': [3], 'q': [3], 'r': [2],
        's': [3], 't': [3],
        'u': [3], 'v': [3], 'w': [5], 'x': [3], 'y': [3], 'z': [3],
        '.': [1], '-': [3], ',': [2], ':': [1], '+': [3], '\'': [1], '!': [1], '?': [3],
        '0': [3], '1': [3], '2': [3], '3': [3], '4': [3], '5': [3], '6': [3], '7': [3],
        '8': [3], '9': [3],
        '(': [2], ')': [2]}


def generate_custom_font(image, fnt, color, block_width=5, block_height=8, barrier=1):
    """
    Функция генерирует кастомный шрифт, нарисованный по пикселям.

    :param image:   картинка с нарисованными символами;
    :param fnt:     словарь с символами;
    :param color:   цвет шрифта;
    :param block_width:   ширина ячейки с символом;
    :param block_height:  высота ячейки с символом;
    :param barrier: толщина перегородки между символами на рисунке;
    :return:
    """

    # создаем копию словаря с символами, чтобы не изменять исходный вариант
    all_symbols = copy.deepcopy(fnt)

    # создаем дополнительный холст, для нанесения "трафарета" из символов кастомного шрифта
    extra_surface = pygame.Surface(image.get_size()).convert()
    extra_surface.fill(color)
    extra_surface.blit(image, (0, 0))

    image = extra_surface.copy()
    image.set_colorkey((255, 255, 255))

    num = 0

    for char in all_symbols.keys():
        image.set_clip(pygame.Rect(((block_width + barrier) * num), 0, block_width, block_height))
        symbol_image = image.subsurface(image.get_clip())

        all_symbols[char].append(symbol_image)
        num += 1

    all_symbols['Height'] = block_height

    return all_symbols


def render_text(text, margin_x, margin_y, spacing, max_width, font, screen):
    """
    Функция рендерит заданный текст с кастомным шрифтом.

    :param text:        текст для вывода;
    :param margin_x:    величина горизонтального отступа от левой границы холста;
    :param margin_y:    величина вертикального отступа от верхней границы холста;
    :param spacing:     расстояние между символами;
    :param max_width:   максимальная длина строки(в пикселях);
    :param font:        шрифт;
    :param screen:      холст;
    :return:
    """

    text += ' '
    origin_x = margin_x
    word = ''

    for char in text:
        if char not in [' ', '\n']:
            try:
                image = font[str(char)][1]
                word += char
            except KeyError:
                pass
        else:
            # длина слова(в пикселях) вместе с символами пустой строки и пропусками
            word_length = sum(map(lambda s: font[s][0] + spacing, word))

            if char == ' ':
                # пробел занимает 3 пикселя
                margin_x += 3 + spacing

            # отображаем символы по одному в положенном месте на экране
            for sym in word:
                image = font[sym][1]
                screen.blit(image, (margin_x, margin_y))
                margin_x += font[sym][0] + spacing

            word = ''
            if char == '\n' or word_length + margin_x - origin_x > max_width:
                margin_x = origin_x
                margin_y += font['Height']

        if margin_x - origin_x > max_width:
            margin_x = origin_x
            margin_y += font['Height']


# ---- Функция показывает заставку, когда игрок начал новую игру ----
# P.S. ФУНКЦИЯ НЕ ГОТОВА
def start_screen(screen, font):
    intro_text = """Вы астронавт-любитель, пытающийся найти драгоценности в открытом космосе. 
    Но в один момент вы сталкиваетесь с целой бандой пиратов, и, стараясь оторваться от них, 
    улетаете в неразведанные места. При попытке сделать трюк вокруг системы планет что-то 
    пошло не по плану: вы слишком близко подлетели к одной из них и не смогли справиться с силой притяжения. 
    После падения ваш корабль сильно пострадал, поэтому вам нужно как можно скорее восстановить 
    его и продолжить свой путь."""

    command_text = "Нажмите любую клавишу на клавиатуре, чтобы продолжить."

    render_text(intro_text, 10, 20, 1, 500, font, screen)
    render_text(command_text, 100, 300, 1, 500, font, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        CLOCK.tick(FPS)


def main_menu(screen, manager):
    background = load_image('all_image(shallow water).png')

    big_font_picture = pygame.transform.scale(load_image('Fonts/font.png', color_key=(0, 0, 0)), (2586, 48))
    title_font = generate_custom_font(big_font_picture, font, (255, 254, 255),
                                      block_width=30, block_height=48, barrier=6)
    screen.blit(background, (0, 0))

    # ---- кнопки в главном меню ----
    new_game_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((420, 320), (100, 50)),
        text="НОВАЯ ИГРА",
        manager=manager
    )
    continue_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((550, 320), (100, 50)),
        text="ПРОДОЛЖИТЬ",
        manager=manager
    )
    exit_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((680, 320), (100, 50)),
        text="ВЫЙТИ",
        manager=manager
    )
    settings_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((810, 320), (100, 50)),
        text="НАСТРОЙКИ",
        manager=manager
    )
    # ---- кнопки в главном меню ----

    # ---- цикл главного меню ----
    while True:
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == new_game_button:
                        pass
                    if event.ui_element == continue_button:
                        return False
                    if event.ui_element == settings_button:
                        pass
                    if event.ui_element == exit_button:
                        sys.exit()
            manager.process_events(event)

        manager.update(tick)
        manager.draw_ui(screen)
        render_text("IMMERSED", 370, 200, 60, 1000, title_font, screen)
        pygame.display.flip()
        CLOCK.tick(FPS)

# custom_font = generate_custom_font(load_image('Fonts/font.png'), font, (255, 254, 255))
