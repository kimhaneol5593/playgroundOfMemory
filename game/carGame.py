import pygame
from random import randint



def run():
    pygame.font.init()
    pygame.mixer.init()
    image_path = 'assets/image/carGame/'
    sound_path = 'assets/sound/'

    def player():
        screen.blit(cars_img[0], (player_x - int(car_x / 2), player_y - int(car_y / 2)))

    def enemies():
        screen.blit(cars_img[1], (enemies_x - 115, enemy1_y))
        screen.blit(cars_img[2], (enemies_x - int(car_x / 2), enemy2_y))
        screen.blit(cars_img[3], (enemies_x + 60, enemy3_y))

    def text(txt_msg, txt_color, txt_size, txt_x, txt_y):
        font = pygame.font.SysFont('arial', txt_size, True)
        txt = font.render(txt_msg, True, txt_color)
        screen.blit(txt, (txt_x, txt_y))

    'COLORS (RGB)'
    white = (255, 255, 255)
    black = (0, 0, 0)

    'WINDOW'
    wid, hei = 400, 500
    screen = pygame.display.set_mode((wid, hei))

    'SPRITE SIZE'
    car_x, car_y = 54, 94

    'PLAYER'
    player_x, player_y = int(wid / 2), int(hei - 50)
    player_spd = 5

    'ENEMIES'
    enemies_x = int(wid / 2)
    enemy1_y = randint(-hei, -car_y)
    enemy2_y = randint(-hei, -car_y)
    enemy3_y = randint(-hei, -car_y)
    enemies_spd = 0

    'IMAGES'
    bg = pygame.image.load(image_path + 'Road.png').convert()
    bg = pygame.transform.scale(bg, (wid, hei))
    bg_y = 0
    cars_img = [pygame.image.load(image_path + 'Player_Car.png'),
                pygame.image.load(image_path + 'Enemy1_Car.png'),
                pygame.image.load(image_path + 'Enemy2_Car.png'),
                pygame.image.load(image_path + 'Enemy3_Car.png')]

    'MUSIC'
    pygame.mixer_music.load(sound_path + 'Chillwave_Nightdrive.mp3')
    pygame.mixer_music.play(-1)

    'SOUND EFFECT'
    car_collision = pygame.mixer.Sound(sound_path + 'Car_Collision.wav')

    clock = pygame.time.Clock()
    score = 1
    score_spd = 0
    main = True

    while main:
        clock.tick(60)
        bg_y1 = bg_y % bg.get_height()
        bg_y += 3
        screen.blit(bg, (0, bg_y1 - bg.get_height()))
        if bg_y1 < hei:
            screen.blit(bg, (0, bg_y1))

        player()
        enemies()

        pygame.draw.rect(screen, white, (0, 0, 54, 20))
        text('S: ' + str(score), black, 15, 0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False

        'CONTROLS'
        arrows = pygame.key.get_pressed()
        if arrows[pygame.K_RIGHT] and player_x <= 290:
            player_x += player_spd
        if arrows[pygame.K_LEFT] and player_x >= 110:
            player_x -= player_spd
        if arrows[pygame.K_UP] and player_y >= 40:
            player_y -= player_spd
        if arrows[pygame.K_DOWN] and player_y <= 440:
            player_y += player_spd

        'ENEMIES SPEED'
        enemy1_y += enemies_spd + 5
        enemy2_y += enemies_spd + 2
        enemy3_y += enemies_spd + 4

        if enemy1_y > hei:
            enemy1_y = randint(-2500, - 2000)
        if enemy2_y > hei:
            enemy2_y = randint(-1000, -750)
        if enemy3_y > hei:
            enemy3_y = randint(-1750, -1250)

        'SCORE'
        if score_spd <= 60:
            score_spd += 1
        else:
            score += 1
            score_spd = 0

        'COLLISION'
        if player_x - 40 > enemies_x and player_y - 140 < enemy3_y:
            if player_x - 40 > enemies_x and player_y > enemy3_y:
                car_collision.play()
                score -= 10
                enemy3_y = randint(-1750, -1250)
        if player_x + 40 < enemies_x and player_y - 140 < enemy1_y:
            if player_x + 40 < enemies_x and player_y > enemy1_y:
                car_collision.play()
                score -= 10
                enemy1_y = randint(-2500, - 2000)
        if player_x - 40 < enemies_x + 10 and player_y - 140 < enemy2_y:
            if player_x + 40 > enemies_x - 10 and player_y - 140 < enemy2_y:
                if player_x + 40 > enemies_x - 10 and player_y > enemy2_y:
                    if player_x - 40 < enemies_x - 10 and player_y > enemy2_y:
                        car_collision.play()
                        score -= 10
                        enemy2_y = randint(-1000, -750)

        if score <= 0:
            break

        pygame.display.update()

    pygame.quit()
    import gameStart
    gameStart.run()
