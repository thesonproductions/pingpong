"""New Lab Tour stage renderer / decision display regression tests."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import unittest
import pygame
from pathlib import Path

from cyberball import config
from cyberball.game import Game
from cyberball.ui import arena


class LabTourV2Test(unittest.TestCase):
    def setUp(self):
        self.game = Game(headless=True)

    def tearDown(self):
        pygame.quit()

    def test_asset_sources_and_four_arenas(self):
        self.assertTrue((arena.ASSET_DIR / "space_bg.png").exists())
        self.assertTrue((arena.ASSET_DIR / "future.ttf").exists())
        self.assertEqual(len(arena.STAGES), 4)
        self.assertEqual(len(set(arena.stage_color(stage) for stage in arena.STAGES)), 4)
        colors = []
        for stage in arena.STAGES:
            surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            arena.draw(surface, stage, now_ms=0)
            colors.append(surface.get_at((config.SCREEN_WIDTH // 2, 400))[:3])
        self.assertEqual(len(set(colors)), 4)

    def test_tab_toggles_honest_ai_overlay(self):
        g = self.game
        g.state.state = "playing"
        g.state.mode = "1p"
        self.assertFalse(g.state.ai_debug)
        g._handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_TAB))
        self.assertTrue(g.state.ai_debug)
        g._draw()
        g._handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_TAB))
        self.assertFalse(g.state.ai_debug)

    def test_stages_preview_in_menu(self):
        g = self.game
        g.state.state = "menu"
        for key, expected in ((pygame.K_1, "easy"), (pygame.K_2, "medium"),
                              (pygame.K_3, "hard"), (pygame.K_4, "extreme")):
            g._handle_event(pygame.event.Event(pygame.KEYDOWN, key=key))
            self.assertEqual(g.state.difficulty, expected)
            g._draw()


if __name__ == "__main__":
    unittest.main()
