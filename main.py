import os
from pathlib import Path
from random import randint
from typing import Optional

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


def minigame(word: str, letters: str, manager: ui.UIManager, clock: pg.Clock):
    current_guess = []
    buttons: list[ui.elements.UIButton] = []
    for letter in letters:
        pos = (randint(20, WIDTH - 60), randint(20, HEIGHT // 2))
        buttons.append(
            ui.elements.UIButton(
                (*pos, 40, 40), letter, manager, object_id=str(randint(0, 10000))
            )
        )
    while "".join(current_guess) != word:
        time_delta = clock.tick(60) / 1000.0
        e = pg.event.wait()
        if e.type == pg.QUIT:
            exit(0)
        if e.type == ui.UI_BUTTON_PRESSED:
            current_guess.append(e.ui_element.text)
            e.ui_element.disable()

        manager.process_events(e)
        manager.update(time_delta)
        manager.draw_ui(screen)

        guess = "".join(current_guess)
        display_text(guess)
        if guess == word:
            for button in buttons:
                button.kill()
                del button
            pg.display.update()
            pg.time.delay(1_000)
            return
        if len(guess) == len(word):
            current_guess = []
            for button in buttons:
                button.enable()
        pg.display.update()


def main():
    with open("resources/Dialogues.txt", encoding="utf-8") as f:
        dialog = [l.strip() for l in f.readlines()]

    pg.init()
    clock = pg.time.Clock()
    manager = ui.UIManager((WIDTH, HEIGHT), "ui_theme.json")

    characters: dict[str, pg.Surface] = {}
    for f_name in (Path(main_dir) / "resources/personnages").iterdir():
        characters[f_name.stem] = pg.transform.scale_by(load_image(f_name, True), 0.5)

    background = pg.transform.scale(
        load_image("lieux/auberge_exterieur.png"), (WIDTH, HEIGHT)
    )

    screen.blit(background, (0, 0))

    pg.display.set_caption("Move It!")
    pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP])

    dialog_index = 0
    minigame_index = 0
    char = characters["Ted"]

    while True:
        if dialog[dialog_index] == "__G__":
            minigame(*words[minigame_index], manager, clock)
            minigame_index += 1
            dialog_index += 1
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
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
    pg.quit()
