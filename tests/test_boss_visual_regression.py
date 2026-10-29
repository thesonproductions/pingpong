"""Regression checks for the screenshot-reported boss arena clutter."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import unittest
from unittest.mock import patch
import pygame

from cyberball.config import SCREEN_HEIGHT, SCREEN_WIDTH
from cyberball.game import Game, _spawn_powerup
from cyberball.entities.powerup import PowerUp
from cyberball.ui.effects import ScreenEffect


class BossVisualRegressionTest(unittest.TestCase):
    def setUp(self):
        self.app = Game(headless=True)
        self.app._start_challenge(5)

    def tearDown(self):
        pygame.quit()

    def test_boss_spawns_at_most_two_visible_powerups(self):
        s = self.app.state
        # Force a spawn whenever the cooldown allows, and run 1500 steps.
        with patch("cyberball.game.random.random", return_value=0):
            for frame in range(1500):
                _spawn_powerup(s)
                for p in s.powerups[:]:
                    p.update()
                    if p.expired:
                        s.powerups.remove(p)
                self.assertLessEqual(len(s.powerups), 2)

    def test_powerup_expires_after_six_seconds(self):
        item = PowerUp(420, 400, "speed")
        for _ in range(item.lifetime_frames - 1):
            item.update()
        self.assertFalse(item.expired)
        item.update()
        self.assertTrue(item.expired)

    def test_boss_warning_does_not_saturate_border_red(self):
        screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill((8, 20, 36))
        effect = ScreenEffect()
        effect.vignette((220, 40, 40), 0.20)
        effect.render_overlays(screen)
        # Border warning should not be an opaque red rectangle.
        r, g, b, _ = screen.get_at((12, SCREEN_HEIGHT // 2))
        self.assertLess(r, 60)
        self.assertGreater(b, 20)

    def test_boss_remains_active_and_draws_playfield(self):
        self.assertTrue(self.app.state.boss_manager.active)
        self.assertEqual(self.app.state.boss_manager.current_boss.boss_type, "titan")
        self.app._draw()
        self.assertEqual(self.app.state.left_score, 0)
        self.assertEqual(self.app.state.right_score, 0)

    def test_boss_hit_reduces_hp_and_returns_ball(self):
        from cyberball.game import _handle_ball_vs_boss
        state = self.app.state
        boss = state.boss_manager.current_boss
        health_before = boss.hp
        state.ball.rect.midleft = (boss.rect.right - 2, boss.rect.centery)
        state.ball.speed_x = -7.0
        self.assertTrue(_handle_ball_vs_boss(state, state.ball))
        self.assertEqual(boss.hp, health_before - 1)
        self.assertGreater(state.ball.speed_x, 0)

    def test_classic_item_spawn_also_has_reasonable_bound(self):
        self.app.state.campaign_level = None
        self.app.state.reset_match()
        s = self.app.state
        with patch("cyberball.game.random.random", return_value=0):
            for _ in range(600):
                _spawn_powerup(s)
                self.assertLessEqual(len(s.powerups), 3)


if __name__ == "__main__":
    unittest.main()
