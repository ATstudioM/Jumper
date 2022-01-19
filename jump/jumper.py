# Динозавры взяты отсюда: https://arks.itch.io/dino-characters
# Террейн отсюда стыбзил: https://pixelfrog-assets.itch.io/pixel-adventure-1
# А вот и кастомный шрифт: https://fonts-online.ru/fonts/comic-cat/download

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
in_menu = True
manager = pygame_gui.UIManager((800, 600))
fullname = os.path.join('data/logo.png')
image = pygame.image.load(fullname)


level = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Первый уровень', 'Второй уровень', 'Третий уровень'],
    starting_option='Первый уровень',
    relative_rect=pygame.Rect((100, 200), (200, 50)),
    manager=manager)

rules = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 275), (200, 50)),
    text='Правила',
    manager=manager)

play = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 350), (200, 50)),
    text='Играть!',
    manager=manager)


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
        self.lab.render(screen)
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
    screen = pygame.display.set_mode(WINDOW_SIZE)
    hero = Hero("data/DinoSprites_doux.gif", (10, 28))
    map = Map('data/map.txt', [0, 3], 3)
    game = Game(map, hero)
    map.render()
    clock = pygame.time.Clock()
    time_delta = clock.tick(60) / 1000.0
    running = True
    pygame.time.set_timer(MOVE_EVENT_TYPE, 100)
    game_over = False
    while running:
        for event in pygame.event.get():
            if in_menu is not True:
                if event.type == pygame.QUIT:
                    running = False
                if game.check_win():
                    game_over = True
                    screen.fill((255, 255, 255))
                    all_sprites.draw(screen)
                    hero.render(screen)
                    show_message(screen, "Вы достигли вершины!", f"Это заняло {jumps} прыжка(ов)!")
                elif event.type == MOVE_EVENT_TYPE:
                    game.move_hero()
                if not game_over:
                    screen.fill((255, 255, 255))
                    all_sprites.draw(screen)
                    game.update_hero()
                    hero.render(screen)
            else:
                screen.fill((255, 255, 255))
                manager.draw_ui(screen)
                screen.blit(image, (20, - 50))
                if event.type == pygame.QUIT:
                    running = False
            manager.process_events(event)
        manager.update(time_delta)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
