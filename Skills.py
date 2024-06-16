from enum import Enum
from Settings import *
import pygame

class Skills(Enum):
    SPEED_UP = (1, pygame.image.load(join('graphics', 'objects', 'items', 'speed_up.png')), "speed-up", "Press F")
    TELEPORTATION = (2, pygame.image.load(join('graphics', 'objects', 'items', 'teleportation.png')), "teleportation", "Press T and click")
    SHRINK = (3, pygame.image.load(join('graphics', 'objects', 'items', 'shrink.png')), "shrink", "Press S")
    INVISIBILITY = (4, pygame.image.load(join('graphics', 'objects', 'items', 'invisibility.png')), "invisibility", "Press V")

    @property
    def id(self):
        return self.value[0]

    @property
    def image(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[2]

    @property
    def keyboard(self):
        return self.value[3]

    def __str__(self):
        return self.value[2]
