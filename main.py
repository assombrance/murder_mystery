import os
from pathlib import Path
from typing import Any, Callable, Optional

import pygame as pg
import pygame_gui as ui

main_dir = os.path.split(os.path.abspath(__file__))[0]


# Height and Width of screen
WIDTH = 640
HEIGHT = 480

DIALOGUE_BOX_WIDTH = WIDTH - 20
DIALOGUE_BOX_HEIGHT = 150

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pg.display.set_mode((WIDTH, HEIGHT))


words = [("COGNAC", "CUGTNIAROC")]


# quick function to load an image
def load_image(name: str | Path, is_char: bool = False):
    path = os.path.join(main_dir, "resources", name)
    return pg.image.load(path).convert_alpha()


def display_text(text: str, text_color: Optional[tuple[int, int, int]] = None):
    if text == "":
        return
    font = pg.font.Font("resources/SpecialElite-Regular.ttf", 20)

    if text_color is None:
        text_color = BLACK

    pg.draw.rect(
        screen,
        WHITE,
        (
            (WIDTH - DIALOGUE_BOX_WIDTH) // 2,
            HEIGHT - DIALOGUE_BOX_HEIGHT - 10,
            DIALOGUE_BOX_WIDTH,
            DIALOGUE_BOX_HEIGHT,
        ),
    )
    rendered_text = font.render(
        text, True, text_color, wraplength=DIALOGUE_BOX_WIDTH - 50
    )
    text_rect = rendered_text.get_rect(
        center=(WIDTH // 2, HEIGHT - 10 - DIALOGUE_BOX_HEIGHT // 2)
    )
    screen.blit(rendered_text, text_rect)


def button(label: str, action: Callable[[str], Any], position: tuple[int, int]):
    ui.elements.UIButton(position, label, command=action)


def minigame(word: str, letters: str):
    display_text("")
    current_guess = []
    for letter in letters:
        pos = (0, 0)
        button(letter, lambda l: current_guess.append(l), pos)
    display_text("".join(current_guess))
    while "".join(current_guess) != word:
        display_text("".join(current_guess))
        if len(current_guess) == len(word):
            current_guess = []
    pg.event.wait()


# here's the full code
def main():

    with open("resources/Dialogues.txt", encoding="utf-8") as f:
        dialog = f.readlines()
    dialog.insert(0, "")

    pg.init()
    manager = ui.UIManager((WIDTH, HEIGHT))

    clock = pg.time.Clock()

    characters: dict[str, pg.Surface] = {}
    for f_name in (Path(main_dir) / "resources/personnages").iterdir():
        characters[f_name.stem] = pg.transform.scale_by(load_image(f_name, True), 0.5)

    background = pg.transform.scale(
        load_image("lieux/auberge_exterieur.png"), (WIDTH, HEIGHT)
    )

    screen.blit(background, (0, 0))

    pg.display.set_caption("Move It!")
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.TEXTINPUT, pg.QUIT, pg.MOUSEBUTTONDOWN])

    dialog_index = 0
    minigame_index = 0
    char = characters["Ted"]

    while True:
        print(dialog[dialog_index], dialog[dialog_index] == "__G__")
        if dialog[dialog_index] == "__G__":
            minigame(*words[minigame_index])
            minigame_index += 1
        else:
            screen.blit(background, (0, 0))
            screen.blit(
                char, (100, HEIGHT - char.get_height() - DIALOGUE_BOX_HEIGHT - 10)
            )
            display_text(dialog[dialog_index])

        e = pg.event.wait()
        keys = pg.key.get_pressed()
        if e.type == pg.QUIT or keys[pg.K_q]:
            return
        if keys[pg.K_SPACE]:
            dialog_index += 1


if __name__ == "__main__":
    main()
    pg.quit()
