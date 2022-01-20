# Динозавры взяты отсюда: https://arks.itch.io/dino-characters
# Террейн отсюда стыбзил: https://pixelfrog-assets.itch.io/pixel-adventure-1
# А вот и кастомный шрифт: https://fonts-online.ru/fonts/comic-cat/download
# Логотип сделан мной лично (Адель Матыгуллин :)

import sqlite3
import pygame
import pygame_gui
import os
pygame.init()
pygame.display.set_caption("Dino Jump")
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 400, 600
FPS = 30
TILE_SIZE = 20
MOVE_EVENT_TYPE = 30
counter = 4
all_sprites = pygame.sprite.Group()
jumps = 0
in_menu = 1
which_skin = 1
manager = pygame_gui.UIManager((400, 600))
manager2 = pygame_gui.UIManager((400, 600))
manager3 = pygame_gui.UIManager((400, 600))
blue = ['data/blue1.png', 'data/blue2.png', 'data/blue3.png', 'data/blue4.png']
red = ['data/red1.png', 'data/red2.png', 'data/red3.png', 'data/red4.png']
yellow = ['data/yellow1.png', 'data/yellow2.png', 'data/yellow3.png', 'data/yellow4.png']
green = ['data/green1.png', 'data/green2.png', 'data/green3.png', 'data/green4.png']
dinosaur = 'blue'
fullname = os.path.join('data/logo.png')
image = pygame.image.load(fullname)
loading = 'data/map.txt'
skin = blue[0]
name = 'No name'
# name - имя пользователя
# jumps - количество прыжков
# loading - имя вскрываемого файла. Map, map2 - первый и второй уровни соответственно

name_enter = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((100, 100), (200, 25)),
    manager=manager)

level = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Первый уровень', 'Второй уровень'],
    starting_option='Первый уровень',
    relative_rect=pygame.Rect((100, 125), (200, 50)),
    manager=manager)

rules = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 320), (200, 50)),
    text='Правила',
    manager=manager)

play = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 255), (200, 50)),
    text='Играть!',
    manager=manager)

dino = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Синий дино', "Зелёный дино", "Жёлтый дино", "Красный дино"],
    starting_option='Синий дино',
    relative_rect=pygame.Rect((100, 190), (200, 50)),
    manager=manager)

top = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 385), (200, 50)),
    text='Топ первого уровня',
    manager=manager)

top2 = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 450), (200, 50)),
    text='Топ второго уровня',
    manager=manager)

back2 = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((100, 525), (200, 50)),
    text='В главное меню',
    manager=manager3)

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
    def __init__(self, position):
        self.x, self.y = position
        self.image = pygame.image.load(skin)
        self.delay = 200

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        global skin
        if dinosaur == 'blue':
            skin = blue[which_skin - 1]
        if dinosaur == 'red':
            skin = red[which_skin - 1]
        if dinosaur == 'green':
            skin = green[which_skin - 1]
        if dinosaur == 'yellow':
            skin = yellow[which_skin - 1]
        self.image = pygame.image.load(skin)
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
        global which_skin
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= 1
            if which_skin == 1:
                which_skin = 3
            elif which_skin == 2:
                which_skin = 4
        elif pygame.key.get_pressed()[pygame.K_d]:
            next_x += 1
            if which_skin == 3:
                which_skin = 1
            elif which_skin == 4:
                which_skin = 2
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
            if which_skin == 1:
                which_skin = 3
            elif which_skin == 2:
                which_skin = 4
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
            if which_skin == 3:
                which_skin = 1
            elif which_skin == 4:
                which_skin = 2
        if self.lab.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def move_hero(self):
        global counter, jumps, which_skin
        next_x, next_y = self.hero.get_position()
        if self.lab.is_free((next_x, next_y - 1)) and counter < 4:
            counter += 1
            if which_skin == 1:
                which_skin = 2
            elif which_skin == 3:
                which_skin = 4
            self.hero.set_position((next_x, next_y - 1))
        elif self.lab.is_free((next_x, next_y + 1)) is False:
            counter = 0
            if self.lab.is_free((next_x, next_y - 1)) and counter < 4:
                counter += 1
                jumps += 1
                if which_skin == 2:
                    which_skin = 1
                elif which_skin == 4:
                    which_skin = 3
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


def update_leaders(level_name: str, player_name: str, jumps_count: int):
    base_conn = sqlite3.connect("data/leaders.db")
    base_cursor = base_conn.cursor()
    base_cursor.execute("""CREATE TABLE IF NOT EXISTS jump_leaders(level_name text, player_name text, jumps_count
    int)""")
    base_values = (str(level_name), str(player_name), int(jumps_count))
    base_querry = "select * from jump_leaders"
    base_cursor.execute(base_querry)
    base_players = base_cursor.fetchall()
    curr_player = ()

    # это конечно, &*$!ец, но вариант с WHERE у меня почему-то не работал (
    for i in base_players:
        if str(i[1]) == player_name and str(i[0]) == level_name:
            curr_player = i
            break

    if curr_player:
        if jumps_count < int(curr_player[2]):
            # А тут работает, вот это приколы
            # Цыганские фокусы при разработке )))
            base_cursor.execute("UPDATE jump_leaders SET jumps_count=" + str(
                jumps_count) + " WHERE player_name='" + player_name + "' AND level_name='" + level_name + "'")
            base_conn.commit()
        return False
    else:

        base_cursor.execute("INSERT INTO jump_leaders VALUES(?, ?, ?);", base_values)
        base_conn.commit()
    base_cursor.close()
    base_conn.close()


