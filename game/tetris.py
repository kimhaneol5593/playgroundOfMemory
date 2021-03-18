from game.scenes import GameMetaData, TitleScene, Scenes
import os, pygame


def run():
    # Positioned Window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)

    #########
    # CLOCK #
    #########
    clock = pygame.time.Clock()

    main_screen = pygame.display.set_mode((GameMetaData.screen_width, GameMetaData.screen_height))

    Scenes.titleScene = TitleScene()
    Scenes.active_scene = Scenes.titleScene

    while True:
        Scenes.active_scene.process_input(pygame.event.get())
        Scenes.active_scene.update()
        Scenes.active_scene.render(main_screen)

        clock.tick(50)
