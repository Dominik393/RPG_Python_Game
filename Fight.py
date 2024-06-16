from FightLostUI import FightLostUI
from Spritessheet import SpritesSheet
from Button import Button
from Notification import *


def reward_player_fight(player, enemy):
    player.player_data.enemies_won_level += 1
    earned = enemy.start_power * player.player_data.power // 4
    player.player_data.coins += earned
    player.player_data.earned_coins_level += earned
    player.player_data.exp += 15 * player.player_data.level


def player_attack(player, enemy):
    if not player.process_status_effects(enemy):
        return False
    player.sound.attack_sound.play()
    enemy.enemy_data.reduce_health(player.player_data.damage)


def is_enemy_dead(enemy):
    return enemy.get_health() <= 0


def display_player(player, display_surface):
    my_spritesheet = SpritesSheet(join('graphics', 'player', f'{player.skin}', 'texture.png'))
    sprite_down = my_spritesheet.parse_sprite('8.png')
    skin_view = pygame.transform.scale(sprite_down, (200, 200))
    display_surface.blit(skin_view, (150, 300))


def display_enemy(enemy, display_surface):
    enemy_spritesheet = SpritesSheet(join(f'graphics/enemies/{enemy.name}/texture.png'))
    sprite_right = enemy_spritesheet.parse_sprite('5.png')
    skin_view_right = pygame.transform.scale(sprite_right, (200, 200))
    display_surface.blit(skin_view_right, (WINDOW_WIDTH - 350, 300))


def skill_buttons_list(player, button, enemy):
    skills = player.player_data.battle_skills

    if len(skills) <= 0:
        return None

    # Create buttons for each skill vertically above the skills button
    skill_width = button.width
    skill_height = 50
    buttons = []
    for i, skill in enumerate(skills):
        buttons.append(
            Button(button.x, button.y - skill_height * (i + 1), skill_width, skill_height, skill.name, (10, 120, 255),
                   function=skill.effect))

    return buttons