def get_leaders(level_name: str) -> list:
    try:
        base_conn = sqlite3.connect("data/leaders.db")
        base_cursor = base_conn.cursor()
        base_players = "SELECT * FROM jump_leaders WHERE level_name='" + level_name + "'"
        base_cursor.execute(base_players)
        leaders_main = base_cursor.fetchall()
        if len(leaders_main) >= 15:
            leaders_main = leaders_main[0:14]
        elif not leaders_main:
            pass
        return leaders_main
    except:
        return []


def main():
    global loading, in_menu, skin, jumps, name, dinosaur
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
                    if str(jumps)[-1] == '1' and str(jumps)[-2] != '1':
                        say = 'прыжок'
                    elif str(jumps)[-1] in ['2', '3', '4']:
                        say = 'прыжка'
                    else:
                        say = 'прыжков'
                    show_message(screen, "Вы достигли финиша!", f"Это заняло {jumps} {say}!")
                    lvl_name = loading[5:-4]
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == back:
                                update_leaders(lvl_name, name, jumps)
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
                                dinosaur = 'blue'
                            elif str(event.text) == 'Зелёный дино':
                                dinosaur = 'green'
                            elif str(event.text) == 'Жёлтый дино':
                                dinosaur = 'yellow'
                            elif str(event.text) == 'Красный дино':
                                dinosaur = 'red'
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == top2:
                            in_menu = 3
                        elif event.ui_element == rules:
                            in_menu = 4
                        elif event.ui_element == top:
                            in_menu = 2
                        elif event.ui_element == play:
                            map = Map(loading, [0, 3], 3)
                            if loading == 'data/map.txt':
                                hero = Hero((10, 28))
                            else:
                                hero = Hero((10, 1))
                            game = Game(map, hero)
                            game.render(screen)
                            in_menu = 0

                    if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                        name = event.text
                        print(name)

                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        running = False

                screen.fill((255, 255, 255))
                manager.draw_ui(screen)
                screen.blit(image, (20, -140))
                font = pygame.font.Font("data\Comic_CAT.otf", 15)
                text = font.render('Введите имя (тык Enter после ввода)', True, (0, 0, 0))
                text_h = text.get_height()
                text_x = 80
                text_y = 100 - text_h - 2
                screen.blit(text, (text_x, text_y))
                if event.type == pygame.QUIT:
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((75, 200), (300, 200)),
                        manager=manager,
                        window_title='Подтверждение',
                        action_long_desc="Уверены?",
                        action_short_name='OK',
                        blocking=True
                    )

            elif in_menu == 2:
                screen.fill((255, 255, 255))
                manager3.draw_ui(screen)
                font = pygame.font.Font("data\Comic_CAT.otf", 35)
                text = font.render('Таблица лидеров', True, (0, 0, 0))
                text_x = 65
                text_y = 20
                screen.blit(text, (text_x, text_y))
                leaders_list = get_leaders("map")
                try:
                    leaders_list.sort(key=lambda x: x[2])
                    font = pygame.font.Font("data\Comic_CAT.otf", 20)
                    text_y = 80
                    leader_text_place = 1
                    if leaders_list:
                        for i in leaders_list:
                            text = font.render(f'{leader_text_place}) {i[1]} прыгнул {i[2]} раз', True, (0, 0, 0))
                            text_x = 70
                            screen.blit(text, (text_x, text_y))
                            text_y += 28
                            leader_text_place += 1
                except:
                    pass
                if event.type == pygame.QUIT:
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((75, 200), (300, 200)),
                        manager=manager,
                        window_title='Подтверждение',
                        action_long_desc="Уверены?",
                        action_short_name='OK',
                        blocking=True
                    )
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        running = False
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == back2:
                            in_menu = 1
