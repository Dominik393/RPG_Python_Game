import pygame

from Skills import Skills
from PlayerData import PlayerData
from Settings import *
from Spritessheet import SpritesSheet
from InventoryUI import InventoryUI
from pygame.math import Vector2 as vector


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, invisible_collision_sprites, player_data, name="undefined",
                 skin=1, direction=vector(0, 0)):
        super().__init__([groups, collision_sprites])
        self.invisible_collision_sprites = invisible_collision_sprites
        self.image = pygame.Surface((42, 48))

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.speed = 250
        self.player_data = PlayerData(100, 30, 1, skin)

        self.collision_sprites = collision_sprites

        self.name = name
        self.direction = None
        self.skin = skin

        self.move_disabled = False

        self.not_used_skills = True

        my_spritesheet = SpritesSheet(f'graphics/player/{skin}/texture.png')
        self.sprite_down = [my_spritesheet.parse_sprite('1.png'), my_spritesheet.parse_sprite('2.png'),
                            my_spritesheet.parse_sprite('3.png')]
        self.sprite_left = [my_spritesheet.parse_sprite('4.png'), my_spritesheet.parse_sprite('5.png'),
                            my_spritesheet.parse_sprite('6.png')]
        self.sprite_right = [my_spritesheet.parse_sprite('7.png'), my_spritesheet.parse_sprite('8.png'),
                             my_spritesheet.parse_sprite('9.png')]
        self.sprite_up = [my_spritesheet.parse_sprite('10.png'), my_spritesheet.parse_sprite('11.png'),
                          my_spritesheet.parse_sprite('12.png')]

        self.current_skin = self.sprite_down
        self.image = self.current_skin[1]

        self.skin_action = 1
        self.skin_timer = 0
        self.prev_image = self.current_skin[1]
        self.is_moving = False

        self.is_invisible = False
        self.invisibility_start_time = None

        self.teleport_target = None  # Координати для телепортації

        # Додані змінні для пришвидшення
        self.speed_boost = 3  # Коефіцієнт пришвидшення
        self.boost_timer = 0
        self.boost_duration = 10 * 1000  # 10 секунд

        # Змінні для зменшення персонажа
        self.shrink_duration = 10 * 1000  # 10 секунд
        self.shrink_timer = 0
        self.original_size = self.rect.size

        self.last_ability_time = pygame.time.get_ticks()  # Останній час використання здібностей

        self.original_images = {
            "down": self.sprite_down.copy(),
            "left": self.sprite_left.copy(),
            "right": self.sprite_right.copy(),
            "up": self.sprite_up.copy()
        }

        # Створення шрифту для ніку
        self.font = pygame.font.Font(None, 24)

        self.current_time = pygame.time.get_ticks()

    def input(self):
        self.current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        key_direction = vector(0, 0)

        # Перевірка кнопок
        if keys[pygame.K_RIGHT]:
            key_direction = vector(1, 0)
            self.current_skin = self.sprite_right
            self.is_moving = True
        elif keys[pygame.K_LEFT]:
            key_direction = vector(-1, 0)
            self.current_skin = self.sprite_left
            self.is_moving = True
        elif keys[pygame.K_UP]:
            key_direction = vector(0, -1)
            self.current_skin = self.sprite_up
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            key_direction = vector(0, 1)
            self.current_skin = self.sprite_down
            self.is_moving = True
        else:
            self.image = self.current_skin[1]

        # Обробка натискання кнопок
        if (keys[pygame.K_f] or keys[pygame.K_v] or keys[pygame.K_s]) and (
                self.not_used_skills or self.current_time - self.last_ability_time > 30000):
            if keys[pygame.K_f] and Skills.SPEED_UP in self.player_data.skills:
                self.activate_speed_boost()
            elif keys[pygame.K_v] and Skills.INVISIBILITY in self.player_data.skills:
                self.activate_invisibility()
            elif keys[pygame.K_s] and Skills.SHRINK in self.player_data.skills:
                self.shrink_player()
            self.last_ability_time = self.current_time
            self.not_used_skills = False
            self.player_data.timer = 30000 - (self.current_time - self.last_ability_time)

        if keys[pygame.K_t] and Skills.TELEPORTATION in self.player_data.skills and (
                self.not_used_skills or self.current_time - self.last_ability_time > 30000):
            if pygame.mouse.get_pressed()[0]:
                self.teleport_target = pygame.mouse.get_pos()
                self.last_ability_time = self.current_time
                self.not_used_skills = False
                self.player_data.timer = 30000 - (self.current_time - self.last_ability_time)

        # Телепортація, якщо телепорт-таргет встановлено
        if self.teleport_target:
            is_collision = False
            for sprite in self.collision_sprites:
                if sprite.rect.collidepoint(self.teleport_target):
                    is_collision = True
                    break
            if not is_collision:
                self.rect.center = self.teleport_target
            self.teleport_target = None

        self.direction = key_direction

    def activate_invisibility(self):
        if not self.is_invisible:
            self.is_invisible = True
            self.invisibility_start_time = pygame.time.get_ticks()
            self.set_transparency(128)  # 50% transparency

    def deactivate_invisibility(self):
        self.is_invisible = False
        self.set_transparency(255)  # Reset transparency to 100%

    def set_transparency(self, alpha):
        for img_list in [self.sprite_down, self.sprite_left, self.sprite_right, self.sprite_up]:
            for img in img_list:
                img.set_alpha(alpha)

    def place(self, pos):
        self.rect = self.image.get_rect(topleft=pos)

    def move(self, dt):
        if self.is_moving:
            self.skin_timer = (self.skin_timer + 1) % 56
            self.is_moving = False
            if self.skin_timer == 55:
                self.skin_action = (self.skin_action + 1) % 3
                self.prev_image = self.image
                self.image = self.current_skin[self.skin_action]

        self.rect.x += self.direction.x * self.speed * dt.get()
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt.get()
        self.collision('vertical')

    def collision(self, axis):
        if not self.is_invisible:
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.rect):
                    if axis == 'horizontal':
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.rect.left = sprite.rect.right
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            self.rect.right = sprite.rect.left
                    else:
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
        else:
            for sprite in self.invisible_collision_sprites:
                if sprite.rect.colliderect(self.rect):
                    if axis == 'horizontal':
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.rect.left = sprite.rect.right
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            self.rect.right = sprite.rect.left
                    else:
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top

    def activate_speed_boost(self):
        if self.boost_timer == 0:
            self.speed *= self.speed_boost  # Збільшення швидкості гравця

        self.boost_timer = pygame.time.get_ticks()

    def shrink_player(self):
        self.rect.size = (self.rect.width // 2, self.rect.height // 2)  # Зменшення розміру персонажа
        # Зменшення розміру зображень
        self.sprite_down = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                            in self.original_images["down"]]
        self.sprite_left = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                            in self.original_images["left"]]
        self.sprite_right = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                             in self.original_images["right"]]
        self.sprite_up = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                          in self.original_images["up"]]
        self.shrink_timer = pygame.time.get_ticks()  # Встановлення таймера зменшення персонажа

    def reset_images(self):
        self.sprite_down = self.original_images["down"].copy()
        self.sprite_left = self.original_images["left"].copy()
        self.sprite_right = self.original_images["right"].copy()
        self.sprite_up = self.original_images["up"].copy()

    def draw(self, screen):
        # Відображення персонажа
        screen.blit(self.image, self.rect.topleft)

        # Відображення ніку над персонажем
        name_surface = self.font.render(self.name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        screen.blit(name_surface, name_rect)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)

        if self.player_data.timer: self.player_data.timer = 30000 - (self.current_time - self.last_ability_time)

        # Перевірка часу зменшення персонажа
        if self.shrink_timer != 0:
            if pygame.time.get_ticks() - self.shrink_timer > self.shrink_duration:
                self.rect.size = self.original_size  # Повернення до оригінального розміру
                self.reset_images()  # Відновлення оригінальних зображень
                self.shrink_timer = 0

        if self.is_invisible and pygame.time.get_ticks() - self.invisibility_start_time > 10000:
            self.deactivate_invisibility()

        if self.boost_timer != 0:
            if pygame.time.get_ticks() - self.boost_timer > self.boost_duration:
                self.speed /= self.speed_boost  # Повернення швидкості до нормального рівня
                self.boost_timer = 0

        if self.teleport_target:
            is_collision = False
            for sprite in self.collision_sprites:
                if sprite.rect.collidepoint(self.teleport_target):
                    is_collision = True
                    break
            if not is_collision:
                self.rect.center = self.teleport_target
                self.collision('horizontal')  # Додати обробку колізій після телепортації
                self.collision('vertical')  # Додати обробку колізій після телепортації
            self.teleport_target = None

    def set_transparency(self, alpha):
        for img_list in [self.sprite_down, self.sprite_left, self.sprite_right, self.sprite_up]:
            for img in img_list:
                img.set_alpha(alpha)

    def activate_invisibility(self):
        if not self.is_invisible:
            self.is_invisible = True
            self.invisibility_start_time = pygame.time.get_ticks()
            self.set_transparency(128)  # 50% transparency

    def deactivate_invisibility(self):
        self.is_invisible = False
        self.set_transparency(255)  # Reset transparency to 100%

    def activate_speed_boost(self):
        if self.boost_timer == 0:
            self.speed *= self.speed_boost  # Збільшення швидкості гравця

        self.boost_timer = pygame.time.get_ticks()

    def shrink_player(self):
        self.rect.size = (self.rect.width // 2, self.rect.height // 2)  # Зменшення розміру персонажа
        # Зменшення розміру зображень
        self.sprite_down = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                            in self.original_images["down"]]
        self.sprite_left = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                            in self.original_images["left"]]
        self.sprite_right = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                             in self.original_images["right"]]
        self.sprite_up = [pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)) for image
                          in self.original_images["up"]]
        self.shrink_timer = pygame.time.get_ticks()  # Встановлення таймера зменшення персонажа

    def reset_images(self):
        self.sprite_down = self.original_images["down"].copy()
        self.sprite_left = self.original_images["left"].copy()
        self.sprite_right = self.original_images["right"].copy()
        self.sprite_up = self.original_images["up"].copy()
