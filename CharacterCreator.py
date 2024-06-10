from PlayerData import available_items
from Settings import *
from Spritessheet import SpritesSheet
from Skills import Skills  # Додано імпорт Skills
import random


def create_character(sound):
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(WINDOW_WIDTH / 2 - 110, 150, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    current_skin = 0
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    text = ''
    default_text = font.render("Character name", True, color)

    skills_list = [
        Skills.SPEED_UP,
        Skills.TELEPORTATION,
        Skills.SHRINK,
        Skills.INVISIBILITY,
        Skills.SPEED_UP,
        Skills.TELEPORTATION,
        Skills.SHRINK,
        Skills.INVISIBILITY
    ]

    while True:
        for event in pygame.event.get():
            # Обробка події закриття вікна
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text, current_skin
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                if event.key == pygame.K_LEFT:
                    sound.arrow_sound.play()
                    current_skin = (current_skin - 1) % 8
                elif event.key == pygame.K_RIGHT:
                    sound.arrow_sound.play()
                    current_skin = (current_skin + 1) % 8

        # Відображення вікна з назвою
        display_surface.fill((30, 30, 30))
        if len(text) == 0:
            txt_surface = default_text
        else:
            txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        display_surface.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(display_surface, color, input_box, 2)

        # Відображення поточного скину
        my_spritesheet = SpritesSheet(join('graphics', 'player', f'{current_skin + 1}', 'texture.png'))
        sprite_down = my_spritesheet.parse_sprite('2.png')
        skin_view = pygame.transform.scale(sprite_down, (200, 200))
        display_surface.blit(skin_view, (WINDOW_WIDTH / 2 - 110, 300))

        # Відображення трьох предметів під скином
        skin_items = available_items[current_skin]
        items_count = len(skin_items)
        sector_width = WINDOW_WIDTH // items_count
        for i, item_type in enumerate(skin_items):
            item_image = item_type.image
            item_surface = pygame.transform.scale(item_image, (50, 50))
            item_x = i * sector_width + (sector_width - item_surface.get_width()) // 2
            item_y = 520
            display_surface.blit(item_surface, (item_x, item_y))

            item_id, price, damage, min_power_to_get, file, name = item_type.value
            item_data_text = font.render(f"Damage: {damage}, Min level to get: {min_power_to_get}",
                                         True, (255, 255, 255))
            text_x = item_x - 150
            text_y = item_y + item_surface.get_height()
            display_surface.blit(item_data_text, (text_x, text_y))

        # Відображення скілу для поточного скину
        current_skill = skills_list[current_skin]
        skill_image = current_skill.value[3]
        skill_surface = pygame.transform.scale(skill_image, (50, 50))
        skill_x = (WINDOW_WIDTH - skill_surface.get_width()) // 2
        skill_y = 620
        display_surface.blit(skill_surface, (skill_x, skill_y))

        skill_id, skill_price, skill_min_power_to_get, skill_file, skill_name = current_skill.value
        skill_data_text = font.render(f"Skill: {skill_name}",
                                      True, (255, 255, 255))
        display_surface.blit(skill_data_text, (skill_x - 70, skill_y + skill_surface.get_height()))

        arrows_image = pygame.image.load(join("graphics", "buttons", "arrow_keys.png")).convert_alpha()
        arrows_width, arrows_height = arrows_image.get_size()
        left_arrow = arrows_image.subsurface(0, 0, arrows_width / 4, arrows_height)
        right_arrow = arrows_image.subsurface(arrows_width / 4 * 3, 0, arrows_width / 4, arrows_height)
        display_surface.blit(pygame.transform.scale(left_arrow, (100, 100)), (450, 400))
        display_surface.blit(pygame.transform.scale(right_arrow, (100, 100)), (700, 400))

        pygame.display.flip()
        clock.tick(30)