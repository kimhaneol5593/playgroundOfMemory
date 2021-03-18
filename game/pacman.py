import pygame
from random import *



def run():
    PLAYER_SIZE = 20
    WALL_SIZE = 5
    MAP_SIZE = [350, 390]
    VELOCITY_1 = 4
    VELOCITY_2 = 2

    class Pickup(pygame.sprite.Sprite):

        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface([5, 5])
            self.image.fill([255, 255, 255])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Enemy(pygame.sprite.Sprite):

        def __init__(
                self,
                x,
                y,
                color,
        ):
            super().__init__()
            self.color = color
            self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.direction = [0, VELOCITY_1]
            self.moves = [False, True, True, False]
            self.edible = False
            self.wait = False
            self.waitcount = 0
            self.speed = VELOCITY_1

        def move(self, level):
            if self.wait:
                self.waitcount += 1
                if self.waitcount == 30 * 3:
                    self.rect.x = WALL_SIZE + 8 * PLAYER_SIZE
                    self.rect.y = WALL_SIZE + 6 * PLAYER_SIZE
                    self.wait = False
                    self.change_color(self.color)
                    self.edible = False
            else:
                if self.edible:
                    if max(abs(self.direction[0]), abs(self.direction[1])) \
                            == VELOCITY_1 and (self.rect.x - WALL_SIZE) \
                            % PLAYER_SIZE == 0 and (self.rect.y - WALL_SIZE) \
                            % PLAYER_SIZE == 0:
                        self.direction[0] = self.direction[0] * VELOCITY_2 \
                                            / VELOCITY_1
                        self.direction[1] = self.direction[1] * VELOCITY_2 \
                                            / VELOCITY_1
                else:
                    if max(abs(self.direction[0]), abs(self.direction[1])) \
                            == VELOCITY_2 and (self.rect.x - WALL_SIZE) \
                            % PLAYER_SIZE == 0 and (self.rect.y - WALL_SIZE) \
                            % PLAYER_SIZE == 0:
                        self.direction[0] = self.direction[0] * VELOCITY_1 \
                                            / VELOCITY_2
                        self.direction[1] = self.direction[1] * VELOCITY_1 \
                                            / VELOCITY_2
                if (self.rect.x - WALL_SIZE) % PLAYER_SIZE == 0 \
                        and (self.rect.y - WALL_SIZE) % PLAYER_SIZE == 0:
                    choices = []
                    self.rect.x += self.direction[0]
                    self.rect.y += self.direction[1]
                    hitlist = pygame.sprite.spritecollide(self, level.wall_list, False)
                    if not hitlist:
                        choices.append([self.direction[0], self.direction[1]] * 2)
                    self.rect.x -= self.direction[0]
                    self.rect.y -= self.direction[1]
                    self.rect.x += self.direction[1]
                    self.rect.y += self.direction[0]
                    hitlist = pygame.sprite.spritecollide(self, level.wall_list, False)
                    if not hitlist:
                        choices.append([self.direction[1], self.direction[0]] * 2)
                    self.rect.x -= self.direction[1]
                    self.rect.y -= self.direction[0]
                    self.rect.x -= self.direction[1]
                    self.rect.y -= self.direction[0]
                    hitlist = pygame.sprite.spritecollide(self, level.wall_list, False)
                    if not hitlist:
                        choices.append([-self.direction[1], -self.direction[0]] * 2)
                    self.rect.x += self.direction[1]
                    self.rect.y += self.direction[0]
                    a = randrange(0, len(choices))
                    self.rect.x += choices[a][0]
                    self.rect.y += choices[a][1]
                    self.direction = [choices[a][0], choices[a][1]]
                else:
                    self.rect.x += self.direction[0]
                    self.rect.y += self.direction[1]
                if self.rect.x > MAP_SIZE[0]:
                    self.rect.x = 0 - PLAYER_SIZE + WALL_SIZE
                elif self.rect.x < 0 - PLAYER_SIZE:
                    self.rect.x = MAP_SIZE[0] - WALL_SIZE

        def change_color(self, color):
            self.image.fill(color)

    class Player(pygame.sprite.Sprite):

        def __init__(
                self,
                x,
                y,
                radius,
        ):
            super().__init__()
            self.image = pygame.Surface([radius, radius])
            self.image.fill([250, 250, 0])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.queue = [-VELOCITY_1, 0]
            self.direction = [-VELOCITY_1, 0]

        def change_direction(self, x, y):
            self.queue = [x, y]

        def move(self, level):
            self.rect.x += self.queue[0]
            self.rect.y += self.queue[1]
            hitlist = pygame.sprite.spritecollide(self, level.wall_list, False)
            if hitlist:
                self.rect.x -= self.queue[0]
                self.rect.y -= self.queue[1]
                self.rect.x += self.direction[0]
                self.rect.y += self.direction[1]
                seclist = pygame.sprite.spritecollide(self, level.wall_list, False)
                if seclist:
                    self.rect.x -= self.direction[0]
                    self.rect.y -= self.direction[1]
            else:
                self.direction[0] = self.queue[0]
                self.direction[1] = self.queue[1]

            if self.rect.x < -PLAYER_SIZE:
                self.rect.x = MAP_SIZE[0] - WALL_SIZE
                self.rect.y = self.rect.y
            if self.rect.x > MAP_SIZE[0]:
                self.rect.x = WALL_SIZE

    class Text:

        def __init__(
                self,
                x,
                y,
                size,
        ):
            self.x = x
            self.y = y
            self.size = size

        def update(self, screen, text):
            cover = pygame.Surface([len(text) * self.size // 2.1, self.size * 0.7])
            cover.fill([0, 0, 30])
            screen.blit(cover, (self.x, self.y))
            myscore = pygame.font.Font(None, self.size)
            label = myscore.render(text, True, (255, 255, 255))
            textrect = (self.x, self.y)
            screen.blit(label, textrect)

    class EatableSwap(pygame.sprite.Sprite):

        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface([10, 10])
            self.image.fill([100, 255, 100])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Map:

        def __init__(self):
            buttons = [EatableSwap(WALL_SIZE + PLAYER_SIZE / 2 - 5,
                                   WALL_SIZE + 1.5 * PLAYER_SIZE - 5),
                       EatableSwap(WALL_SIZE + 16.5 * PLAYER_SIZE - 5,
                                   WALL_SIZE + 1.5 * PLAYER_SIZE - 5),
                       EatableSwap(WALL_SIZE + PLAYER_SIZE / 2 - 5,
                                   WALL_SIZE + 17.5 * PLAYER_SIZE - 5),
                       EatableSwap(WALL_SIZE + 16.5 * PLAYER_SIZE - 5,
                                   WALL_SIZE + 17.5 * PLAYER_SIZE - 5)]
            self.button_list = pygame.sprite.Group()
            for i in buttons:
                self.button_list.add(i)
            enemies = [Enemy(WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 6 * PLAYER_SIZE, [255, 0, 0]),
                       Enemy(WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 6 * PLAYER_SIZE, [0, 255, 0]),
                       Enemy(WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 6 * PLAYER_SIZE, [0, 255, 255]),
                       Enemy(WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 6 * PLAYER_SIZE, [125, 0, 125])]
            self.enemy_list = pygame.sprite.Group()
            for i in enemies:
                self.enemy_list.add(i)
            food = [[WALL_SIZE + PLAYER_SIZE / 2 - 2.5 + PLAYER_SIZE * (i
                                                                        % 17),
                     WALL_SIZE + PLAYER_SIZE / 2 - 2.5 + i // 17
                     * PLAYER_SIZE] for i in range(17 * 19)]
            remove = [
                [1, 1],
                [3, 1],
                [4, 1],
                [6, 1],
                [7, 1],
                [8, 1],
                [9, 1],
                [10, 1],
                [12, 1],
                [13, 1],
                [15, 1],
                [1, 2],
                [6, 2],
                [10, 2],
                [15, 2],
                [1, 3],
                [2, 3],
                [4, 3],
                [6, 3],
                [10, 3],
                [12, 3],
                [14, 3],
                [15, 3],
                [8, 3],
                [4, 4],
                [8, 4],
                [12, 4],
                [0, 5],
                [2, 5],
                [3, 5],
                [4, 5],
                [5, 5],
                [6, 5],
                [8, 5],
                [10, 5],
                [11, 5],
                [12, 5],
                [13, 5],
                [14, 5],
                [16, 5],
                [0, 6],
                [4, 6],
                [12, 6],
                [16, 6],
                [2, 7],
                [4, 7],
                [12, 7],
                [14, 7],
                [0, 8],
                [1, 8],
                [2, 8],
                [14, 8],
                [15, 8],
                [16, 8],
                [2, 9],
                [4, 9],
                [12, 9],
                [14, 9],
                [0, 10],
                [4, 10],
                [12, 10],
                [16, 10],
                [0, 11],
                [2, 11],
                [4, 11],
                [5, 11],
                [6, 11],
                [8, 11],
                [10, 11],
                [11, 11],
                [12, 11],
                [14, 11],
                [16, 11],
                [0, 12],
                [2, 12],
                [8, 12],
                [14, 12],
                [16, 12],
                [0, 13],
                [2, 13],
                [3, 13],
                [4, 13],
                [6, 13],
                [8, 13],
                [10, 13],
                [12, 13],
                [13, 13],
                [14, 13],
                [16, 13],
                [6, 14],
                [10, 14],
                [1, 15],
                [2, 15],
                [4, 15],
                [6, 15],
                [7, 15],
                [8, 15],
                [9, 15],
                [10, 15],
                [12, 15],
                [14, 15],
                [15, 15],
                [1, 16],
                [4, 16],
                [12, 16],
                [15, 16],
                [1, 17],
                [3, 17],
                [4, 17],
                [5, 17],
                [6, 17],
                [8, 17],
                [10, 17],
                [11, 17],
                [12, 17],
                [13, 17],
                [15, 17],
                [8, 18],
                [6, 9],
                [7, 9],
                [8, 9],
                [9, 9],
                [10, 9],
                [6, 8],
                [7, 8],
                [8, 8],
                [9, 8],
                [10, 8],
                [6, 7],
                [7, 7],
                [8, 7],
                [9, 7],
                [10, 7],
                [0, 1],
                [16, 1],
            ]
            for i in remove:
                food[i[0] + 17 * i[1]] = 1
            self.food_list = pygame.sprite.Group()
            for i in food:
                if i != 1:
                    item = Pickup(i[0], i[1])
                    self.food_list.add(item)
            walls = [
                [WALL_SIZE + 6 * PLAYER_SIZE, WALL_SIZE + 7 * PLAYER_SIZE,
                 5 * PLAYER_SIZE, WALL_SIZE],
                [WALL_SIZE + 6 * PLAYER_SIZE, WALL_SIZE + 7 * PLAYER_SIZE,
                 WALL_SIZE, 3 * PLAYER_SIZE],
                [11 * PLAYER_SIZE, WALL_SIZE + 7 * PLAYER_SIZE, WALL_SIZE,
                 3 * PLAYER_SIZE],
                [WALL_SIZE + 6 * PLAYER_SIZE, WALL_SIZE + 10 * PLAYER_SIZE
                 - WALL_SIZE, 5 * PLAYER_SIZE, WALL_SIZE],
                [0, 0, MAP_SIZE[0], 5],
                [0, 0, 5, 2 * WALL_SIZE + 5 * PLAYER_SIZE],
                [0, WALL_SIZE + 5 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE,
                 WALL_SIZE],
                [PLAYER_SIZE, WALL_SIZE + 5 * PLAYER_SIZE, WALL_SIZE, 2
                 * PLAYER_SIZE],
                [0, 7 * PLAYER_SIZE, PLAYER_SIZE + WALL_SIZE, WALL_SIZE],
                [0, MAP_SIZE[1] - 5, MAP_SIZE[0], 5],
                [MAP_SIZE[0] - 5, 0, 5, 2 * WALL_SIZE + 5 * PLAYER_SIZE],
                [MAP_SIZE[0] - WALL_SIZE - PLAYER_SIZE, WALL_SIZE + 5
                 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE, WALL_SIZE],
                [MAP_SIZE[0] - PLAYER_SIZE - WALL_SIZE, WALL_SIZE + 5
                 * PLAYER_SIZE, WALL_SIZE, 2 * PLAYER_SIZE],
                [MAP_SIZE[0] - PLAYER_SIZE - WALL_SIZE, 7 * PLAYER_SIZE,
                 PLAYER_SIZE + WALL_SIZE, WALL_SIZE],
                [MAP_SIZE[0] - PLAYER_SIZE - WALL_SIZE, WALL_SIZE + 10
                 * PLAYER_SIZE, WALL_SIZE, 4 * PLAYER_SIZE],
                [MAP_SIZE[0] - PLAYER_SIZE - WALL_SIZE, 14 * PLAYER_SIZE,
                 PLAYER_SIZE + WALL_SIZE, WALL_SIZE],
                [MAP_SIZE[0] - PLAYER_SIZE - WALL_SIZE, 10 * PLAYER_SIZE
                 + WALL_SIZE, PLAYER_SIZE + WALL_SIZE, WALL_SIZE],
                [0, WALL_SIZE + 10 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE,
                 WALL_SIZE],
                [PLAYER_SIZE, WALL_SIZE + 10 * PLAYER_SIZE, WALL_SIZE, 4
                 * PLAYER_SIZE],
                [0, 14 * PLAYER_SIZE, PLAYER_SIZE + WALL_SIZE, WALL_SIZE],
                [0, 14 * PLAYER_SIZE, WALL_SIZE, 5 * PLAYER_SIZE
                 + WALL_SIZE],
                [MAP_SIZE[0] - WALL_SIZE, 14 * PLAYER_SIZE, WALL_SIZE, 5
                 * PLAYER_SIZE + WALL_SIZE],
            ]
            self.wall_list = pygame.sprite.Group()
            innerWalls = [
                [WALL_SIZE + PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 3 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE, 2
                 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 6 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE, 5
                 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 12 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE, 2
                 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 15 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + PLAYER_SIZE, WALL_SIZE + 3 * PLAYER_SIZE, 2
                 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 6 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 10 * PLAYER_SIZE, WALL_SIZE + PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 3 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 4 * PLAYER_SIZE, WALL_SIZE + 3 * PLAYER_SIZE,
                 PLAYER_SIZE, 5 * PLAYER_SIZE],
                [WALL_SIZE + 12 * PLAYER_SIZE, WALL_SIZE + 3 * PLAYER_SIZE,
                 PLAYER_SIZE, 5 * PLAYER_SIZE],
                [WALL_SIZE + 14 * PLAYER_SIZE, WALL_SIZE + 3 * PLAYER_SIZE,
                 2 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 2 * PLAYER_SIZE, WALL_SIZE + 5 * PLAYER_SIZE,
                 5 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 10 * PLAYER_SIZE, WALL_SIZE + 5 * PLAYER_SIZE,
                 5 * PLAYER_SIZE, PLAYER_SIZE],
                [0, WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 3
                 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 14 * PLAYER_SIZE, WALL_SIZE + 8 * PLAYER_SIZE,
                 WALL_SIZE + 3 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 2 * PLAYER_SIZE, WALL_SIZE + 7 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 14 * PLAYER_SIZE, WALL_SIZE + 7 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 4 * PLAYER_SIZE, WALL_SIZE + 9 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 12 * PLAYER_SIZE, WALL_SIZE + 9 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 4 * PLAYER_SIZE, WALL_SIZE + 11 * PLAYER_SIZE,
                 3 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 10 * PLAYER_SIZE, WALL_SIZE + 11
                 * PLAYER_SIZE, 3 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 11 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 2 * PLAYER_SIZE, WALL_SIZE + 11 * PLAYER_SIZE,
                 PLAYER_SIZE, 2 * PLAYER_SIZE],
                [WALL_SIZE + 14 * PLAYER_SIZE, WALL_SIZE + 11
                 * PLAYER_SIZE, PLAYER_SIZE, 2 * PLAYER_SIZE],
                [WALL_SIZE + 2 * PLAYER_SIZE, WALL_SIZE + 13 * PLAYER_SIZE,
                 3 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 12 * PLAYER_SIZE, WALL_SIZE + 13
                 * PLAYER_SIZE, 3 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 10 * PLAYER_SIZE, WALL_SIZE + 13
                 * PLAYER_SIZE, PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 6 * PLAYER_SIZE, WALL_SIZE + 13 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 6 * PLAYER_SIZE, WALL_SIZE + 15 * PLAYER_SIZE,
                 5 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 17 * PLAYER_SIZE,
                 PLAYER_SIZE, 2 * PLAYER_SIZE],
                [WALL_SIZE + 3 * PLAYER_SIZE, WALL_SIZE + 17 * PLAYER_SIZE,
                 4 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 10 * PLAYER_SIZE, WALL_SIZE + 17
                 * PLAYER_SIZE, 4 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 4 * PLAYER_SIZE, WALL_SIZE + 15 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 12 * PLAYER_SIZE, WALL_SIZE + 15
                 * PLAYER_SIZE, PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + PLAYER_SIZE, WALL_SIZE + 15 * PLAYER_SIZE, 2
                 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + 14 * PLAYER_SIZE, WALL_SIZE + 15
                 * PLAYER_SIZE, 2 * PLAYER_SIZE, PLAYER_SIZE],
                [WALL_SIZE + PLAYER_SIZE, WALL_SIZE + 15 * PLAYER_SIZE,
                 PLAYER_SIZE, 3 * PLAYER_SIZE],
                [WALL_SIZE + 15 * PLAYER_SIZE, WALL_SIZE + 15
                 * PLAYER_SIZE, PLAYER_SIZE, 3 * PLAYER_SIZE],
            ]
            for i in walls:
                wall = Wall(i[0], i[1], i[2], i[3])
                self.wall_list.add(wall)
            for i in innerWalls:
                wall = Wall(i[0], i[1], i[2], i[3])
                self.wall_list.add(wall)

    class Wall(pygame.sprite.Sprite):

        def __init__(
                self,
                x,
                y,
                width,
                height,
        ):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill([0, 0, 125])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # - Starting the main game class
    def window():
        pygame.init()

        # - Using the cl_vars for the window
        screen = pygame.display.set_mode([MAP_SIZE[0], MAP_SIZE[1] + 70])
        # - Creating the player class
        player = Player(WALL_SIZE + 8 * PLAYER_SIZE, WALL_SIZE + 14 * PLAYER_SIZE, PLAYER_SIZE)
        entities = pygame.sprite.Group()
        entities.add(player)
        clock = pygame.time.Clock()
        score_count = Text(210, 410, 35)
        score_label = Text(70, 410, 35)
        level_map = Map()
        score_value = 0
        enemy_value = 200
        for i in range(3):
            # - Pretty much the main game loop
            # This is a lot simpler than the other game cause its pacman
            done = False
            edible = False
            count = 0
            # - Calculating FPS
            while not done:
                count += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        import gameStart
                        gameStart.run()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            player.change_direction(-4, 0)
                        elif event.key == pygame.K_RIGHT:
                            player.change_direction(4, 0)
                        elif event.key == pygame.K_DOWN:
                            player.change_direction(0, 4)
                        elif event.key == pygame.K_UP:
                            player.change_direction(0, -4)
                        elif event.key == pygame.K_SPACE:
                            unpause = False
                            while not unpause:
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                            unpause = True
                for i in level_map.enemy_list:
                    i.move(level_map)
                # - Drawing, THIS SHOULD BE MOVED TO SEPERATE FUNCTION
                player.move(level_map)
                screen.fill([0, 0, 30])
                score_label.update(screen, 'Score: ')
                score_count.update(screen, str(score_value))
                level_map.button_list.draw(screen)
                level_map.wall_list.draw(screen)
                level_map.food_list.draw(screen)
                level_map.enemy_list.draw(screen)
                entities.draw(screen)
                foodlist = pygame.sprite.spritecollide(player,
                                                       level_map.food_list, False)
                if edible:
                    if count == 30 * 6:
                        enemy_value = 200
                        edible = False
                        for i in level_map.enemy_list:
                            i.change_color(i.color)
                            i.edible = False
                    elif count > 30 * 3:
                        for i in level_map.enemy_list:
                            if i.edible:
                                if count % 15 == 0 or count % 15 == 1:
                                    i.change_color([150, 255, 150])
                                elif count % 15 == 2:
                                    i.change_color([60, 60, 225])
                for i in foodlist:
                    score_value += 10
                    level_map.food_list.remove(i)
                buttonlist = pygame.sprite.spritecollide(player,
                                                         level_map.button_list, False)
                if buttonlist:
                    edible = True
                    count = 0
                    for i in buttonlist:
                        level_map.button_list.remove(i)
                    for i in level_map.enemy_list:
                        i.change_color([60, 60, 255])
                        i.edible = True
                enemylist = pygame.sprite.spritecollide(player,
                                                        level_map.enemy_list, False)
                if enemylist:
                    if enemylist[0].edible:
                        score_value += enemy_value
                        enemy_value *= 2
                        enemylist[0].waitcount = 0
                        enemylist[0].wait = True
                        enemylist[0].rect.y = WALL_SIZE + 8 * PLAYER_SIZE
                        enemylist[0].rect.x = WALL_SIZE + 8 * PLAYER_SIZE
                        enemylist[0].change_color(enemylist[0].color)
                        enemylist[0].edible = False
                    else:
                        done = True
                pygame.display.flip()
                clock.tick(30)
            player.rect.x = WALL_SIZE + 8 * PLAYER_SIZE
            player.rect.y = WALL_SIZE + 14 * PLAYER_SIZE
            for i in level_map.enemy_list:
                i.change_color(i.color)
                i.rect.x = WALL_SIZE + 8 * PLAYER_SIZE
                i.rect.y = WALL_SIZE + 6 * PLAYER_SIZE
            enemy_value = 200
            clock.tick(2 / 3)
        import gameStart
        gameStart.run()

    window()