def item_buttons_list(player, button, enemy):
    items = player.player_data.inventory.get_item_list()
    items = list(items)

    if len(items) <= 0:
        return None

    # Create buttons for each item vertically above the items button
    item_width = button.width
    item_height = 50
    buttons = []

    for i, item in enumerate(items):
        item_list_surface = pygame.Surface((item_width, item_height))
        item_list_surface.fill((10, 120, 255))
        item_image_position = (0, -5)
        item_list_surface.blit(item.image, item_image_position)
        # Draw item amount to the right of the item image
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"x{item.amount}", True, 'black')
        text_position = (item_image_position[1] + item.image.get_width(), item_image_position[1] + item_height // 2
                         - text_surface.get_height() // 2 + 7)
        item_list_surface.blit(text_surface, text_position)
        # Draw item name to the right of the item amount
        text_position = (text_position[0] + text_surface.get_width() + 10, text_position[1])
        text_surface = font.render(item.item_type.name, True, 'black')
        item_list_surface.blit(text_surface, text_position)

        buttons.append(Button(button.x, button.y - item_height * (i + 1), item_width, item_height, item.name,
                              (10, 120, 255), function=item.use))
        buttons[-1].set_surface(item_list_surface)

    return buttons


def display_health(player, enemy, display_surface):
    # Create health Bars for player and enemy
    font = pygame.font.Font(None, 40)
    health_bar_width = 240
    health_bar_height = 30

    player_max_health = pygame.Surface((health_bar_width, health_bar_height))
    player_max_health.fill('black')
    player_health = pygame.Surface(
        (health_bar_width * (max(player.get_health(), 0) / player.get_max_health()), health_bar_height))
    player_health.fill('green')
    player_health_rect = player_health.get_rect(topleft=(150, 250))
    text_surface_player = font.render(f"{player.get_health()}/{player.get_max_health()}", True, 'black')
    text_rect_player = text_surface_player.get_rect(center=player_health_rect.center)  # Center the text

    enemy_max_health = pygame.Surface((health_bar_width, health_bar_height))
    enemy_max_health.fill('black')
    enemy_health = pygame.Surface((health_bar_width * (enemy.get_health() / enemy.get_max_health()), health_bar_height))
    enemy_health.fill('green')
    enemy_health_rect = enemy_health.get_rect(topleft=(WINDOW_WIDTH - 350, 250))
    text_surface_enemy = font.render(f"{enemy.get_health()}/{enemy.get_max_health()}", True, 'black')
    text_rect_enemy = text_surface_enemy.get_rect(center=enemy_health_rect.center)  # Center the text

    display_surface.blit(player_max_health, player_health_rect)
    display_surface.blit(player_health, player_health_rect)
    display_surface.blit(enemy_max_health, enemy_health_rect)
    display_surface.blit(enemy_health, enemy_health_rect)
    display_surface.blit(text_surface_player, text_rect_player.topleft)  # Use the centered text rect
    display_surface.blit(text_surface_enemy, text_rect_enemy.topleft)  # Use the centered text rect


def create_buttons():
    button_width, button_height = 370, 50
    button_y = WINDOW_HEIGHT - button_height - 40
    spacing = 40
    button1 = Button(spacing, button_y, button_width, button_height, 'Attack')
    button2 = Button(spacing * 2 + button_width, button_y, button_width, button_height, 'Skills')
    button3 = Button(spacing * 3 + button_width * 2, button_y, button_width, button_height, 'Items')

    return button1, button2, button3


def attack_animation(player, enemy, display_surface, enemy_dead):
    # Load player and enemy sprites
    player_spritesheet = SpritesSheet(join('graphics', 'player', f'{player.skin}', 'texture.png'))
    enemy_spritesheet = SpritesSheet(join(f'graphics/enemies/{enemy.name}/texture.png'))
    player_right = player_spritesheet.parse_sprite('8.png')
    enemy_right = enemy_spritesheet.parse_sprite('5.png')
    player_right = pygame.transform.scale(player_right, (200, 200))
    enemy_right = pygame.transform.scale(enemy_right, (200, 200))
    background_image = pygame.image.load('graphics/map/background/village.png').convert()

    player_pos = (150 - 4, 300 - 4)
    enemy_pos = (WINDOW_WIDTH - 350 - 4, 300 - 4)

    surface_width, surface_height = 208, 208
    player_surface = pygame.Surface((surface_width, surface_height))
    enemy_surface = pygame.Surface((surface_width, surface_height))
    player_surface.blit(player_right, (4, 4))
    enemy_surface.blit(enemy_right, (4, 4))

    move_player_right = True
    move_player_left = False
    move_enemy_left = False
    move_enemy_right = False

    pygame.draw.rect(display_surface, 'black', (0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, WINDOW_HEIGHT))
    display_surface.blit(background_image, (0, -350))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if move_player_right:
            player_pos = (player_pos[0] + 2, player_pos[1])
            background_subsurface = background_image.subsurface(
                (player_pos[0], player_pos[1], surface_width, surface_height))
            background_subsurface.blit(player_surface, (0, 0))
            if player_pos[0] >= WINDOW_WIDTH - 750:
                move_player_right = False
                move_player_left = True
                display_health(player, enemy, display_surface)
        elif move_player_left:
            player_pos = (player_pos[0] - 2, player_pos[1])
            background_subsurface = background_image.subsurface(
                (player_pos[0], player_pos[1], surface_width, surface_height))
            background_subsurface.blit(player_surface, (0, 0))
            if player_pos[0] <= 150 - 4:
                move_player_left = False
                if not enemy_dead:
                    move_enemy_left = True
                else:
                    return
        elif move_enemy_left:
            enemy_pos = (enemy_pos[0] - 2, enemy_pos[1])
            background_subsurface = background_image.subsurface(
                (enemy_pos[0], enemy_pos[1], surface_width, surface_height))
            background_subsurface.blit(enemy_surface, (0, 0))
            if enemy_pos[0] <= 550:
                move_enemy_left = False
                move_enemy_right = True
        elif move_enemy_right:
            enemy_pos = (enemy_pos[0] + 2, enemy_pos[1])
            background_subsurface = background_image.subsurface(
                (enemy_pos[0], enemy_pos[1], surface_width, surface_height))
            background_subsurface.blit(enemy_surface, (0, 0))
            if enemy_pos[0] >= WINDOW_WIDTH - 350:
                return

        # Create a subsurface of the background image for player and enemy
        player_background_subsurface = background_image.subsurface(
            pygame.Rect(player_pos[0], player_pos[1] + 350, surface_width, surface_height))
        enemy_background_subsurface = background_image.subsurface(
            pygame.Rect(enemy_pos[0], enemy_pos[1] + 350, surface_width, surface_height))

        # Blit the subsurface onto the player and enemy surfaces
        player_surface.blit(player_background_subsurface, (0, 0))
        enemy_surface.blit(enemy_background_subsurface, (0, 0))

        # Blit player and enemy onto their surfaces
        player_surface.blit(player_right, (4, 4))
        enemy_surface.blit(enemy_right, (4, 4))

        # Blit the player and enemy surfaces onto the display surface at the new positions
        display_surface.blit(player_surface, player_pos)
        display_surface.blit(enemy_surface, enemy_pos)

        pygame.display.flip()
        pygame.time.wait(1)


def draw_everything(player, enemy, display_surface, background_image, buttons, item_buttons=None, skill_buttons=None):
    display_surface.blit(background_image, (0, -350))

    pygame.draw.rect(display_surface, 'black', (0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, WINDOW_HEIGHT))

    display_player(player, display_surface)

    display_enemy(enemy, display_surface)

    display_health(player, enemy, display_surface)

    for button in buttons:
        button.draw(display_surface, 1)

    if item_buttons:
        for button in item_buttons:
            button.draw(display_surface)

    if skill_buttons:
        for button in skill_buttons:
            button.draw(display_surface)

    pygame.display.flip()


def configure_sound(player):
    player.sound.fight_sound.set_volume(0.0)
    player.sound.background_sound.set_volume(0.05)


def confirm_enemy_death(enemy, player):
    player.sound.fight_win_sound.play()
    reward_player_fight(player, enemy)
    configure_sound(player)
    enemy.destroy()


def fight(enemy, player, dt):
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    background_image = pygame.image.load('graphics/map/background/village.png').convert()

    # Create buttons
    buttons = create_buttons()

    item_buttons = None
    skill_buttons = None
    notification = None

    did_action = False

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if skill_buttons:
                    for button in skill_buttons:
                        if button.is_over(pos):
                            button.use_function(player, enemy)
                            did_action = True
                            skill_buttons = None
                if item_buttons:
                    for button in item_buttons:
                        if button.is_over(pos):
                            button.use_function(player, enemy)
                            did_action = True
                            item_buttons = None
                if buttons[0].is_over(pos):
                    if player_attack(player, enemy):
                        enemy.kill()
                        return
                    did_action = True
                if buttons[1].is_over(pos):
                    if skill_buttons:
                        skill_buttons = None
                    else:
                        skill_buttons = skill_buttons_list(player, buttons[1], enemy)
                if buttons[2].is_over(pos):
                    if item_buttons:
                        item_buttons = None
                    else:
                        item_buttons = item_buttons_list(player, buttons[2], enemy)
        if did_action:
            attack_animation(player, enemy, display_surface, is_enemy_dead(enemy))
            if is_enemy_dead(enemy):
                confirm_enemy_death(enemy, player)
                return
            if enemy.fight_ai(player):
                FightLostUI(player.groups, player)
                configure_sound(player)
                player.sound.fight_lost_sound.play()
                enemy.escape()
                return
            did_action = False

        # Display background image
        display_surface.blit(background_image, (0, -350))

        # Fill lower part of the screen with black
        pygame.draw.rect(display_surface, 'black', (0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, WINDOW_HEIGHT))

        # Display player sprite
        display_player(player, display_surface)

        # Display enemy sprite
        display_enemy(enemy, display_surface)

        # Display bars for player and enemy health
        display_health(player, enemy, display_surface)

        # Draw buttons
        for button in buttons:
            button.draw(display_surface, 1)

        if item_buttons:
            for button in item_buttons:
                button.draw(display_surface)

        if skill_buttons:
            for button in skill_buttons:
                button.draw(display_surface)

        if notification:
            notification.draw(display_surface)
            if notification.update(dt):
                notification = None

        if is_enemy_dead(enemy):
            confirm_enemy_death(enemy, player)
            return

        pygame.display.flip()
        clock.tick(30)
