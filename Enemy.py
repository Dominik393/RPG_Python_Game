from EntityData import EntityData
from Settings import *
from Spritessheet import SpritesSheet
from Fight import fight
from StatusEffects import StatusEffects


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, player, timer, power, max_health, direction, name, health=None):
        super().__init__([groups, collision_sprites])
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.name = name

        self.start_power = power

        my_spritesheet = SpritesSheet(f'graphics/enemies/{self.name}/texture.png')
        self.sprite_down = [my_spritesheet.parse_sprite('1.png'), my_spritesheet.parse_sprite('2.png'),
                            my_spritesheet.parse_sprite('3.png')]
        self.sprite_left = [my_spritesheet.parse_sprite('4.png'), my_spritesheet.parse_sprite('5.png'),
                            my_spritesheet.parse_sprite('6.png')]
        self.sprite_right = [my_spritesheet.parse_sprite('7.png'), my_spritesheet.parse_sprite('8.png'),
                             my_spritesheet.parse_sprite('9.png')]
        self.sprite_up = [my_spritesheet.parse_sprite('10.png'), my_spritesheet.parse_sprite('11.png'),
                          my_spritesheet.parse_sprite('12.png')]

        self.current_skin = self.sprite_right
        self.direction = direction
        self.opposite_direction(self.direction)
        self.image = self.current_skin[1]

        self.player = player
        if health is None:
            health = max_health
        self.enemy_data = EntityData(health, max_health, power)
        self.status_effects = StatusEffects()

        self.speed = 30
        self.collision_sprites = collision_sprites
        self.timer = timer

        self.skin_action = 1
        self.skin_timer = 0
        self.prev_image = self.current_skin[1]
        self.is_moving = False
        self.escape_timer = None

    def is_in_move_range(self):
        player_pos, self_pos = vector(self.player.rect.center), vector(self.rect.center)
        in_range = False
        if abs(player_pos[0] - self_pos[0]) < WINDOW_WIDTH // 2 and abs(
                player_pos[1] - self_pos[1]) < WINDOW_HEIGHT // 2:
            in_range = True

        return in_range

    def is_active(self):
        if self.escape_timer is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.escape_timer >= 3500:
                self.escape_timer = None
            else:
                return False
        player_pos, self_pos = vector(self.player.rect.center), vector(self.rect.center)
        in_range = self_pos.distance_to(player_pos) < 50

        return in_range

    def input(self, dt):
        if self.is_active() and not self.player.is_invisible and self.player.player_data.health >= 10:
            self.player.sound.background_sound.set_volume(0.0)
            self.player.sound.fight_sound.set_volume(0.45)
            self.player.paused = True
            fight(self, self.player, dt)
            self.player.paused = False
            dt.set(0)

    def move(self, dt):
        if not self.is_in_move_range():
            return

        self.skin_timer = (self.skin_timer + 1) % 56
        if self.skin_timer == 55:
            self.skin_action = (self.skin_action + 1) % 3
            self.prev_image = self.image
            self.image = self.current_skin[self.skin_action]

        self.rect.x += self.direction.x * self.speed * dt.get()
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt.get()
        self.collision('vertical')

    def update(self, dt):
        self.old_rect = self.rect.copy()
        if not self.player.paused:
            self.input(dt)
            self.move(dt)

    def opposite_direction(self, direction):
        if direction == vector(0, 1):
            self.current_skin = self.sprite_up
        elif direction == vector(0, -1):
            self.current_skin = self.sprite_down
        elif direction == vector(1, 0):
            self.current_skin = self.sprite_left
        elif direction == vector(-1, 0):
            self.current_skin = self.sprite_right

        direction *= -1

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.opposite_direction(self.direction)

                    # right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.opposite_direction(self.direction)

                else:
                    # up
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.opposite_direction(self.direction)

                    # down
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.opposite_direction(self.direction)

    def escape(self):
        self.escape_timer = pygame.time.get_ticks()

    def process_status_effects(self, player):
        if player.status_effects.protected:
            self.enemy_data.damage = 0
        else:
            self.enemy_data.damage = self.enemy_data.power

        if self.status_effects.stunned:
            return False

        if self.status_effects.on_fire:
            self.enemy_data.health -= 1
            if self.enemy_data.health <= 0:
                return False

        if self.status_effects.poisoned:
            self.enemy_data.health -= 1
            if self.enemy_data.health <= 0:
                return False

        return True

    def fight_ai(self, player):
        if not self.process_status_effects(player):
            return False

        player.sound.attack_sound.play()
        player.player_data.health = max(0, player.player_data.health - self.enemy_data.damage)
        self.enemy_data.damage = 0
        if player.player_data.health <= 0:
            return True

    def get_health(self):
        return self.enemy_data.health

    def get_max_health(self):
        return self.enemy_data.max_health

    def destroy(self):
        self.kill()
