import os
from pathlib import Path

import pygame as pg
import pygame_gui as ui

main_dir = os.path.split(os.path.abspath(__file__))[0]


# Height and Width of screen
WIDTH = 640
HEIGHT = 480
# Height and width of the sprite
SPRITE_WIDTH = 80
SPRITE_HEIGHT = 100

DIALOGUE_BOX_WIDTH = 300
DIALOGUE_BOX_HEIGHT = 150


# quick function to load an image
def load_image(name: str | Path):
    path = os.path.join(main_dir, "resources", name)
    return pg.image.load(path).convert()


# here's the full code
def main():
    pg.init()
    manager = ui.UIManager((WIDTH, HEIGHT))

    font = pg.font.Font(None, 24)
    text_color = (0, 0, 0)

    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    characters = {}
    for f_name in (Path(main_dir) / "resources/personnages").iterdir():
        characters[f_name.stem] = pg.transform.scale(
            load_image(f_name), (SPRITE_WIDTH, SPRITE_HEIGHT)
        )
    # entity = load_image("alien1.gif")
    background = pg.transform.scale(
        load_image("lieux/auberge_exterieur.png"), (WIDTH, HEIGHT)
    )

    screen.blit(background, (0, 0))

    pg.display.set_caption("Move It!")

    # This is a simple event handler that enables player input.
    while True:
        # Draw the background
        screen.blit(background, (0, 0))
        screen.blit(characters["Ted"], (100, HEIGHT - SPRITE_HEIGHT))
        pg.draw.rect(
            screen,
            (255, 255, 255),
            (
                (WIDTH - DIALOGUE_BOX_WIDTH) // 2,
                HEIGHT - DIALOGUE_BOX_HEIGHT - 50,
                DIALOGUE_BOX_WIDTH,
                DIALOGUE_BOX_HEIGHT,
            ),
        )
        rendered_text = font.render("hello world", True, text_color)
        text_rect = rendered_text.get_rect(
            center=(WIDTH // 2, HEIGHT - 50 - DIALOGUE_BOX_HEIGHT // 2)
        )
        screen.blit(rendered_text, text_rect)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        # screen.blit(p.image, p.pos)
        clock.tick(60)
        pg.display.update()
        pg.time.delay(20)


if __name__ == "__main__":
    main()
    pg.quit()
