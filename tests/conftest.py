import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402
import pytest


@pytest.fixture(scope="session", autouse=True)
def pygame_environment():
    pygame.init()
    pygame.display.set_mode((1400, 760))
    yield
    pygame.quit()
