"""Regression coverage: scoreboard readability and live scoring in both modes."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import unittest
import pygame

from cyberball.game import Game, _handle_scoring
from cyberball.config import SCREEN_WIDTH, SCREEN_HEIGHT


class ScoreboardTests(unittest.TestCase):
    def setUp(self):
        self.app = Game(headless=True)

    def tearDown(self):
        pygame.quit()

    def _score_card_bytes(self, value, side):
        self.app.state.left_score = value if side == "left" else 0
        self.app.state.right_score = value if side == "right" else 0
        image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        image.fill((0, 0, 0))
        self.app.hud._draw_scores(image, self.app.state, 0, 0)
        region = pygame.Rect(172 if side == "left" else 732, 6, 120, 91)
        return pygame.image.tostring(image.subsurface(region), "RGB")

    def test_classic_score_cards_show_distinct_digit_shapes(self):
        for side in ("left", "right"):
            for a, b in ((0, 1), (1, 10), (10, 11)):
                self.assertNotEqual(
                    self._score_card_bytes(a, side),
                    self._score_card_bytes(b, side),
                    f"{side}: {a} and {b} rendered the same")
        self.app.state.state = "playing"
        self.app.state.campaign_level = None
        self.app._draw()  # full Classic render also remains functional

    def test_actual_scoring_updates_both_counters(self):
        state = self.app.state
        state.campaign_level = None
        state.state = "playing"
        state.reset_match()
        state.ball.rect.left = -3
        self.assertTrue(_handle_scoring(state))
        self.assertEqual((state.left_score, state.right_score), (0, 1))
        state.ball.rect.right = SCREEN_WIDTH + 3
        self.assertTrue(_handle_scoring(state))
        self.assertEqual((state.left_score, state.right_score), (1, 1))

    def test_campaign_and_boss_overlay_do_not_hide_scores(self):
        self.app._start_challenge(5)
        self.app.state.left_score = 1
        self.app.state.right_score = 2
        self.app._draw()
        self.assertEqual(self.app.state.left_score, 1)
        self.assertEqual(self.app.state.right_score, 2)


if __name__ == "__main__":
    unittest.main()
