"""Visual and mechanics regressions for visible robot boss characters."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import unittest
import pygame
from cyberball.game import Game, _handle_ball_vs_boss
from cyberball.entities.boss import Titan, Barrage, Split
from cyberball.ui import boss_visuals


class BossSpriteVisualTests(unittest.TestCase):
    def setUp(self):
        self.app = Game(headless=True)
        self.app._start_challenge(5)

    def tearDown(self):
        pygame.quit()

    def test_titan_is_in_arena_not_at_left_screen_edge(self):
        boss = self.app.state.boss_manager.current_boss
        self.assertIsInstance(boss, Titan)
        self.assertGreaterEqual(boss.rect.x, 100)
        self.assertLess(boss.rect.right, 300)
        self.app._draw()
        # Front guard must be visually distinct from the space background.
        pixel = self.app.screen.get_at((boss.rect.right-2, boss.rect.centery))[:3]
        self.assertGreater(pixel[0], 100)
        self.assertGreater(pixel[0], pixel[2])

    def test_three_unique_sprites_have_substantial_visible_pixels(self):
        hashes = []
        for kind in ("titan", "barrage", "split"):
            art = boss_visuals.sprite(kind)
            self.assertGreater(art.get_width(), 150)
            mask = pygame.mask.from_surface(art, threshold=20)
            self.assertGreater(mask.count(), 2000, kind)
            hashes.append(pygame.image.tostring(art, "RGBA"))
        self.assertEqual(len(set(hashes)), 3)

    def test_hitboxes_are_on_visible_front_shields(self):
        for cls in (Titan, Barrage, Split):
            with self.subTest(cls=cls.__name__):
                boss = cls(x=170)
                state = self.app.state
                state.boss_manager.current_boss = boss
                state.boss_manager.active = True
                self.assertEqual(boss.rect.right, 190)
                art = pygame.Surface(self.app.screen.get_size(), pygame.SRCALPHA)
                boss_visuals.draw_boss(art, boss, (0,0), 300)
                front_x = boss.rect.right - 2
                sample_y = (boss.segments[0].rect.centery if isinstance(boss, Split)
                            else boss.rect.centery)
                self.assertGreater(art.get_at((front_x, sample_y))[3], 150)
                health_before = boss.hp
                self.app.state.ball.rect.midleft = (front_x, sample_y)
                self.app.state.ball.speed_x = -7.0
                self.assertTrue(_handle_ball_vs_boss(state, state.ball))
                self.assertEqual(boss.hp, health_before - 1)
                self.assertGreater(state.ball.speed_x, 0)

    def test_split_segments_draw_separately_and_hide_dead_half(self):
        boss = Split(x=170)
        a = pygame.Surface(self.app.screen.get_size(), pygame.SRCALPHA)
        boss_visuals.draw_boss(a, boss)
        self.assertGreater(a.get_at((boss.rect.right-2,
                                      boss.segments[0].rect.centery))[3], 150)
        self.assertGreater(a.get_at((boss.rect.right-2,
                                      boss.segments[1].rect.centery))[3], 150)
        boss.segments[0].hp = 0
        boss.hp = boss.segments[1].hp
        b = pygame.Surface(self.app.screen.get_size(), pygame.SRCALPHA)
        boss_visuals.draw_boss(b, boss)
        self.assertEqual(b.get_at((boss.rect.right-2,
                                    boss.segments[0].rect.centery))[3], 0)
        self.assertGreater(b.get_at((boss.rect.right-2,
                                      boss.segments[1].rect.centery))[3], 150)

    def test_normal_arcade_paddle_is_not_moved(self):
        state = self.app.state
        state.campaign_level = None
        state.reset_match()
        self.assertEqual(state.left_paddle.rect.x, 0)
        self.assertFalse(state.boss_manager.active)
        self.assertEqual(state.boss_manager.boss_x, 170)


if __name__ == "__main__":
    unittest.main()
