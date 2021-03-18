import pygame, random



def run():
    pygame.init()

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (213, 50, 80)
    blue = (50, 153, 213)

    # 화면 사이즈 지정
    dis_width = 600
    dis_height = 400

    dis = pygame.display.set_mode((dis_width, dis_height))

    clock = pygame.time.Clock()

    snake_block = 10
    snake_speed = 10

    font_style = pygame.font.SysFont("bahnschrift", 20)
    score_font = pygame.font.SysFont("comicsansms", 35)

    def Your_score(score):
        value = score_font.render("Score: " + str(score), True, black)
        dis.blit(value, [0, 0])

    # 뱀 그리기 함수
    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

    # 메세지 출력용 함수
    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])

    def gameLoop():
        game_over = False
        game_close = False

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        while not game_over:
            # 뱀이 벽에 닿았을 때
            while game_close == True:
                dis.fill(white)
                message("Game Over! Play Again: Press C Quit: Press Q", red)

                Your_score(Length_of_snake - 1)
                pygame.display.update()

                # 게임 start or 게임 종료
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop()
            # 방향키로 움직이기
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    import gameStart
                    gameStart.run()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(white)
            pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1

            clock.tick(snake_speed)

        import gameStart
        gameStart.run()

    gameLoop()
