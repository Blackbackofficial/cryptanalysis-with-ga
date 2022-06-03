import os

from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from encryption.menu import MenuDisplay

os.system('cls||clear')


def demo(screen):
    effects = [
        Cycle(
            screen,
            FigletText("Gen-Key && decoder", font='big'),
            int(screen.height / 2 - 8)),
        Cycle(
            screen,
            FigletText("with"),
            int(screen.height / 2)),
        Cycle(
            screen,
            FigletText("genetics algo"),
            int(screen.height / 2 + 8)),
        Stars(screen, 200)
    ]
    screen.play([Scene(effects, 500)], stop_on_resize=True, repeat=False)


Screen.wrapper(demo)

if __name__ == "__main__":
    menu = ['I want to encrypt a message.', 'I have already encrypted, just decipher!', 'leave?']

    MenuDisplay(menu)
