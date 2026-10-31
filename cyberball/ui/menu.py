"""Menu, pause, and HUD rendering."""
import math
import random
from pathlib import Path
import pygame

from ..config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYBER_BLUE, NEON_PINK, NEON_GREEN,
    ELECTRIC_PURPLE, BRIGHT_WHITE, GLOW_WHITE, DIM_GRAY, DARK_CYAN,
    DIFFICULTIES, POWERUP_GOLD, MENU_ANIMATION_SPEED,
)
from ..entities.particle import Particle
from .backgrounds import MenuDemo
from . import arena


class MenuRenderer:
    def __init__(self, fonts):
        self.title_font = fonts['title']
        self.menu_font = fonts['menu']
        self.ui_font = fonts['ui']
        self.small_font = fonts['small']
        self.particles = []
        self.demo = MenuDemo()
        self._hus_logo = self._load_hus_logo()

    @staticmethod
    def _load_hus_logo():
        """Load and scale the official supplied wordmark once, retaining alpha."""
        path = Path(__file__).resolve().parent.parent / 'assets' / 'hus_logo.png'
        try:
            image = pygame.image.load(str(path)).convert_alpha()
            max_width, max_height = 188, 73
            factor = min(max_width / image.get_width(), max_height / image.get_height())
            size = (max(1, round(image.get_width() * factor)),
                    max(1, round(image.get_height() * factor)))
            return pygame.transform.smoothscale(image, size)
        except (OSError, pygame.error, ValueError, ZeroDivisionError):
            return None

    def _draw_hus_brand(self, surface):
        if self._hus_logo is None:
            return
        # Subtle light-glass treatment keeps the blue wordmark readable
        # on the dark neon background, without covering title or controls.
        rect = pygame.Rect(18, 7, 211, 92)
        shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (3, 11, 26, 115), shadow.get_rect(),
                         border_radius=15)
        surface.blit(shadow, (rect.x + 3, rect.y + 4))
        backing = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(backing, (244, 249, 255, 232), backing.get_rect(),
                         border_radius=15)
        pygame.draw.rect(backing, (172, 217, 244, 255), backing.get_rect(),
                         width=2, border_radius=15)
        surface.blit(backing, rect.topleft)
        surface.blit(self._hus_logo, self._hus_logo.get_rect(center=rect.center))

    def _spawn_bg_particle(self):
        if len(self.particles) < 20:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = random.choice([CYBER_BLUE, NEON_PINK, ELECTRIC_PURPLE, NEON_GREEN])
            self.particles.append(Particle(x, y, color))

    def draw_menu(self, surface, state):
        arena.draw(surface, state.difficulty, pygame.time.get_ticks())
        self.demo.update()
        self.demo.draw(surface)
        self._spawn_bg_particle()
        self.particles[:] = [p for p in self.particles if p.update()]
        for p in self.particles:
            p.draw(surface)

        t = pygame.time.get_ticks() * MENU_ANIMATION_SPEED

        for i in range(0, SCREEN_WIDTH, 50):
            alpha = int(50 + 30 * math.sin(t + i * 0.1))
            s = pygame.Surface((2, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((*DARK_CYAN, max(0, alpha)))
            surface.blit(s, (i, 0))

        # Keep the co-brand mark in the quiet upper-left corner.
        self._draw_hus_brand(surface)

        # Lab branding and classic Cyberball game title.
        eyebrow = self.small_font.render("LAB TOUR 2026", True, NEON_GREEN)
        surface.blit(eyebrow, eyebrow.get_rect(center=(SCREEN_WIDTH // 2, 67)))
        # Title
        title = self.title_font.render("CYBERBALL 2084", True, CYBER_BLUE)
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        ty = 112 + int(8 * math.sin(t))
        for off in [(4, 4), (-4, -4), (4, -4), (-4, 4)]:
            glow = self.title_font.render("CYBERBALL 2084", True, BRIGHT_WHITE)
            glow.set_alpha(60)
            surface.blit(glow, (tx + off[0], ty + off[1]))
        surface.blit(title, (tx, ty))

        subtitle = self.ui_font.render("HUMAN VS AI  /  NEON ARENA", True, NEON_PINK)
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, ty + 80))

        # Preview of the selected difficulty as a themed arena stage.
        stage = arena.stage_label(state.difficulty)
        st = self.small_font.render(stage + '  [1-4]', True,
                                   arena.stage_color(state.difficulty))
        surface.blit(st, st.get_rect(center=(SCREEN_WIDTH // 2, 251)))

        # Main menu
        items = [
            ("SPACE", "ARCADE: CLASSIC MATCH"),
            ("L", "CHALLENGERS: FIVE LEVELS"),
            ("1 / 2 / 3 / 4", f"DIFFICULTY: {state.difficulty.upper()}"),
            ("M", f"MODE: {state.mode.upper()}  (1P vs AI / 2P local)"),
            ("V / B", f"VOLUME: {int(state.audio.volume * 100)}%"),
            ("C", f"COLORBLIND: {'ON' if state.colorblind else 'OFF'}"),
            ("O", "SETTINGS"),
            ("ESC", "EXIT"),
        ]
        y = 282
        for key, desc in items:
            key_surf = self.menu_font.render(key, True, NEON_GREEN)
            desc_surf = self.menu_font.render(desc, True, GLOW_WHITE)
            total_w = key_surf.get_width() + 30 + desc_surf.get_width()
            x = SCREEN_WIDTH // 2 - total_w // 2
            surface.blit(key_surf, (x, y))
            surface.blit(desc_surf, (x + key_surf.get_width() + 30, y))
            y += 47

        # Stats footer
        hs = state.stats.high_score(state.difficulty)
        foot1 = self.small_font.render(
            f"Games: {state.stats.data['games_played']}  |  High Score ({state.difficulty}): {hs}",
            True, (144, 174, 203),
        )
        surface.blit(foot1, (SCREEN_WIDTH // 2 - foot1.get_width() // 2, SCREEN_HEIGHT - 60))
        foot2 = self.small_font.render(
            f"Total Hits: {state.stats.data['total_hits']}  |  Max Combo: {state.stats.data['max_combo']}  |  "
            f"Powerups: {state.stats.data['powerups_collected']}",
            True, (144, 174, 203),
        )
        surface.blit(foot2, (SCREEN_WIDTH // 2 - foot2.get_width() // 2, SCREEN_HEIGHT - 35))

    def draw_pause(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        title = self.title_font.render("PAUSED", True, NEON_GREEN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

        lines = [
            "P — Resume",
            "ESC — Back to Menu",
            "R — Reset Match",
            "V / B — Volume  -  /  +",
            "M — Toggle Mute",
        ]
        y = SCREEN_HEIGHT // 2 - 20
        for line in lines:
            s = self.menu_font.render(line, True, GLOW_WHITE)
            surface.blit(s, (SCREEN_WIDTH // 2 - s.get_width() // 2, y))
            y += 45
