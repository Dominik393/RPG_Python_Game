from Settings import *


class GameSound:
    def __init__(self):
        self.audio_files = {
            'background': pygame.mixer.Sound(join('audio', 'background.mp3')),
            'npc': pygame.mixer.Sound(join('audio', 'npc.mp3')),
            'coin': pygame.mixer.Sound(join('audio', 'coin.wav')),
            'jump': pygame.mixer.Sound(join('audio', 'jump.wav')),
            'up_level': pygame.mixer.Sound(join('audio', 'up_level.wav')),
            'quest_done': pygame.mixer.Sound(join('audio', 'quest_done.mp3')),
            'fight': pygame.mixer.Sound(join('audio', 'fight.mp3')),
            'fight_win': pygame.mixer.Sound(join('audio', 'fight_win.mp3')),
            'fight_lost': pygame.mixer.Sound(join('audio', 'fight_lost.mp3')),
            'skill_activate': pygame.mixer.Sound(join('audio', 'skill_activate.mp3')),
            'timer': pygame.mixer.Sound(join('audio', 'timer.mp3')),
            'fortune_fail': pygame.mixer.Sound(join('audio', 'fortune_fail.wav')),
            'fortune_health': pygame.mixer.Sound(join('audio', 'fortune_health.mp3')),
            'fortune_coin': pygame.mixer.Sound(join('audio', 'fortune_coin.mp3')),
            'fortune_equipment': pygame.mixer.Sound(join('audio', 'fortune_equipment.mp3')),
            'skill_small': pygame.mixer.Sound(join('audio', 'skill_small.mp3')),
            'mouse_click': pygame.mixer.Sound(join('audio', 'mouse_click.mp3')),
            'money': pygame.mixer.Sound(join('audio', 'money.wav')),
            'attack': pygame.mixer.Sound(join('audio', 'attack.wav')),
            'start_game': pygame.mixer.Sound(join('audio', 'start_game.mp3')),
            'quest_item': pygame.mixer.Sound(join('audio', 'quest_item.wav')),
            'health': pygame.mixer.Sound(join('audio', 'health.mp3')),
        }

        self.background_sound = pygame.mixer.Sound(join('audio', 'background.mp3'))
        self.background_sound.set_volume(0.05)

        self.menu_sound = pygame.mixer.Sound(join('audio', 'menu_button.mp3'))
        self.menu_sound.set_volume(2.0)
        self.arrow_sound = pygame.mixer.Sound(join('audio', 'arrows.flac'))

        self.coin_sound = self.audio_files['coin']
        self.coin_sound.set_volume(0.3)

        self.money_sound = self.audio_files['money']
        self.money_sound.set_volume(0.3)

        self.up_level_sound = self.audio_files['up_level']
        self.up_level_sound.set_volume(0.3)

        self.quest_done_sound = self.audio_files['quest_done']
        self.quest_done_sound.set_volume(0.45)

        self.fight_win_sound = self.audio_files['fight_win']
        self.fight_win_sound.set_volume(0.45)

        self.fight_lost_sound = self.audio_files['fight_lost']
        self.fight_lost_sound.set_volume(0.45)

        self.skill_activate_sound = self.audio_files['skill_activate']
        self.skill_activate_sound.set_volume(0.45)

        self.fortune_fail_sound = self.audio_files['fortune_fail']
        self.fortune_fail_sound.set_volume(0.45)

        self.fortune_coin_sound = self.audio_files['fortune_coin']
        self.fortune_coin_sound.set_volume(0.45)

        self.fortune_health_sound = self.audio_files['fortune_health']
        self.fortune_health_sound.set_volume(0.45)

        self.fortune_equipment_sound = self.audio_files['fortune_equipment']
        self.fortune_equipment_sound.set_volume(0.45)

        self.jump_sound = self.audio_files['jump']
        self.jump_sound.set_volume(0.4)

        self.timer_sound = self.audio_files['timer']
        self.timer_sound.set_volume(0.6)

        self.health_sound = self.audio_files['health']
        self.health_sound.set_volume(0.6)

        self.skill_small_sound = self.audio_files['skill_small']
        self.skill_small_sound.set_volume(0.45)

        self.mouse_click_sound = self.audio_files['mouse_click']
        self.mouse_click_sound.set_volume(0.45)

        self.attack_sound = self.audio_files['attack']
        self.attack_sound.set_volume(0.6)

        self.quest_item_sound = self.audio_files['quest_item']
        self.quest_item_sound.set_volume(0.6)

        self.start_game_sound = self.audio_files['start_game']
        self.start_game_sound.set_volume(0.3)
        self.start_game_sound.play(-1)

        self.npc_sound = self.audio_files['npc']
        self.npc_sound.set_volume(0.0)
        self.npc_sound.play(-1)

        self.fight_sound = self.audio_files['fight']
        self.fight_sound.set_volume(0.0)
        self.fight_sound.play(-1)
