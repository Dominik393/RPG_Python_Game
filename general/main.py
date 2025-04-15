import pygame.sprite
from GameSound import GameSound
from Settings import *
from Level import Level
from pytmx.util_pygame import load_pygame
from player.CharacterCreator import create_character
from player.PlayerData import PlayerData
from Menu import MainMenu
from DeltaTime import DT


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('No Title RPG Game')
        self.clock = pygame.time.Clock()

        self.player_data = None
        self.tmx_maps = {1: load_pygame(join('..', 'resources', 'data', 'maps', 'level1.tmx')),
                         2: load_pygame(join('..', 'resources', 'data', 'maps', 'level2.tmx')),
                         3: load_pygame(join('..', 'resources', 'data', 'maps', 'level3.tmx'))}

        self.current_stage = None

        self.current_skin = 0
        self.skin_font = pygame.font.Font(None, 24)
        self.dt = DT(self.clock)

        self.sound = GameSound()

    def fade_to_black(self, reverse=False, fade_time=300):
        fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        fade_surface.fill((0, 0, 0))
        if reverse:
            for alpha in range(255, -1, -5):
                fade_surface.set_alpha(alpha)
                self.display_surface.blit(fade_surface, (0, 0))
                pygame.display.update()
                pygame.time.delay(fade_time // 51)
        else:
            for alpha in range(0, 256, 5):
                fade_surface.set_alpha(alpha)
                self.display_surface.blit(fade_surface, (0, 0))
                pygame.display.update()
                pygame.time.delay(fade_time // 51)

    def run(self):
        menu = MainMenu(self.sound)
        save_data = menu.run(None, None, None)

        if save_data is not None:
            self.player_data, self.current_skin, player_name = save_data
            level = self.player_data.level
        else:
            player_name, self.current_skin = create_character(self.sound)
            self.player_data = PlayerData(100, 30, 30, 1, 10, self.current_skin + 1)
            level = 1
            self.player_data.level = level

        self.current_stage = Level(self.tmx_maps[level], player_name, self.current_skin + 1, self.player_data,
                                   self.sound)
        self.sound.start_game_sound.stop()
        self.sound.background_sound.play(-1)

        self.dt.update()
        while True:
            self.dt.update()
            if self.player_data.level != level:
                self.fade_to_black()
                level = self.player_data.level
                # only 3 levels at this time available
                if level == 4:
                    pygame.quit()
                    sys.exit()
                self.current_stage = Level(self.tmx_maps[level], player_name, self.current_skin + 1, self.player_data,
                                           self.sound)
                pygame.display.update()
                pygame.time.delay(100)
                self.fade_to_black(reverse=True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        option = menu.run(self.player_data, self.current_skin, player_name)
                        if option == 'Exit':
                            pygame.quit()
                            sys.exit()
                        else:
                            pass
            self.current_stage.run(self.dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
