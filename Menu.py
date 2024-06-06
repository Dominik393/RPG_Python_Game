from GameSound import GameSound
from Settings import *

class MainMenu:
    def __init__(self, sound):
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect()
        self.options = ['Start Game', 'Settings', 'Save', 'Exit']
        self.current_option = 0
        self.sound = sound

    def render(self):
        self.image.fill('black')
        font = pygame.freetype.Font(None, 36)
        for i, option in enumerate(self.options):
            color = 'white' if i == self.current_option else 'gray'
            text_surface, _ = font.render(option, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + i * 70))
            self.image.blit(text_surface, text_rect)
        self.display_surface.blit(self.image, self.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.sound.menu_sound.play()
            self.current_option = (self.current_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.sound.menu_sound.play()
            self.current_option = (self.current_option + 1) % len(self.options)
        elif keys[pygame.K_RETURN]:
            return self.options[self.current_option]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            option = self.update()
            if option:
                return option
            self.render()
            pygame.display.flip()
            pygame.time.wait(100)
