"""Offline Lab Tour arena skins. Presentation only; original mechanics unchanged.

Backdrop: drakzlin's CC0 space background. Kenney UI fonts / sprites are CC0.
"""
from functools import lru_cache
from pathlib import Path
import math
import pygame

from ..config import SCREEN_WIDTH, SCREEN_HEIGHT

ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"
STAGES = {
    "easy": ("01  //  NEON DOCK", (35, 211, 247), (9, 43, 66)),
    "medium": ("02  //  ORBITAL FIELD", (80, 232, 172), (13, 54, 51)),
    "hard": ("03  //  QUANTUM GRID", (175, 121, 255), (44, 23, 80)),
    "extreme": ("04  //  OVERDRIVE", (255, 86, 147), (79, 24, 51)),
}


@lru_cache(maxsize=1)
def _base():
    path = ASSET_DIR / "space_bg.png"
    if not path.exists():
        return None
    try:
        raw = pygame.image.load(str(path))
        return pygame.transform.smoothscale(raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        return None


@lru_cache(maxsize=4)
def _canvas(stage):
    _, accent, shade = STAGES.get(stage, STAGES["medium"])
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    background = _base()
    if background is None:
        bg.fill((5, 13, 31))
    else:
        bg.blit(background, (0, 0))
    dark = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dark.fill((3, 8, 25, 168))
    bg.blit(dark, (0, 0))
    tint = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    tint.fill((*shade, 64))
    bg.blit(tint, (0, 0))
    # Perspective floor and concentric reactor rings give each stage a distinct look.
    horizon = 505
    for x in range(-600, 1700, 110):
        pygame.draw.aaline(bg, tuple(int(v * .27) for v in accent),
                           (SCREEN_WIDTH // 2, horizon), (x, SCREEN_HEIGHT))
    for y in (537, 570, 614, 670, 739):
        pygame.draw.line(bg, tuple(int(v * .25) for v in accent),
                         (0, y), (SCREEN_WIDTH, y), 1)
    for rad in (160, 220, 290):
        pygame.draw.circle(bg, tuple(int(v * .20) for v in accent),
                           (SCREEN_WIDTH // 2, 390), rad, 1)
    # Level-specific silhouettes in the uppermost field.
    if stage == "easy":
        for i in range(5):
            pygame.draw.rect(bg, (11, 68, 90),
                             (90+i*185, 108+(i%2)*22, 58, 5), border_radius=2)
    elif stage == "medium":
        for i in range(5):
            pygame.draw.circle(bg, (16, 102, 93), (95+i*200, 180+(i%2)*62),
                               46, 1)
    elif stage == "hard":
        for i in range(0, SCREEN_WIDTH, 64):
            pygame.draw.line(bg, (36, 26, 80), (i, 0), (i+120, 440), 1)
    else:
        for i in range(8):
            x = i*143
            pygame.draw.polygon(bg, (90, 25, 62),
                                [(x, 138), (x+35, 90), (x+70, 138)], 2)
    return bg


@lru_cache(maxsize=8)
def lab_font(size=20, wide=False):
    name = "future.ttf" if wide else "future_narrow.ttf"
    path = ASSET_DIR / name
    if path.exists():
        return pygame.font.Font(str(path), size)
    return pygame.font.Font(None, size)


def stage_label(stage):
    return STAGES.get(stage, STAGES["medium"])[0]


def stage_color(stage):
    return STAGES.get(stage, STAGES["medium"])[1]


def draw(surface, stage="medium", now_ms=0, boss=False):
    """One cached static backdrop plus lightweight moving neon energy."""
    surface.blit(_canvas(stage), (0, 0))
    accent = (255, 77, 96) if boss else stage_color(stage)
    w, h = surface.get_size()
    phase = now_ms * .001
    # Pulsing side rails, never cross the active ball/paddle center.
    for x in (24, w - 24):
        for i in range(4):
            y = (int(phase*42) + i*215) % (h+110) - 55
            pygame.draw.line(surface, tuple(min(255, int(v*.65)) for v in accent),
                             (x, y), (x, y+45), 2)
    pygame.draw.rect(surface, tuple(int(v*.40) for v in accent),
                     pygame.Rect(18, 112, w-36, h-155), 1, border_radius=15)
    # A subtle moving indicator for each theme.
    px = int(w/2 + 170*math.sin(phase*.7))
    pygame.draw.circle(surface, tuple(int(v*.48) for v in accent),
                       (px, 155), 4)


def overlay_ai_decision(surface, state, label_font=None):
    """Honest look inside the hand-coded AI or boss logic; no neural claims."""
    if state.mode != "1p":
        return
    if state.boss_manager.active:
        boss = state.boss_manager.current_boss
        policy = f"BOSS: {boss.boss_type.upper()}  /  RULE-BASED"
        target_y = state.ball.rect.centery
    else:
        policy = "PREDICTIVE TRACKING  /  RULE-BASED"
        target_y = state.ball.rect.centery
        if state.difficulty in ("hard", "extreme") and state.ball.speed_x < -0.1:
            time_to_left = abs(state.ball.rect.centerx - state.left_paddle.rect.centerx) / max(abs(state.ball.speed_x), .1)
            yy = state.ball.rect.centery + (state.ball.speed_y + state.ball.spin*.1) * time_to_left
            folded = yy % (2 * SCREEN_HEIGHT)
            target_y = folded if folded <= SCREEN_HEIGHT else 2 * SCREEN_HEIGHT - folded
    accent = stage_color(state.difficulty)
    if label_font is None:
        label_font = lab_font(16)
    panel = pygame.Surface((440, 105), pygame.SRCALPHA)
    pygame.draw.rect(panel, (5, 18, 37, 235), (0, 0, 440, 105), border_radius=13)
    pygame.draw.rect(panel, (*accent, 190), (0, 0, 440, 105), 2, border_radius=13)
    lines = ("AI DECISION VIEW  [TAB]", policy,
             f"BALL Y {state.ball.rect.centery:>4}  /  TARGET Y {int(target_y):>4}")
    for i, line in enumerate(lines):
        glyph = label_font.render(line, True, accent if i == 0 else (217, 236, 247))
        panel.blit(glyph, (16, 11 + i*30))
    surface.blit(panel, (SCREEN_WIDTH//2-220, SCREEN_HEIGHT-153))
    if not state.boss_manager.active:
        # Marker at the predicted interception height for visualization.
        pred = max(110, min(SCREEN_HEIGHT-55, int(target_y)))
        pygame.draw.circle(surface, accent, (44, pred), 9, 2)
        pygame.draw.line(surface, accent, (48, pred), (94, pred), 1)
