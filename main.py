import os
from pathlib import Path
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


# quick function to load an image
def load_image(name: str | Path, is_char: bool = False):
    path = os.path.join(main_dir, "resources", name)
    return pg.image.load(path).convert_alpha()


def display_text(text: str, text_color: Optional[tuple[int, int, int]] = None):
    font = pg.font.Font(None, 24)

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
    rendered_text = font.render(text, True, text_color)
    text_rect = rendered_text.get_rect(
        center=(WIDTH // 2, HEIGHT - 10 - DIALOGUE_BOX_HEIGHT // 2)
    )
    screen.blit(rendered_text, text_rect)


# here's the full code
def main():
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
    text = "hello"
    final_text = "world"

    # This is a simple event handler that enables player input.
    while True:
        # Draw the background
        screen.blit(background, (0, 0))
        char = characters["Ted"]
        screen.blit(char, (100, HEIGHT - char.get_height() - DIALOGUE_BOX_HEIGHT - 10))

        display_text(text)

        for e in pg.event.get():
            keys = pg.key.get_pressed()
            if e.type == pg.QUIT or keys[pg.K_q]:
                return
            if keys[pg.K_t]:
                text = final_text
        # screen.blit(p.image, p.pos)
        clock.tick(60)
        pg.display.update()
        pg.time.delay(20)


if __name__ == "__main__":
    main()
    pg.quit()
