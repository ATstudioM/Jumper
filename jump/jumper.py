import pygame
# import os

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 400, 600
FPS = 30
TILE_SIZE = 20
MOVE_EVENT_TYPE = 30
counter = 4


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

    def render(self, screen):
        colors = {0: (255, 255, 255, 200), 1: (0, 0, 0), 2: (255, 0, 0)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

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
        global counter
        next_x, next_y = self.hero.get_position()
        if self.lab.is_free((next_x, next_y - 1)) and counter < 4:
            counter += 1
            self.hero.set_position((next_x, next_y - 1))
        elif self.lab.is_free((next_x, next_y + 1)) is False:
            counter = 0
            if self.lab.is_free((next_x, next_y - 1)) and counter < 4:
                counter += 1
                self.hero.set_position((next_x, next_y - 1))
        elif self.lab.is_free((next_x, next_y + 1)):
            counter = 5
            self.hero.set_position((next_x, next_y + 1))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    hero = Hero("data/DinoSprites_doux.gif", (13, 28))
    map = Map('data/map.txt', [0, 2], 2)
    game = Game(map, hero)
    clock = pygame.time.Clock()
    running = True
    pygame.time.set_timer(MOVE_EVENT_TYPE, 200)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOVE_EVENT_TYPE:
                game.move_hero()
        game.update_hero()
        map.render(screen)
        hero.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