# *Ворчит*
# А вот это мои фокусы:
            elif in_menu == 3:
                screen.fill((255, 255, 255))
                manager3.draw_ui(screen)
                font = pygame.font.Font("data\Comic_CAT.otf", 35)
                text = font.render('Таблица лидеров', True, (0, 0, 0))
                text_x = 65
                text_y = 20
                screen.blit(text, (text_x, text_y))
                leaders_list = get_leaders("map2")
                try:
                    leaders_list.sort(key=lambda x: x[2])
                    font = pygame.font.Font("data\Comic_CAT.otf", 20)
                    text_y = 80
                    leader_text_place = 1
                    if leaders_list:
                        for i in leaders_list:
                            text = font.render(f'{leader_text_place}) {i[1]} прыгнул {i[2]} раз', True, (0, 0, 0))
                            text_x = 70
                            screen.blit(text, (text_x, text_y))
                            text_y += 28
                            leader_text_place += 1
                except:
                    pass

                if event.type == pygame.QUIT:
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((75, 200), (300, 200)),
                        manager=manager,
                        window_title='Подтверждение',
                        action_long_desc="Уверены?",
                        action_short_name='OK',
                        blocking=True
                    )
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        running = False
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == back2:
                            in_menu = 1

            elif in_menu == 4:
                screen.fill((255, 255, 255))
                manager3.draw_ui(screen)
                font = pygame.font.Font("data\Comic_CAT.otf", 20)
                text = font.render('''Цель: Достичь зеленой клетки
                ''', True, (0, 0, 0))
                text_x = 20
                text_y = 20
                screen.blit(text, (text_x, text_y))
                text = font.render('''Метод достижения: Перемещение c''', True, (0, 0, 0))
                text_y = 70
                screen.blit(text, (text_x, text_y))
                text = font.render('''помощью кнопок "A" "D" или стрелок
                ''', True, (0, 0, 0))
                text_y = 100
                screen.blit(text, (text_x, text_y))
                text = font.render('''Смысл многочисленных попыток:''', True, (0, 0, 0))
                text_y = 150
                screen.blit(text, (text_x, text_y))
                text = font.render('''Получение первого места в топах
                ''', True, (0, 0, 0))
                text_y = 180
                screen.blit(text, (text_x, text_y))
                text = font.render('''Как туда попасть: Пишешь свой ник,''', True, (0, 0, 0))
                text_y = 230
                screen.blit(text, (text_x, text_y))
                text = font.render('''берёшь динозавра на свой выбор,''', True, (0, 0, 0))
                text_y = 260
                screen.blit(text, (text_x, text_y))
                text = font.render('''выбираешь уровень (второй легче!),''', True, (0, 0, 0))
                text_y = 290
                screen.blit(text, (text_x, text_y))
                text = font.render('''и начинаешь вырываться в топ!
                ''', True, (0, 0, 0))
                text_y = 320
                screen.blit(text, (text_x, text_y))
                text = font.render('''Слушать побольше:''', True, (0, 0, 0))
                text_y = 370
                screen.blit(text, (text_x, text_y))
                text = font.render('''twenty one pilots |-/''', True, (0, 0, 0))
                text_y = 400
                screen.blit(text, (text_x, text_y))
                text = font.render('''grandson ××''', True, (0, 0, 0))
                text_y = 430
                screen.blit(text, (text_x, text_y))
                text = font.render('''big baby tape''', True, (0, 0, 0))
                text_y = 460
                screen.blit(text, (text_x, text_y))
                text = font.render('''soda luv''', True, (0, 0, 0))
                text_y = 490
                screen.blit(text, (text_x, text_y))
                text = font.render('''kizaru''', True, (0, 0, 0))
                text_y = 520
                screen.blit(text, (text_x, text_y))
                if event.type == pygame.QUIT:
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((75, 200), (300, 200)),
                        manager=manager,
                        window_title='Подтверждение',
                        action_long_desc="Уверены?",
                        action_short_name='OK',
                        blocking=True
                    )
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        running = False
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == back2:
                            in_menu = 1

            manager.process_events(event)
            manager2.process_events(event)
            manager3.process_events(event)
            if game != 0:
                if game_over is True:
                    manager2.draw_ui(screen)
        manager.update(time_delta)
        manager2.update(time_delta)
        manager3.update(time_delta)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()

# А почему бы не написать сюда текст песни Коржа? )))

# Лес с деревьями до луны
# Дождь в лоб мелкими каплями
# Прогонит гостей, и среди всех своих
# Остались лишь самые стойкие
# На мятой траве, устеленной покрывалами
# Вокруг всё выпито, скурено
# Девчонка с глазами пьяными
# Ответь, что ты задумала?
# Когда я шёл на дым костра в полной луне
# По глухим местам на шорох теней
# И тут же, на мой крик друзья кричали в ответ
# Впереди сверкал пламенный свет. Эй
# Правнуки партизан в родной стихии
# Пробираются в руках с ветками сухими
# Ноги колет шишками, не одеть сандали
# Пьяные, счастливые — все по поступали
# Идейные, со взглядами
# Страну поднять продуманы планы
# А в ночном лесу, без сигарет
# Все ждут, кого-то отправили
# Когда я шёл на дым костра при полной луне
# По глухим местам на шорох теней
# И тут же, на мой крик друзья кричали в ответ
# Впереди сверкал пламенный свет. Эй
# Где же вы, мои друзья?
# С кем мечтали, с кем хотели
# Не теряться никогда, оставаться в теме
# Деньги замотали всех. Деньги заменили воздух
# И люди рядом, но уже не те
# Так знай, что никогда не поздно
# Иди на дым костра, в полной луне
# К тем глухим местам — шорох теней
# И будут там твои друзья — радостный смех
# Обними меня, пламенный свет. Эй
