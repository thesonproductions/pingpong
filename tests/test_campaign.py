"""Regression tests for Lab Tour campaign merged into Cyberball_2084."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import unittest
import pygame

from cyberball.game import Game, _check_match_end, _check_boss_trigger
from cyberball.ui import level_select
from cyberball.campaign import challenge, CHALLENGES
from cyberball.config import MATCH_POINT_LIMIT


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.app = Game(headless=True)

    def tearDown(self):
        pygame.quit()

    @staticmethod
    def event(key):
        return pygame.event.Event(pygame.KEYDOWN, key=key)

    def test_five_cards_selectable(self):
        self.assertEqual(len(CHALLENGES), 5)
        for n, rect in level_select.cards():
            self.assertEqual(level_select.select_at(rect.center), n)
        self.app._handle_event(self.event(pygame.K_l))
        self.assertEqual(self.app.state.state, "level_select")
        self.app._draw()
        self.app._handle_event(self.event(pygame.K_2))
        self.assertEqual(self.app.state.campaign_level, 2)
        self.assertEqual(self.app.state.state, "playing")
        self.assertEqual(self.app.state.difficulty, "medium")

    def test_campaign_ends_at_three_points(self):
        self.app._start_challenge(1)
        self.app.state.right_score = 3
        _check_match_end(self.app.state)
        self.assertEqual(self.app.state.state, "gameover")
        self.assertEqual(self.app.state.game_over_winner, "PLAYER")
        self.app._handle_event(self.event(pygame.K_n))
        self.assertEqual(self.app.state.campaign_level, 2)
        self.assertEqual(self.app.state.right_score, 0)

    def test_original_arcade_remains_eleven_points(self):
        self.app.state.campaign_level = None
        self.app.state.reset_match()
        self.app.state.state = "playing"
        self.app.state.right_score = MATCH_POINT_LIMIT - 1
        _check_match_end(self.app.state)
        self.assertEqual(self.app.state.state, "playing")
        self.app.state.right_score = MATCH_POINT_LIMIT
        _check_match_end(self.app.state)
        self.assertEqual(self.app.state.state, "gameover")

    def test_neat_is_not_mislabelled(self):
        self.assertNotIn("NEURAL", challenge(3).name)
        self.assertEqual(challenge(3).difficulty, "hard")

    def test_boss_stage_starts_with_boss_and_restores_after_loss(self):
        self.app._start_challenge(5)
        self.assertTrue(self.app.state.boss_manager.active)
        self.assertEqual(self.app.state.boss_manager.current_boss.boss_type, "titan")
        self.app.state.boss_manager.on_player_lost_point()
        self.app.state.reset_round()
        self.assertTrue(self.app.state.boss_manager.active)

    def test_time_expiration_and_pause(self):
        self.app._start_challenge(4)
        self.app.state.campaign_started_ms -= 90000
        self.app._update_playing()
        self.assertEqual(self.app.state.state, "gameover")
        self.assertEqual(self.app.state.game_over_winner, "DRAW")
        self.app._start_challenge(3)
        self.app._handle_event(self.event(pygame.K_p))
        self.assertEqual(self.app.state.state, "paused")
        remaining = self.app.state.campaign_time_left()
        self.assertGreater(remaining, 0)
        self.app._handle_event(self.event(pygame.K_p))
        self.assertEqual(self.app.state.state, "playing")

    def test_in_game_esc_returns_to_levels(self):
        self.app._start_challenge(1)
        self.app._handle_event(self.event(pygame.K_ESCAPE))
        self.assertEqual(self.app.state.state, "level_select")


if __name__ == "__main__":
    unittest.main()
