"""In-game HUD: scores, combo, powerup timers."""
import math
import pygame

from ..config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CYBER_BLUE, NEON_PINK, POWERUP_GOLD,
    NEON_GREEN, DIM_GRAY, POWERUP_DURATION, BRIGHT_WHITE, ALERT_RED,
)
from ..entities.powerup import COLORS as POWERUP_COLORS, LABELS as POWERUP_LABELS
from . import arena


def draw_boss_hp_bar(surface, boss, font):
    if boss is None:
        return
    center_x = SCREEN_WIDTH // 2
    y = 15
    name = font.render(f"BOSS: {boss.boss_type.upper()}", True, ALERT_RED)
    surface.blit(name, name.get_rect(center=(center_x, y)))
    bar_w = 420
    bar_h = 16
    bar_x = center_x - bar_w // 2
    bar_y = y + 20
    pygame.draw.rect(surface, (40, 10, 10), (bar_x, bar_y, bar_w, bar_h))
    if hasattr(boss, 'segments'):
        total = boss.hp_max
        seg_w = bar_w // max(1, total)
        filled = sum(seg.hp for seg in boss.segments)
        for i in range(filled):
            pygame.draw.rect(surface, ALERT_RED,
                             (bar_x + i * seg_w + 1, bar_y + 1, seg_w - 2, bar_h - 2))
    else:
        frac = boss.hp / max(1, boss.hp_max)
        pygame.draw.rect(surface, ALERT_RED,
                         (bar_x + 1, bar_y + 1, int((bar_w - 2) * frac), bar_h - 2))
    pygame.draw.rect(surface, BRIGHT_WHITE, (bar_x, bar_y, bar_w, bar_h), 2)


class HUD:
    def __init__(self, fonts):
        self.score_font = fonts['score']
        self.ui_font = fonts['ui']
        self.small_font = fonts['small']

    def draw(self, surface, state, shake):
        shake_x, shake_y = shake
        self._draw_scores(surface, state, shake_x, shake_y)
        self._draw_combo(surface, state, shake_x, shake_y)
        self._draw_powerup_bars(surface, state)
        self._draw_footer(surface, state)

    def _draw_scores(self, surface, state, sx, sy):
        left_color = self._flash_color(CYBER_BLUE, state.score_flash['left'])
        right_color = self._flash_color(NEON_PINK, state.score_flash['right'])

        left_label = self.small_font.render("AI", True, CYBER_BLUE)
        right_label = self.small_font.render("HUMAN", True, NEON_PINK)
        surface.blit(left_label, left_label.get_rect(center=(SCREEN_WIDTH // 4, 16)))
        surface.blit(right_label, right_label.get_rect(center=(3 * SCREEN_WIDTH // 4, 16)))
        left = self.score_font.render(str(state.left_score), True, left_color)
        right = self.score_font.render(str(state.right_score), True, right_color)
        surface.blit(left, (SCREEN_WIDTH // 4 - left.get_width() // 2 + sx, 30 + sy))
        surface.blit(right, (3 * SCREEN_WIDTH // 4 - right.get_width() // 2 + sx, 30 + sy))

        if state.score_flash['left'] > 0:
            state.score_flash['left'] -= 1
        if state.score_flash['right'] > 0:
            state.score_flash['right'] -= 1

    @staticmethod
    def _flash_color(base, flash):
        if flash <= 0:
            return base
        f = flash / 30
        return tuple(min(255, int(c + 100 * f)) for c in base)

    def _draw_combo(self, surface, state, sx, sy):
        if state.combo_counter <= 1:
            return
        combo_txt = self.ui_font.render(f"COMBO x{state.combo_counter}", True, POWERUP_GOLD)
        y = 80 + int(5 * math.sin(pygame.time.get_ticks() * 0.01))
        surface.blit(combo_txt, (SCREEN_WIDTH // 2 - combo_txt.get_width() // 2 + sx, y + sy))
        if state.score_multiplier > 1:
            mult = self.ui_font.render(f"SCORE x{state.score_multiplier:.1f}", True, NEON_GREEN)
            surface.blit(mult, (SCREEN_WIDTH // 2 - mult.get_width() // 2 + sx, y + 30 + sy))

    def _draw_powerup_bars(self, surface, state):
        if not state.active_powerups:
            return
        for idx, p in enumerate(state.active_powerups[:4]):
            # Explicit label and remaining time: avoid two ambiguous orange
            # blocks (progress bar + an acronym) at the top of the screen.
            x, y, width, height = 22, 114 + idx * 43, 245, 36
            ratio = max(0.0, min(1.0, p["duration"] / POWERUP_DURATION))
            color = POWERUP_COLORS.get(p["type"], POWERUP_GOLD)
            panel = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(panel, (5, 18, 34, 234), (0, 0, width, height),
                             border_radius=8)
            pygame.draw.rect(panel, (*color, 205), (0, 0, width, height),
                             1, border_radius=8)
            label = p["type"].replace("_", " ").upper()
            remaining = max(0.0, p["duration"] / 60.0)
            glyph = self.small_font.render(f"{label}  {remaining:.1f}s", True, color)
            panel.blit(glyph, (12, 4))
            pygame.draw.rect(panel, (42, 54, 68), (12, height-8, width-24, 4),
                             border_radius=2)
            pygame.draw.rect(panel, color,
                             (12, height-8, int((width-24)*ratio), 4),
                             border_radius=2)
            surface.blit(panel, (x, y))

    def _draw_footer(self, surface, state):
        speed = abs(state.ball.speed_x) if state.ball else 0.0
        mode = "1P" if state.mode == "1p" else "2P"
        stage = (f"LEVEL {state.campaign_level}/5" if state.campaign_level
                 else arena.stage_label(state.difficulty))
        txt = self.small_font.render(
            f"{stage}   |   {mode}   |   "
            f"TAB: AI VIEW   P: PAUSE   ESC: MENU",
            True, (147, 185, 207),
        )
        surface.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 24)))
