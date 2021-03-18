import os
import sys
from glob import glob
from random import shuffle, choice, randrange

import pygame

from functions.grab import grab
from functions.menu import menu
from functions.soundsinit import init


def run():
    image_path = 'assets/image/puzzle/'
    sound_path = 'assets/sound/'

    def harmonic_color(image):
        "Returns a random color from image"
        w, h = image.get_size()
        color = image.get_at((randrange(0, w // 2), randrange(0, h // 2)))
        return color

    def floor(num_to_round):
        "Return a rounded number. Ex.: 510 => 500; 36 => 30"
        str_num = str(num_to_round)
        lenstr = len(str_num)
        str_num = ["1"]
        print(str_num)
        for n in range(1, lenstr):
            str_num.append("0")
            print(str_num)
        str_num = "".join(str_num)
        str_num = int(str_num)
        flr = num_to_round // str_num * str_num
        return flr

    class Puzzle:
        tiles_fixed = 0
        score = 0
        sounds, winsounds = init(sound_path)
        image = pygame.image.load(choice(glob(image_path + "\\*.png")))
        w, h = image.get_size()
        w = floor(w)
        h = floor(h)
        screen = pygame.display.set_mode((w * 3 - w // 2 + 14, h))
        pygame.display.set_caption("Puzzle-mania 2.6")
        image.convert()
        bar = pygame.Surface((7, h))
        bar.fill(harmonic_color(image))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 24)
        font2 = pygame.font.SysFont("Arial", 20)
        # pygame.event.set_grab(True)
        maxscore = 0
        ### colors
        BLACKTILE = (harmonic_color(image))

        def __init__(self, file):
            self.file = file
            self.load_maxscore()

        def file_is_empty(self):
            "If a file is empty True"
            with open(self.file, "r") as file_check:
                f = file_check.read()
            if f == "":
                return True
            else:
                return False

        def savescore(self):
            if int(Puzzle.score) > int(Puzzle.maxscore):
                self.write_maxscore(str(int(Puzzle.score)))

        def write_maxscore(self, score):
            "Write in the score.txt file"
            with open(self.file, "w") as file:
                file.write(str(score))
                Puzzle.maxscore = score

        def read_maxscore(self):
            with open(self.file, "r") as file_saved:
                last_maxscore = int(file_saved.read())
                print("Maxscore = " + str(last_maxscore))
                return last_maxscore

        def file_exists(self):
            "Check if file exists"
            if self.file in os.listdir():
                return True
            else:
                return False

        def first_score(self):
            "Create a new file for the score"
            self.write_maxscore("10")

        def load_maxscore(self):
            ''' check if a file exists
                    if exists
                        if is empty: it writes 10 in it
                        else it reads the score as an integer
                    else: create and write 10
            '''
            if self.file_exists():
                if not self.file_is_empty():
                    # This reads the score and put in Puuzzle.maxscore
                    Puzzle.maxscore = int(self.read_maxscore())
                else:
                    self.first_score()
            else:
                self.first_score()

    def start_again():
        '''This is called when you hit space, it resets the value to fit the new
        The separator will always be in color with the image'''
        global blacktile

        Puzzle.image = pygame.image.load(choice(glob(image_path + "\\*.png")))
        Puzzle.w, Puzzle.h = Puzzle.image.get_size()
        Puzzle.w = floor(Puzzle.w)
        Puzzle.h = floor(Puzzle.h)
        Tile.w = Puzzle.w // 10
        Tile.h = Puzzle.h // 10
        bar = pygame.Surface((7, Puzzle.h))
        Puzzle.screen = pygame.display.set_mode((Puzzle.w * 3 + 14 - Puzzle.w // 2, Puzzle.h))
        Puzzle.image.convert()
        Puzzle.bar.fill(harmonic_color(Puzzle.image))
        blacktile = pygame.Surface((Tile.w, Tile.h))
        blacktile.fill(harmonic_color(Puzzle.image))

    class Tile:
        w = Puzzle.w // 10
        h = Puzzle.h // 10

    def check_if_ok(tile3, tile1, numtile):
        global rects3, puzzle3, puzzle

        # Check if the images are the same (same color)
        uguale = 0
        for pxh in range(Tile.h):
            for pxw in range(Tile.w):
                if tile3.get_at((pxw, pxh)) == tile1.get_at((pxw, pxh)):
                    uguale += 1
                else:
                    # if there is one pixel that is different it quits
                    # they are not equal, so break - avoid time consuming
                    break
        pixels = Tile.h * Tile.w

        ###########################################################################
        #                          YOU PUT IT IN THE RIGHT SPOT                   #
        ###########################################################################

        if pixels == uguale:
            pygame.mixer.pause()
            pygame.mixer.Sound.play(choice(Puzzle.winsounds))

            Puzzle.score += 25
            brighten = 32
            tile3.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
            puzzle3[numtile][1] = tile3
            puzzle[numtile][1] = tile3
            # Another tile fixed correctly
            Puzzle.tiles_fixed += 1
        else:
            Puzzle.score -= 1

        # Check if the puzzle is finished
        if Puzzle.tiles_fixed == (Puzzle.w // Tile.w) * (Puzzle.h // Tile.h) - 1:
            Puzzle.image = pygame.image.load(choice(glob(image_path + "/*.png")))
            create_puzzle()
            show_puzzle()

    def blit(part, x, y):
        "Show something on the window"
        Puzzle.screen.blit(part, (x, y))

    def play(snd):
        pygame.mixer.Sound.play(Puzzle.sounds[snd])

    def get_coords(event):
        global coords

        mousex, mousey = event
        mx = ((mousex - 7 - Puzzle.w // 2) // Tile.w) * Tile.w
        my = (mousey // Tile.h) * Tile.h
        for coord in coords:
            # if the mouse touches a tile that has the same coordinates
            if coord[1] == mx and coord[2] == my:
                # show the number of the tile
                # print(coord[0])
                # print(puzzle[coord[0]])
                return coord

    def get_coords2(event):
        "Returns the coordinates of the piece you leave on the table"
        global coords
        # mouse coordinates
        mousex, mousey = event
        # transform coordinates into
        mx = ((mousex - 14 - Puzzle.w - Puzzle.w // 2) // Tile.w) * Tile.w
        my = (mousey // Tile.h) * Tile.h
        print(mx, my)
        # In coord we have all the coordinates of the first correct puzzle
        for coord in coords:
            # if the mouse touches a tile that has the same coordinates
            if coord[1] == mx and coord[2] == my:
                # show the number of the tile
                # print(coord[0])
                # print(puzzle[coord[0]])
                return coord

    blacktile = pygame.Surface((Tile.w, Tile.h))
    blacktile.fill(Puzzle.BLACKTILE)

    class Event_listener():
        "How to exit from the game"
        global coords, dragging, puzzle2, blacktile, puzzle3
        drag = 0
        # tile = pygame.Surface((Tile.w, Tile.h))
        p2pos = 0
        # see in which quadro you picked the tile
        pos3 = False

        def check(self):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pyzzlemania.savescore()
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pyzzlemania.savescore()
                        self.quit()
                    if event.key == pygame.K_SPACE:
                        # show_puzzle(shuffled=1)
                        myimage = choice(glob(image_path + "/*.png"))
                        Puzzle.image = pygame.image.load(myimage)
                        start_again()
                        create_puzzle()
                        show_puzzle()
                    if event.key == pygame.K_s:
                        pygame.mixer.music.unload()
                    if event.key == pygame.K_m:
                        pygame.mixer.music.unload()
                        music()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # right mouse - flip horizzontally

                    if event.button == 3:
                        Puzzle.score -= 1
                        x, y = event.pos
                        if x > Puzzle.w // 2 and x < Puzzle.w * 2 - Puzzle.w // 2:
                            coord = get_coords(event.pos)
                            puzzle2[coord[0]][1] = pygame.transform.flip(puzzle2[coord[0]][1], 1, 0)
                        if x > Puzzle.w * 2 - Puzzle.w // 2:
                            coord2 = get_coords2(event.pos)
                            if puzzle[coord2[0]][1] != puzzle3[coord2[0]][1]:
                                puzzle3[coord2[0]][1] = pygame.transform.flip(puzzle3[coord2[0]][1], 1, 0)
                                check_if_ok(puzzle[coord2[0]][1], puzzle3[coord2[0]][1], coord2[0])

                    # middle button - flip vertically when scroll

                    if event.button == 4 or event.button == 5:
                        Puzzle.score -= 1
                        x, y = event.pos
                        if x > Puzzle.w // 2 and x < Puzzle.w * 2 - Puzzle.w // 2:
                            coord = get_coords(event.pos)
                            puzzle2[coord[0]][1] = pygame.transform.flip(puzzle2[coord[0]][1], 0, 1)
                        if x > Puzzle.w * 2 - Puzzle.w // 2:
                            coord2 = get_coords2(event.pos)
                            if puzzle[coord2[0]][1] != puzzle3[coord2[0]][1]:
                                puzzle3[coord2[0]][1] = pygame.transform.flip(puzzle3[coord2[0]][1], 0, 1)
                                check_if_ok(puzzle[coord2[0]][1], puzzle3[coord2[0]][1], coord2[0])

                    if event.button == 1:
                        play("click")
                        # Until you press you will see the image
                        # under the mouse arrow icon
                        Event_listener.drag = 1
                        x, y = event.pos
                        # Avoid working out of the middle area
                        if x > Puzzle.w // 2 + 7 and x < Puzzle.w * 2 - Puzzle.w // 2 + 7:
                            coord = get_coords(event.pos)
                            if puzzle2[coord[0]][1] == blacktile:
                                Event_listener.drag = 0

                            # if y > 0 and y < Puzzle.h:
                            else:
                                # check if the mouse is over a tile and
                                # get it into Event...tile
                                puzzle_get = puzzle2[coord[0]][1]
                                Event_listener.tile = puzzle_get
                                puzzle2[coord[0]][1] = blacktile
                                # Memorizzo la posizione del tile
                                Event_listener.p2pos = coord[0]
                                show_puzzle2()
                                Event_listener.pos3 = False
                                # print(coord)
                                # blit(blacktile, coord[1] + Puzzle.w, coord[2])
                                # blit(puzzle2[coord[0]][1], event.pos[0], event.pos[1])
                                # print(coord[0])

                        #                                        #
                        #            Clicco nel 3o quadrante     #
                        #                                        #
                        elif x > Puzzle.w * 2 - Puzzle.w // 2 + 7:  # and x < Puzzle.w * 3 - Puzzle.w // 2:
                            # coord2 = [num, x, y]
                            coord2 = get_coords2(event.pos)
                            # you picked the tile in the 3rd quadro
                            if puzzle[coord2[0]][1] == puzzle3[coord2[0]][1] or puzzle3[coord2[0]][1] == blacktile:
                                Event_listener.drag = 0
                            else:
                                Event_listener.pos3 = True
                                Event_listener.p3pos = coord2[0]
                                # Prendo l'immagine nel puzzle 3 alle coord
                                # coord2[0][0] è il numero del tile
                                # coord2[0][1] + la surface
                                tile_in_3o = puzzle3[coord2[0]][1]
                                # Memorizza il tile appena cliccato
                                Event_listener.tile = tile_in_3o
                                # mette un tile bianco al posto del tile preso nello schermo 2
                                puzzle3[coord2[0]][1] = blacktile
                                # drag è sempre 1, quindi dovrebbe funzionare il "lascito"

                                coord2 = get_coords2(event.pos)
                                if puzzle3[coord2[0]][1] == blacktile:
                                    puzzle_get = puzzle3[coord2[0]][1]


                # QUANDO RILASCIO IL PULSANTE
                # NON C'è PIù il trascinamento drag = 0
                # Se mi trovo nel quadro 3 => rilascio i tile nella nuova pos
                # altrimenti rimetto il tile nel puzzle 2

                # BUGFIX: when you mouse up on many tile the tile disappear

                elif event.type == pygame.MOUSEBUTTONUP:
                    if Event_listener.drag:
                        play("click")
                        Puzzle.score -= 1

                        if event.pos[0] > Puzzle.w // 2 + Puzzle.w + 14:
                            Event_listener.drag = 0
                            # See where you are leaving the piece
                            coord2 = get_coords2(event.pos)
                            # Number of the tile where you are putting the piece
                            casella = puzzle3[coord2[0]]
                            tile3 = casella[1]
                            if tile3 == blacktile:
                                # Se cìè un black tile è vuoto e Molla il pezzo
                                Event_listener.drag = 0
                                # In quel posto metto il pezzo in memoria
                                # come coordinata metto...
                                puzzle3[coord2[0]][1] = Event_listener.tile
                                # Controlla se l'immagine nella posizione è
                                # uguale a quella della posizione originale nel puzzle 1
                                check_if_ok(Event_listener.tile, puzzle[coord2[0]][1], coord2[0])
                                # if Event_listener.tile == puzzle[coord2[0]][1]:
                                #     play("joy")


                            elif Event_listener.pos3:
                                puzzle3[Event_listener.p3pos][1] = Event_listener.tile
                            else:
                                self.back_in_place()

                        # ho indentato questo else per fixare il bug del tile scomparso
                        else:
                            # Rimette il pezzo preso nel primo spazio vuoto
                            # del puzzle 2
                            self.back_in_place()

        def back_in_place(self):
            for n, tile in enumerate(puzzle2):
                if tile[1] == blacktile:
                    Event_listener.drag = 0
                    puzzle2[n][1] = Event_listener.tile
                    break

        def quit(self):
            "Quite pygame and the python interpreter"
            import gameStart
            gameStart.run()
            sys.exit()

    def create_puzzle():
        "Take the image and makes a puzzle, returns list of pieces and coordinates"
        global puzzle, puzzle2, puzzle3
        global coords, origcoords

        puzzle = []
        puzzle2 = []  # this will be shuffled
        puzzle3 = []
        coords = []
        blit(Puzzle.image, 0, 0)
        pygame.display.update()
        order = 0
        for m in range(Puzzle.h // Tile.h):
            for n in range(Puzzle.w // Tile.w):
                # grab returns a Surface object
                tile = grab(Puzzle.screen, n * Tile.w, m * Tile.h, Tile.w, Tile.h)
                puzzle.append([order, tile])
                if randrange(0, 2):
                    if randrange(0, 2):
                        tile = pygame.transform.flip(tile, 1, 0)
                    else:
                        tile = pygame.transform.flip(tile, 0, 1)
                puzzle2.append([order, tile])
                puzzle3.append([order, blacktile])
                # The coordinates of the tiles
                coords.append([order, n * Tile.w, m * Tile.h])
                order += 1
        # for n, x, y in coords:
        #     puzzle[2] = (x, y)
        shuffle(puzzle2)
        origcoords = coords[:]

    def show_puzzle(shuffled=0):
        "This shows the puzzle, if sfl=1, shuffles it"
        global puzzle, coords, origcoords

        rects = []
        if shuffled == 1:
            # randomize the positions of the tiles
            coords1 = coords[:]
            shuffle(coords)
        else:
            coords = origcoords[:]
        screen1 = pygame.Surface((Puzzle.w // 2, Puzzle.h // 2))
        n = 0
        for num_tile, x, y in coords:
            # The tiles are half the normal size
            screen1.blit(pygame.transform.scale(puzzle[n][1], (Tile.w // 2, Tile.h // 2)), (x // 2, y // 2))
            rects.append(pygame.Rect(x + Puzzle.w, y, Tile.w // 2, Tile.h // 2))
            n += 1
        # Puzzle.screen.blit(pygame.transform.scale(screen1, (Puzzle.w // 4, Puzzle.h // 4)), (0, 0))
        Puzzle.screen.blit(screen1, (0, 0))

    def show_puzzle2():
        global puzzle2

        rects2 = []
        n = 0
        # the coords=[[0, 50, 0], [1, 100, 0]...]
        for num_tile, x, y in coords:
            blit(puzzle2[n][1], x + Puzzle.w // 2 + 7, y)
            rects2.append(pygame.Rect(x + Puzzle.w // 2 + 7, y, Tile.w, Tile.h))
            n += 1
        draw_grid()

    def show_puzzle3():
        global puzzle3

        rects3 = []
        n = 0
        # the coords=[[0, 50, 0], [1, 100, 0]...]
        # Create a surface half of the Puzzle.image (Puzzle.w // 2 e Puzzle.h // 2)

        for num_tile, x, y in coords:
            blit(puzzle3[n][1], x + Puzzle.w * 2 - Puzzle.w // 2 + 14, y)
            rects3.append(pygame.Rect(x + Puzzle.w * 2 - Puzzle.w // 2 + 14, y, Tile.w, Tile.h))
            n += 1
        draw_grid2()

    def draw_grid():
        "Draws the grid 10x10 for 40x50 tiles"

        def draw_horizzontal():
            x = Puzzle.w // 2 + 7  # sempre uguale a 500
            y = n * Tile.h
            w = Puzzle.w * 2 + 7 - Puzzle.w // 2
            h = n * Tile.h
            pygame.draw.line(Puzzle.screen, (0, 0, 0), (x, y), (w, h), 2)

        def draw_vertical():
            xv = Puzzle.w // 2 + 7 + n * Tile.w  # Parte da 500 + 50 ... 100...
            yv = 0  # parte sempre da altezza 0 (top)
            wv = Puzzle.w // 2 + 7 + n * Tile.w  # parte da 500 e aggiunge 50 x 10 = 500
            hv = Puzzle.h  # altezza 500
            pygame.draw.line(Puzzle.screen, (0, 0, 0), (xv, yv), (wv, hv), 2)

        for n in range(10):
            draw_horizzontal()
            draw_vertical()

    def draw_grid2():
        "Draws the grid 10x10 for 40x50 tiles"

        def draw_horizzontal():
            x = Puzzle.w * 2 - Puzzle.w // 2 + 14  # sempre uguale a 500
            y = n * Tile.h  # va in basso di 50, 100...
            w = Puzzle.w * 3 - Puzzle.w // 2 + 14  # ascissa 2 = 1500
            h = n * Tile.h  # ordinata come sopra 50, 100...
            pygame.draw.line(Puzzle.screen, (128, 128, 128, 64), (x, y), (w, h), 1)

        def draw_vertical():
            xv = Puzzle.w * 2 - Puzzle.w // 2 + 14 + n * Tile.w  # Parte da 112800 + 50 ... 100...
            yv = 0  # parte sempre da altezza 0 (top)
            wv = Puzzle.w * 2 - Puzzle.w // 2 + 14 + n * Tile.w  # parte da 1000 e aggiunge 50 x 10 = 500
            hv = Puzzle.h  # altezza 500
            pygame.draw.line(Puzzle.screen, (128, 128, 128, 128), (xv, yv), (wv, hv), 1)

        for n in range(10):
            draw_horizzontal()
            draw_vertical()

    def show_sol():
        create_puzzle()
        show_puzzle2()

    def bars():
        Puzzle.screen.blit(Puzzle.bar, (Puzzle.w // 2, 0))
        Puzzle.screen.blit(Puzzle.bar, (Puzzle.w // 2 + Puzzle.w + 7, 0))

    def font1(text, height):
        write2(text, Puzzle.screen, Puzzle.font, 100, height)

    def write2(text, screen, font, x, y, color="Coral", ):
        text = font.render(text, 1, pygame.Color(color))
        text_rect = text.get_rect(center=(Puzzle.w // 4, y))
        screen.blit(text, text_rect)
        return text

    def writing(text, width, height):
        write2(text, Puzzle.screen, Puzzle.font, width, height)

    def soundinit():
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(32)

    drag = 0

    pyzzlemania = Puzzle("../score.txt")

    def music():
        pygame.mixer.music.load(choice([
            sound_path + "basslove.ogg",
            sound_path + "song1.mp3"]))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)

    def start():
        "The game starts here"
        global puzzle, coords, drag
        # creates puzzle grabbing pieces from this image
        create_puzzle()
        # soundinit()
        # show_puzzle2()
        # music()
        while True:
            Puzzle.screen.fill((0, 0, 0))
            # Puzzle.screen.blit(Puzzle.screen2, (0, 500))
            show_puzzle()
            show_puzzle2()
            show_puzzle3()
            bars()
            writing(f"Score {int(Puzzle.score)}", 10, Puzzle.h // 2 + 30)
            writing(f"Pieces fixed = {int(Puzzle.tiles_fixed)}/{Puzzle.w // Tile.w * Puzzle.h // Tile.h}", 10,
                    Puzzle.h // 2 + 60)
            font1(f"Maxiscore {Puzzle.maxscore}", Puzzle.h - 30)
            if Event_listener.drag == 1:
                Puzzle.score -= .01
                Puzzle.screen.blit(Event_listener.tile,
                                   (pygame.mouse.get_pos()[0] - Tile.w // 2, pygame.mouse.get_pos()[1] - Tile.h // 2))
            # User input
            Event_listener().check()
            pygame.display.update()
            Puzzle.clock.tick(60)

    menu(Puzzle, start)
    start()
