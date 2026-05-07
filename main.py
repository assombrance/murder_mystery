from pathlib import Path
from random import randint
from typing import Annotated, Literal, Optional

import pygame as pg
import pygame_gui as ui
from pydantic import BaseModel, Field, RootModel

main_dir = Path(__file__).absolute().parent
resources = main_dir / "resources"


class Line(BaseModel):
    type: Literal["line"]
    text: str
    character: Optional[str] = None
    background: Optional[str] = None
    music: Optional[str] = None


class Minigame(BaseModel):
    type: Literal["minigame"]
    text: str
    word: str
    letters: str
    character: Optional[str] = None
    background: Optional[str] = None
    music: Optional[str] = None


# class Scenario(BaseModel):
#     lines: list[Annotated[Line | Minigame, Field(discriminator="type")]]


class Scenario(
    RootModel[list[Annotated[Line | Minigame, Field(discriminator="type")]]]
):
    pass


# Height and Width of screen
WIDTH = 640
HEIGHT = 480

DIALOGUE_BOX_WIDTH = WIDTH - 20
DIALOGUE_BOX_HEIGHT = 150

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pg.display.set_mode((WIDTH, HEIGHT))


def load_image(name: str | Path):
    return pg.image.load(resources / name).convert_alpha()


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
            display_text("Je ne vous comprends pas, pouvez-vous répéter ?")
        pg.display.update()


def play_music(song_name: str):
    pg.mixer.music.load(resources / "audios" / song_name)
    pg.mixer.music.play(loops=-1)


def main():
    with open(resources / "dialogs.json", encoding="utf-8") as f:
        dialog = Scenario.model_validate_json(f.read()).root

    pg.init()
    clock = pg.time.Clock()
    manager = ui.UIManager((WIDTH, HEIGHT), "ui_theme.json")

    characters: dict[str, pg.Surface] = {}
    for f_name in (resources / "personnages").iterdir():
        characters[f_name.stem] = pg.transform.scale_by(load_image(f_name), 0.5)

    background = pg.transform.scale(
        load_image("lieux/auberge_exterieur.png"), (WIDTH, HEIGHT)
    )

    screen.blit(background, (0, 0))

    pg.display.set_caption("Move It!")
    pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP])

    dialog_index = 0
    line = dialog[dialog_index]
    if line.music is not None:
        play_music(line.music)
    char = None

    while True:
        if line.character is not None:
            char = characters[line.character]
            screen.blit(background, (0, 0))
            screen.blit(
                char, (100, HEIGHT - char.get_height() - DIALOGUE_BOX_HEIGHT - 10)
            )
        display_text(line.text)
        if isinstance(line, Minigame):
            minigame(line.word, line.letters, manager, clock)
            dialog_index += 1
            line = dialog[dialog_index]
            screen.blit(background, (0, 0))
            if char is not None:
                screen.blit(
                    char, (100, HEIGHT - char.get_height() - DIALOGUE_BOX_HEIGHT - 10)
                )

        e = pg.event.wait()
        keys = pg.key.get_pressed()
        if e.type == pg.QUIT or keys[pg.K_q]:
            return
        if keys[pg.K_SPACE]:
            dialog_index += 1
            line = dialog[dialog_index]
            if line.music is not None:
                play_music(line.music)
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
    pg.quit()
