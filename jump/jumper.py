# Динозавры взяты отсюда: https://arks.itch.io/dino-characters
# Террейн отсюда стыбзил: https://pixelfrog-assets.itch.io/pixel-adventure-1
# А вот и кастомный шрифт: https://fonts-online.ru/fonts/comic-cat/download
# Логотип сделан мной лично (Адель Матыгуллин :)

import pygame
import pygame_gui
import os

pygame.init()
pygame.display.set_caption("Jumper")
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 400, 600
FPS = 30
TILE_SIZE = 20
MOVE_EVENT_TYPE = 30
counter = 4
all_sprites = pygame.sprite.Group()
jumps = 0
in_menu = 1
manager = pygame_gui.UIManager((400, 600))
manager2 = pygame_gui.UIManager((400, 600))
fullname = os.path.join('data/logo.png')
image = pygame.image.load(fullname)
loading = 'data/map.txt'
skin = "data/DinoSprites_doux.gif"
name = 'No name'
# name - имя пользователя
# jumps - количество прыжков
# loading - имя вскрываемого файла. Map, map2 - первый и второй уровни соответственно

name_enter = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((100, 110), (200, 25)),
    manager=manager)

level = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Первый уровень', 'Второй уровень'],
    starting_option='Первый уровень',
    relative_rect=pygame.Rect((100, 150), (200, 50)),
    manager=manager)

rules = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 375), (200, 50)),
    text='Правила',
    manager=manager)

play = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 300), (200, 50)),
    text='Играть!',
    manager=manager)

dino = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Синий дино', "Зелёный дино", "Жёлтый дино", "Красный дино"],
    starting_option='Синий дино',
    relative_rect=pygame.Rect((100, 225), (200, 50)),
    manager=manager)


top = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 450), (200, 50)),
    text='Топ первого уровня',
    manager=manager)

top2 = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 525), (200, 50)),
    text='Топ второго уровня',
    manager=manager)

back = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 375), (200, 50)),
    text='В главное меню',
    manager=manager2)


class Map:

    def __init__(self, filename, free_tile, finish_tile):
        self.map = []
        with open(f"{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tile
        self.finish_tile = finish_tile

    def render(self):
        colors = {0: 'brown.png', 1: 'block.png', 2: 'grass.png', 3: 'green.png'}
        for y in range(self.height):
            for x in range(self.width):
                background = pygame.sprite.Sprite()
                background.image = pygame.image.load('data/' + (colors[self.get_tile_id((x, y))]))
                background.rect = background.image.get_rect()
                background.rect.x = x * 20
                background.rect.y = y * 20
                all_sprites.add(background)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, pos):
        return self.get_tile_id(pos) in self.free_tiles


class Hero:

    def __init__(self, pic, position):
        self.x, self.y = position
        self.image = pygame.image.load(f"{pic}")
        self.delay = 200

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Game:

    def __init__(self, labyrinth, hero):
        self.lab = labyrinth
        self.hero = hero

    def render(self, screen):
        self.lab.render()
        self.hero.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= 1
        elif pygame.key.get_pressed()[pygame.K_d]:
            next_x += 1
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if self.lab.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def move_hero(self):
        global counter, jumps
        next_x, next_y = self.hero.get_position()
        if self.lab.is_free((next_x, next_y - 1)) and counter < 4:
            counter += 1
            self.hero.set_position((next_x, next_y - 1))
        elif self.lab.is_free((next_x, next_y + 1)) is False:
            counter = 0
            if self.lab.is_free((next_x, next_y - 1)) and counter < 4:
                counter += 1
                jumps += 1
                self.hero.set_position((next_x, next_y - 1))
        elif self.lab.is_free((next_x, next_y + 1)):
            counter = 5
            self.hero.set_position((next_x, next_y + 1))

    def check_win(self):
        return str(self.lab.get_tile_id(self.hero.get_position())) == '3'


def show_message(screen, message, message2):
    global jumps
    font = pygame.font.Font("data\Comic_CAT.otf", 30)
    text = font.render(message, True, (255, 255, 255))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = WINDOW_WIDTH // 2 - text_w // 2
    text_y = WINDOW_HEIGHT // 2 - text_h // 2
    pygame.draw.rect(screen, (252, 202, 78), (text_x - 200, text_y - 10, text_w + 400, text_h + 50))
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font("data\Comic_CAT.otf", 30)
    text = font.render(message2, True, (255, 255, 255))
    text_y = text_y + 30
    text_x = text_x - 40
    screen.blit(text, (text_x, text_y))


def main():
    global loading, in_menu, skin, jumps, name
    screen = pygame.display.set_mode(WINDOW_SIZE)
    hero = 0
    game = 0
    clock = pygame.time.Clock()
    time_delta = clock.tick(60) / 1000.0
    running = True
    pygame.time.set_timer(MOVE_EVENT_TYPE, 100)
    game_over = False
    while running:
        for event in pygame.event.get():
            if in_menu == 0:
                if event.type == pygame.QUIT:
                    running = False
                if game.check_win():
                    game_over = True
                    all_sprites.draw(screen)
                    hero.render(screen)
                    show_message(screen, "Вы достигли финиша!", f"Это заняло {jumps} прыжка(ов)!")
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == back:
                                game_over = False
                                in_menu = 1
                                jumps = 0
                elif event.type == MOVE_EVENT_TYPE:
                    game.move_hero()
                if not game_over:
                    screen.fill((255, 255, 255))
                    all_sprites.draw(screen)
                    game.update_hero()
                    hero.render(screen)
            elif in_menu == 1:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == level:
                            if str(event.text) == 'Первый уровень':
                                loading = 'data/map.txt'
                            elif str(event.text) == 'Второй уровень':
                                loading = 'data/map2.txt'
                        elif event.ui_element == dino:
                            if str(event.text) == 'Синий дино':
                                skin = "data/DinoSprites_doux.gif"
                            elif str(event.text) == 'Зелёный дино':
                                skin = "data/DinoSprites_vita.gif"
                            elif str(event.text) == 'Жёлтый дино':
                                skin = "data/DinoSprites_tard.gif"
                            elif str(event.text) == 'Красный дино':
                                skin = "data/DinoSprites_mort.gif"
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == play:
                            map = Map(loading, [0, 3], 3)
                            if loading == 'data/map.txt':
                                hero = Hero(skin, (10, 28))
                            else:
                                hero = Hero(skin, (10, 1))
                            game = Game(map, hero)
                            game.render(screen)
                            in_menu = 0
                    if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                        name = event.text
                        print(name)
                screen.fill((255, 255, 255))
                manager.draw_ui(screen)
                screen.blit(image, (20, -140))
                font = pygame.font.Font("data\Comic_CAT.otf", 15)
                text = font.render('Введите имя (тык Enter после ввода)', True, (0, 0, 0))
                text_h = text.get_height()
                text_x = 80
                text_y = 110 - text_h - 2
                screen.blit(text, (text_x, text_y))
                if event.type == pygame.QUIT:
                    running = False
            manager.process_events(event)
            manager2.process_events(event)
            if game != 0:
                if game.check_win() is True:
                    manager2.draw_ui(screen)
        manager.update(time_delta)
        manager2.update(time_delta)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
