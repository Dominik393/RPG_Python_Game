from Settings import *
from Spritessheet import SpritesSheet
from Button import Button
from Notification import *


def reward_player_fight(player, enemy):
    player.player_data.enemies_won_level += 1
    print(player.player_data.level, enemy.start_power * 10, player.player_data.power // 2)
    earned = enemy.start_power * 5 * player.player_data.power // 2
    player.player_data.coins += earned
    player.player_data.earned_coins_level += earned
    player.player_data.exp += 15 * player.player_data.level

def player_attack(player, enemy):
    if not player.process_status_effects(enemy):
        return False

    enemy.enemy_data.reduce_health(player.player_data.damage)

def is_enemy_dead(enemy):
    return enemy.get_health() <= 0

def display_player(player, display_surface):
    my_spritesheet = SpritesSheet(join('graphics', 'player', f'{player.skin}', 'texture.png'))
    sprite_down = my_spritesheet.parse_sprite('8.png')
    skin_view = pygame.transform.scale(sprite_down, (200, 200))
    display_surface.blit(skin_view, (150, 300))

def display_enemy(enemy, display_surface):
    enemy_spritesheet = SpritesSheet(join(f'graphics/enemies/{enemy.__class__.__name__}/texture.png'))
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
        buttons.append(Button(button.x, button.y - skill_height * (i + 1), skill_width, skill_height, skill.name, (10, 120, 255),
                       function= skill.effect))

    return buttons


def item_buttons_list(player, button):
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
                              (10, 120, 255)))
        buttons[-1].set_surface(item_list_surface)

    return buttons

def display_health(player, enemy, display_surface):
    # Create health Bars for player and enemy
    font = pygame.font.Font(None, 40)
    health_bar_width = 240
    health_bar_height = 30

    player_max_health = pygame.Surface((health_bar_width, health_bar_height))
    player_max_health.fill('black')
    player_health = pygame.Surface((health_bar_width * (player.get_health()/player.get_max_health()), health_bar_height))
    player_health.fill('green')
    player_health_rect = player_health.get_rect(topleft=(150, 250))
    text_surface_player = font.render(f"{player.get_health()}/{player.get_max_health()}", True, 'black')
    text_rect_player = text_surface_player.get_rect(center=player_health_rect.center)  # Center the text

    enemy_max_health = pygame.Surface((health_bar_width, health_bar_height))
    enemy_max_health.fill('black')
    enemy_health = pygame.Surface((health_bar_width * (enemy.get_health()/enemy.get_max_health()), health_bar_height))
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

def fight(enemy, player, dt):
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    background_image = pygame.image.load('graphics/map/background/1.png').convert()

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
                    print('button 2 clicked')
                if buttons[2].is_over(pos):
                    if item_buttons:
                        item_buttons = None
                    else:
                        item_buttons = item_buttons_list(player, buttons[2])
                    print('button 3 clicked')
        if did_action:
            enemy.fight_ai(player)
            did_action = False


        display_surface.fill((30, 30, 30))

        # Display player sprite
        display_player(player, display_surface)

        # Display enemy sprite
        display_enemy(enemy, display_surface)

        # Display squares above player and enemy
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
            player.player_data.fight_win_sound.play()
            reward_player_fight(player, enemy)
            enemy.destroy()
            return

        pygame.display.flip()
        clock.tick(30)


