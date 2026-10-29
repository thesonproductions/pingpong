"""Regressions: a boss must not take damage for successfully returning Pong."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import unittest
import pygame

from cyberball.game import (
    Game, _handle_ball_vs_boss, _handle_scoring, _laser_hits_boss
)
from cyberball.entities.boss import Titan, Barrage, Split
from cyberball.entities.laser import Laser
from cyberball.ui import boss_visuals
from cyberball.config import SCREEN_WIDTH


class BossCombatRulesTests(unittest.TestCase):
    def setUp(self):
        self.game = Game(headless=True)
        self.game._start_challenge(5)

    def tearDown(self):
        pygame.quit()

    def test_defense_no_longer_deals_damage_for_any_boss(self):
        state = self.game.state
        for cls in (Titan, Barrage, Split):
            boss = cls(170)
            state.boss_manager.current_boss = boss
            state.boss_manager.active = True
            hp_before = boss.hp
            target_y = (boss.segments[0].rect.centery if isinstance(boss, Split)
                        else boss.rect.centery)
            state.ball.rect.midleft = (boss.rect.right - 3, target_y)
            state.ball.speed_x = -7
            self.assertTrue(_handle_ball_vs_boss(state, state.ball))
            self.assertEqual(boss.hp, hp_before)
            self.assertGreater(state.ball.speed_x, 0)

    def test_three_goals_defeat_stage_five_boss(self):
        state = self.game.state
        boss = state.boss_manager.current_boss
        self.assertEqual(boss.hp, 3)
        self.assertEqual(boss.hp_max, 3)
        for goal in (1, 2, 3):
            state.ball.rect.right = -10
            self.assertTrue(_handle_scoring(state))
            self.assertEqual(state.right_score, goal)
            self.assertEqual(boss.hp, 3 - goal)
            if goal < 3:
                self.assertEqual(state.state, "playing")
                self.assertIs(state.boss_manager.current_boss, boss)
            else:
                self.assertEqual(state.state, "gameover")
                self.assertEqual(state.game_over_winner, "PLAYER")
                self.assertEqual(state.match_stats.boss_kills, 1)

    def test_opponent_goal_does_not_restore_boss_hp(self):
        state = self.game.state
        boss = state.boss_manager.current_boss
        boss.hp = 2
        state.ball.rect.left = SCREEN_WIDTH + 15
        self.assertTrue(_handle_scoring(state))
        self.assertEqual(state.left_score, 1)
        self.assertIs(state.boss_manager.current_boss, boss)
        self.assertEqual(boss.hp, 2)

    def test_laser_hits_boss_but_normal_return_does_not(self):
        state = self.game.state
        boss = state.boss_manager.current_boss
        hp_before = boss.hp
        laser = Laser(boss.rect.right, boss.rect.centery, "left")
        self.assertTrue(_laser_hits_boss(state, laser))
        self.assertEqual(boss.hp, hp_before - 1)
        self.assertFalse(_laser_hits_boss(
            state, Laser(boss.rect.right, boss.rect.centery, "right")))

    def test_laser_can_finish_campaign_boss(self):
        state = self.game.state
        boss = state.boss_manager.current_boss
        boss.hp = 1
        laser = Laser(boss.rect.right, boss.rect.centery, "left")
        self.assertTrue(_laser_hits_boss(state, laser))
        self.assertEqual(state.state, "gameover")
        self.assertEqual(state.game_over_winner, "PLAYER")
        self.assertEqual(state.match_stats.boss_kills, 1)

    def test_combo_multiplier_does_not_skip_boss_hp(self):
        state = self.game.state
        state.score_multiplier = 3.0
        state.ball.rect.right = -9
        self.assertTrue(_handle_scoring(state))
        self.assertEqual(state.right_score, 1)
        self.assertEqual(state.boss_manager.current_boss.hp, 2)
        self.assertEqual(state.state, "playing")

    def test_full_game_loop_laser_collides_with_boss(self):
        state = self.game.state
        boss = state.boss_manager.current_boss
        boss.hp = 2
        state.ball.rect.center = (SCREEN_WIDTH // 2, 400)
        state.ball.speed_x = 0
        state.ball.speed_y = 0
        state.lasers = [Laser(boss.rect.right + 24, boss.rect.centery, "left")]
        self.game._update_playing()
        self.assertEqual(boss.hp, 1)
        self.assertEqual(len(state.lasers), 0)
        self.assertEqual(state.state, "playing")

    def test_classic_boss_has_five_hp_and_missed_goal_costs_one(self):
        state = self.game.state
        state.campaign_level = None
        state.reset_match()
        state.state = "playing"
        state.boss_manager.on_player_score(5)
        boss = state.boss_manager.current_boss
        self.assertEqual(boss.hp, 5)
        state.ball.rect.right = -5
        self.assertTrue(_handle_scoring(state))
        self.assertEqual(boss.hp, 4)

    def test_visual_size_and_hitbox_are_both_compact(self):
        state = self.game.state
        titan = state.boss_manager.current_boss
        self.assertLessEqual(titan.rect.height, 195)
        self.assertLessEqual(boss_visuals.display_sprite("titan").get_height(), 195)
        self.assertLessEqual(boss_visuals.display_sprite("barrage").get_height(), 135)
        self.assertLessEqual(boss_visuals.display_sprite("split").get_height(), 80)
        self.game._draw()


if __name__ == "__main__":
    unittest.main()
