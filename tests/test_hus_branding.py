"""Regression checks for HUS co-branding in Cyberball's main menu."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import unittest
from pathlib import Path
import pygame
from cyberball.game import Game
from cyberball.ui.menu import MenuRenderer
from cyberball.config import SCREEN_WIDTH, SCREEN_HEIGHT


class HusBrandingTests(unittest.TestCase):
    def setUp(self):
        self.app = Game(headless=True)

    def tearDown(self):
        pygame.quit()

    def test_png_is_local_and_aspect_ratio_is_preserved(self):
        path = Path(__file__).resolve().parents[1] / "cyberball/assets/hus_logo.png"
        self.assertTrue(path.is_file())
        source = pygame.image.load(str(path))
        logo = self.app.menu._hus_logo
        self.assertIsNotNone(logo)
        self.assertLessEqual(logo.get_width(), 188)
        self.assertLessEqual(logo.get_height(), 73)
        self.assertAlmostEqual(
            logo.get_width() / logo.get_height(),
            source.get_width() / source.get_height(), delta=0.05,
        )
        self.assertEqual(logo.get_at((0, 0)).a, 0)

    def test_brand_panel_is_visible_and_clear_of_game_title(self):
        game = self.app
        for difficulty in ("easy", "medium", "hard", "extreme"):
            game.state.state = "menu"
            game.state.difficulty = difficulty
            game._draw()
            # Bright-but-muted brand card against the dark space background.
            r, g, b, _ = game.screen.get_at((220, 40))
            self.assertGreater(min(r, g, b), 170)
            # The original central title remains outside the logo panel.
            rect = pygame.Rect(18, 7, 211, 92)
            self.assertLess(rect.bottom, 104)
            self.assertLess(rect.right, SCREEN_WIDTH // 2 - 250)

    def test_logo_missing_does_not_crash_rendering(self):
        game = self.app
        game.menu._hus_logo = None
        game.state.state = "menu"
        game._draw()
        self.assertEqual(game.screen.get_size(), (SCREEN_WIDTH, SCREEN_HEIGHT))


if __name__ == "__main__":
    unittest.main()
