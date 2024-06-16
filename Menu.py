from Save import *
from Settings import *

class MainMenu:
    def __init__(self, sound):
        self.display_surface = pygame.display.get_surface()
        self.background_image = pygame.image.load(join('graphics', 'objects', 'background.png'))
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.button_images = [
            pygame.image.load(join('graphics', 'objects', 'button_play.png')).convert_alpha(),
            pygame.image.load(join('graphics', 'objects', 'button_save.png')).convert_alpha(),
            pygame.image.load(join('graphics', 'objects', 'button_load.png')).convert_alpha(),
            pygame.image.load(join('graphics', 'objects', 'button_exit.png')).convert_alpha()
        ]

        self.button_images_bigger = [
            pygame.image.load(join('graphics', 'objects', 'button_play_bigger.png')).convert_alpha(),
            pygame.image.load(join('graphics', 'objects', 'button_save_bigger.png')).convert_alpha(),
            pygame.image.load(join('graphics', 'objects', 'button_load_bigger.png')).convert_alpha(),
            pygame.image.load(join('graphics', 'objects', 'button_exit_bigger.png')).convert_alpha()
        ]

        self.logo_image = pygame.image.load(join('graphics', 'objects', 'logo.png')).convert_alpha()
        self.logo_rect = self.logo_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6))

        self.options = ['Play', 'Save', 'Load', 'Exit']
        self.current_option = 0
        self.sound = sound

    def render(self):
        self.display_surface.blit(self.background_image, (0, 0))

        self.display_surface.blit(self.logo_image, self.logo_rect)

        for i in range(len(self.options)):
            if i == self.current_option:
                button = self.button_images_bigger[i]
            else:
                button = self.button_images[i]

            button_rect = button.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 25 + i * 100))
            self.display_surface.blit(button, button_rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.sound.menu_sound.play()
            self.current_option = (self.current_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.sound.menu_sound.play()
            self.current_option = (self.current_option + 1) % len(self.options)
        elif keys[pygame.K_RETURN]:
            self.sound.menu_sound.play()
            return self.options[self.current_option]

    def run(self, player_data, current_skin, player_name):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            option = self.update()
            if option == 'Exit':
                pygame.quit()
                sys.exit()
            elif option == "Load":
                return load_save()
            elif option == "Save":
                if player_data is None or current_skin is None:
                    continue
                create_save(player_data, current_skin, player_name)
            elif option == "Play":
                return None
            self.render()
            pygame.display.flip()
            pygame.time.wait(100)
