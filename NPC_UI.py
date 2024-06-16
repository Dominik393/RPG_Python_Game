from Settings import *


class UI:
    def __init__(self, npc, dialogue_data, current_dialogue):
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT / 4))
        self.image.fill('black')
        self.rect = self.image.get_frect(topleft=(0, WINDOW_HEIGHT * 3 / 4))

        self.dialogue_data = dialogue_data
        self.current_dialogue = current_dialogue
        self.response_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                              pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]
        self.NPC = npc

    def get_text(self):
        return self.dialogue_data.parse_text(self.current_dialogue)

    def show(self):
        self.display_surface.blit(self.image, self.rect.topleft)
        pygame.display.flip()

    def render_end_dialogue_prompt(self):
        font = pygame.freetype.Font(None, 24)
        prompt_text = "Press Enter to end dialogue"
        prompt_surface, _ = font.render(prompt_text, 'white', 'black')
        self.image.blit(prompt_surface, (self.rect.width - prompt_surface.get_width() - 10, self.rect.height - 30))
        self.show()

    def render_text(self, text):
        self.image.fill('black')
        font = pygame.freetype.Font(None, 30)
        words = text.split(' ')
        lines = ['']
        for word in words:
            test_line = lines[-1] + ' ' + word
            text_rect = font.get_rect(test_line, size=30)
            if text_rect.width > self.rect.width - 20:  # Subtract 20 to leave a margin
                lines.append(word)
            else:
                lines[-1] = test_line
        for i, line in enumerate(lines):
            for j in range(len(line)):
                text_surface, _ = font.render(line[:j + 1].strip(), 'white', 'black')
                self.image.blit(text_surface, (10, 10 + i * 30))  # Adjust the y position for each line
                self.show()
                pygame.time.wait(14)  # Adjust the wait time to control the speed of the text

    def render_responses(self, responses):
        font = pygame.freetype.Font(None, 24)
        for i, response in enumerate(responses):
            response_text = f"{i + 1}: {response}"
            response_surface, _ = font.render(response_text, 'white', 'black')
            self.image.blit(response_surface, (10, self.rect.height - (len(responses) - i) * 30))
        self.show()

    def run(self):
        end, text_ended = False, False
        text, responses = self.get_text()
        self.render_text(text)
        self.render_responses(responses)

        selected_responses = []

        while not end:
            answer = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if len(responses) > 0:
                for i in range(len(responses)):
                    if keys[self.response_keys[i]]:
                        answer = i
            else:
                text_ended = True

            if text_ended:
                self.render_end_dialogue_prompt()
                if keys[pygame.K_RETURN]:
                    end = True

            if 0 < int(self.current_dialogue) < 1000 and not int(self.current_dialogue) % 2: self.NPC.action()
            if answer is not None:
                selected_response = list(responses.keys())[answer]
                selected_responses.append(answer)
                if responses[selected_response]['next'] is not None:
                    self.current_dialogue = responses[selected_response]['next']
                    # award player, is it is Questgiver
                    text, responses = self.get_text()
                    self.render_text(text)
                    self.render_responses(responses)
                else:
                    text_ended = True

        return selected_responses, self.current_dialogue
