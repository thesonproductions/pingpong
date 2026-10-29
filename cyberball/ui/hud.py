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
        # Kenney Future's square digits looked like solid coloured bars on
        # some display scales. Keep arcade fonts elsewhere, but make scores
        # immediately readable at a distance during the Lab Tour.
        self.score_font = pygame.font.Font(None, 79)
        self.score_label_font = pygame.font.Font(None, 25)
        self.ui_font = fonts['ui']
        self.small_font = fonts['small']

    def draw(self, surface, state, shake):
        shake_x, shake_y = shake
        self._draw_scores(surface, state, shake_x, shake_y)
        self._draw_combo(surface, state, shake_x, shake_y)
        self._draw_powerup_bars(surface, state)
        self._draw_footer(surface, state)

    def _draw_scores(self, surface, state, sx, sy):
        # Compact contrast panels sit outside the boss HP bar (x=302..722).
        # Fixed positions ensure scores are equally visible in Classic and
        # campaign mode, independently of the chosen space background.
        for x, label, value, color, flash in (
            (172, "AI", state.left_score, CYBER_BLUE, state.score_flash["left"]),
            (732, "HUMAN", state.right_score, NEON_PINK, state.score_flash["right"]),
        ):
            card = pygame.Rect(x, 6, 120, 91)
            pygame.draw.rect(surface, (5, 16, 31), card, border_radius=13)
            pygame.draw.rect(surface, color, card, width=2, border_radius=13)
            label_surface = self.score_label_font.render(label, True, color)
            surface.blit(label_surface, label_surface.get_rect(
                center=(card.centerx, card.top + 17)))
            number_surface = self.score_font.render(
                str(value), True, self._flash_color(color, flash))
            surface.blit(number_surface, number_surface.get_rect(
                center=(card.centerx, card.top + 56)))

        for side in ("left", "right"):
            if state.score_flash[side] > 0:
                state.score_flash[side] -= 1

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
