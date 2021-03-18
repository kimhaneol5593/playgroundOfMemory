import pygame, time, sys


game_start = True


def run():
    pygame.init()
    image_path = "assets/image/main/"

    # 이미지
    pacmanBtn = pygame.image.load(image_path + "pacmanBtn.png")
    shootingBtn = pygame.image.load(image_path + "shootingBtn.png")
    flappyBtn = pygame.image.load(image_path + "flappyBtn.png")
    rabbitBtn = pygame.image.load(image_path + "rabbitBtn.png")
    snakeBtn = pygame.image.load(image_path + "snakeBtn.png")
    rhythmBtn = pygame.image.load(image_path + "rhythmBtn.png")
    carBtn = pygame.image.load(image_path + "carBtn.png")
    puzzleBtn = pygame.image.load(image_path + "puzzleBtn.png")
    tetrisBtn = pygame.image.load(image_path + "tetrisBtn.png")
    minesBtn = pygame.image.load(image_path + "minesBtn.png")
    pingpongBtn = pygame.image.load(image_path + "pingpongBtn.png")

    pacmanBtn2 = pygame.image.load(image_path + "pacmanBtn2.png")
    shootingBtn2 = pygame.image.load(image_path + "shootingBtn2.png")
    flappyBtn2 = pygame.image.load(image_path + "flappyBtn2.png")
    rabbitBtn2 = pygame.image.load(image_path + "rabbitBtn2.png")
    snakeBtn2 = pygame.image.load(image_path + "snakeBtn2.png")
    rhythmBtn2 = pygame.image.load(image_path + "rhythmBtn2.png")
    carBtn2 = pygame.image.load(image_path + "carBtn2.png")
    puzzleBtn2 = pygame.image.load(image_path + "puzzleBtn2.png")
    tetrisBtn2 = pygame.image.load(image_path + "tetrisBtn2.png")
    minesBtn2 = pygame.image.load(image_path + "minesBtn2.png")
    pingpongBtn2 = pygame.image.load(image_path + "pingpongBtn2.png")

    # 화면 설정
    display_width = 1030
    display_height = 750
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("추억놀이터")

    # Button 클래스
    class GameBtn:
        def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x + width > mouse[0] > x and y + height > mouse[1] > y:
                gameDisplay.blit(img_act, (x_act, y_act))
                if click[0] and action is not None:
                    time.sleep(1)
                    action()
            else:
                gameDisplay.blit(img_in, (x, y))

    # 게임 종료
    def quitgame():
        pygame.quit()
        sys.exit()

    # 메뉴 화면
    def mainmenu():
        menu = True

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitgame()

            bg_surface = pygame.image.load(image_path + 'background.png').convert()
            bg_surface = pygame.transform.scale2x(bg_surface)
            gameDisplay.blit(bg_surface, (0, 0))

            GameBtn(pacmanBtn, 120, 170, 198, 119, pacmanBtn2, 125, 175, pacmanRun)
            GameBtn(shootingBtn, 320, 170, 198, 119, shootingBtn2, 325, 175, shootingRun)
            GameBtn(flappyBtn, 520, 170, 198, 119, flappyBtn2, 525, 175, flappyRun)
            GameBtn(rabbitBtn, 720, 170, 198, 119, rabbitBtn2, 725, 175, rabbitRun)

            GameBtn(snakeBtn, 120, 300, 198, 119, snakeBtn2, 125, 305, snakeRun)
            GameBtn(rhythmBtn, 320, 300, 198, 119, rhythmBtn2, 325, 305, rhythmRun)
            GameBtn(carBtn, 520, 300, 198, 119, carBtn2, 525, 305, carRun)
            GameBtn(puzzleBtn, 720, 300, 198, 119, puzzleBtn2, 725, 305, puzzleRun)

            GameBtn(tetrisBtn, 200, 430, 198, 119, tetrisBtn2, 205, 435, tetrisRun)
            GameBtn(minesBtn, 420, 430, 198, 119, minesBtn2, 425, 435, minesRun)
            GameBtn(pingpongBtn, 640, 430, 198, 119, pingpongBtn2, 645, 435, TTRun)
            pygame.display.update()

    # 선택 화면
    def snakeRun():
        from game import snake
        snake.run()

    def pacmanRun():
        from game import pacman
        pacman.run()

    def rhythmRun():
        from game import rhythm
        rhythm.run()

    def flappyRun():
        from game import flappy
        flappy.run()

    def shootingRun():
        from game import shooting
        shooting.run()

    def rabbitRun():
        from game import rabbit
        rabbit.run()

    def carRun():
        from game import carGame
        carGame.run()

    def puzzleRun():
        from game import puzzleGame
        puzzleGame.run()

    def tetrisRun():
        from game import tetris
        tetris.run()

    def minesRun():
        from game import minesweeper
        minesweeper.run()

    def TTRun():
        from game import pingpong
        pingpong.run()

    mainmenu()


if game_start:
    game_start = False
    run()
