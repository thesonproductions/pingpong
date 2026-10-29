"""Distinct original vector-style cyberpunk boss characters for Cyberball.

Visuals are procedurally drawn on transparent Pygame sprites. They use no
external artwork, and their rightmost glowing guard is aligned exactly with
the boss collision rectangle's right edge.
"""
from functools import lru_cache
import math
import pygame


RED = (249, 65, 101)
HOT = (255, 119, 140)
SHADOW = (16, 13, 35)
STEEL = (38, 44, 76)
MID = (82, 87, 132)
LIGHT = (177, 194, 222)
CYAN = (50, 229, 241)
GOLD = (254, 202, 102)
PURPLE = (177, 115, 252)


def poly(canvas, points, fill, line=HOT, width=3):
    pygame.draw.polygon(canvas, fill, points)
    pygame.draw.polygon(canvas, line, points, width)


def aura(canvas, pos, size, color):
    x, y = pos
    for radius, a in ((size+19, 12), (size+12, 23), (size+6, 44)):
        pygame.draw.circle(canvas, (*color, a), (x, y), radius)
    pygame.draw.circle(canvas, (17, 28, 50), (x, y), size+3)
    pygame.draw.circle(canvas, color, (x, y), size, 3)
    pygame.draw.circle(canvas, (*color, 160), (x, y), max(3, size-7))


def titan(canvas):
    # Massive twin-shouldered armored titan, facing right.
    for points in (
        [(54, 53), (18, 83), (20, 151), (58, 176), (71, 132)],
        [(126, 53), (162, 83), (160, 151), (125, 176), (112, 132)]
    ):
        poly(canvas, points, (39, 45, 76), (146, 76, 102), 4)
    for x in (30, 136):
        poly(canvas, [(x, 92), (x+12, 86), (x+18, 103), (x+18, 163),
                      (x+4, 182), (x-7, 153)], (53, 63, 94), RED, 3)
        pygame.draw.circle(canvas, CYAN, (x+10, 136), 5)
    # Mechanic legs / thruster units.
    for x in (51, 107):
        poly(canvas, [(x, 200), (x+34, 202), (x+27, 258),
                      (x+4, 267), (x-6, 250)],
             (41, 56, 90), (112, 135, 180), 3)
        pygame.draw.rect(canvas, RED, (x+4, 252, 18, 4), border_radius=2)
        pygame.draw.polygon(canvas, (80, 204, 239),
                            [(x+4, 267), (x+25, 267), (x+15, 284)])
    poly(canvas, [(47, 115), (90, 99), (137, 115), (143, 188),
                  (118, 233), (61, 233), (37, 188)],
         (35, 44, 77), LIGHT, 4)
    poly(canvas, [(58, 134), (90, 123), (123, 134), (131, 174),
                  (115, 209), (66, 209), (50, 174)],
         (23, 32, 60), RED, 3)
    # Helmet crown, visor and angular horns.
    poly(canvas, [(54, 72), (36, 35), (59, 44), (73, 16), (107, 16),
                  (122, 44), (145, 35), (126, 72), (123, 109), (57, 109)],
         (45, 51, 87), HOT, 4)
    poly(canvas, [(55, 76), (72, 66), (111, 66), (127, 76),
                  (115, 92), (70, 92)],
         (11, 20, 43), CYAN, 3)
    pygame.draw.line(canvas, (84, 247, 250), (74, 80), (108, 80), 5)
    pygame.draw.line(canvas, LIGHT, (76, 108), (105, 108), 3)
    aura(canvas, (90, 165), 21, RED)
    pygame.draw.line(canvas, CYAN, (69, 202), (110, 202), 3)
    for x in (63, 74, 85, 96, 107):
        pygame.draw.line(canvas, GOLD, (x, 216), (x+5, 216), 2)


def barrage(canvas):
    # Floating assault drone with paired forward cannons.
    for x in (44, 123):
        poly(canvas, [(x-16, 89), (x+15, 81), (x+28, 116),
                      (x+15, 177), (x-16, 165)],
             STEEL, RED, 3)
        poly(canvas, [(x, 113), (x+39, 118), (x+42, 147), (x, 152)],
             (37, 40, 72), GOLD, 3)
        pygame.draw.rect(canvas, (10, 18, 34), (x+19, 126, 18, 12))
        pygame.draw.rect(canvas, CYAN, (x+27, 129, 13, 6))
    poly(canvas, [(90, 43), (122, 67), (134, 119),
                  (120, 189), (90, 216), (60, 189), (46, 119), (58, 67)],
         (41, 45, 79), (218, 78, 131), 4)
    poly(canvas, [(90, 69), (113, 95), (119, 138),
                  (104, 174), (76, 174), (61, 138), (67, 95)],
         (19, 28, 53), CYAN, 2)
    aura(canvas, (90, 126), 29, PURPLE)
    for dx in (-22, 22):
        pygame.draw.circle(canvas, HOT, (90+dx, 75), 7)
    pygame.draw.polygon(canvas, (88, 222, 255),
                        [(70, 205), (85, 239), (101, 205)])
    pygame.draw.polygon(canvas, (88, 222, 255),
                        [(110, 205), (126, 239), (140, 205)])


def split_drone(canvas):
    # Deliberately different small unit for each of Split's two colliders.
    poly(canvas, [(40, 36), (22, 54), (31, 102), (58, 117),
                  (118, 117), (151, 98), (157, 54), (127, 34)],
         (37, 48, 83), PURPLE, 3)
    poly(canvas, [(50, 35), (65, 18), (116, 18), (136, 35),
                  (129, 80), (106, 99), (65, 99), (47, 80)],
         (28, 34, 65), LIGHT, 3)
    pygame.draw.rect(canvas, (11, 24, 44), (59, 50, 65, 26),
                     border_radius=6)
    pygame.draw.line(canvas, CYAN, (68, 63), (83, 63), 5)
    pygame.draw.line(canvas, RED, (103, 63), (117, 63), 5)
    aura(canvas, (91, 96), 11, PURPLE)
    for x in (34, 144):
        pygame.draw.circle(canvas, HOT, (x, 80), 8, 2)


@lru_cache(maxsize=3)
def sprite(kind):
    if kind == "titan":
        canvas = pygame.Surface((193, 300), pygame.SRCALPHA)
        titan(canvas)
    elif kind == "barrage":
        canvas = pygame.Surface((193, 255), pygame.SRCALPHA)
        barrage(canvas)
    else:
        canvas = pygame.Surface((193, 138), pygame.SRCALPHA)
        split_drone(canvas)
    return canvas


def draw_boss(surface, boss, shake=(0, 0), time_ms=0):
    """Render boss and accurate guard at the front of its collidable hitbox."""
    sx, sy = shake
    kind = boss.boss_type
    pulse = 0.7 + 0.3 * math.sin(time_ms * 0.007)
    if kind == "split":
        centers = [
            (segment.rect, i)
            for i, segment in enumerate(boss.segments) if segment.hp > 0
        ]
    else:
        centers = [(boss.rect, None)]
    for rect, _ in centers:
        art = sprite(kind)
        # Sprite front edge == collision right edge, not an invisible x=0 paddle.
        x = rect.right - 180 + sx
        y = rect.centery - art.get_height() // 2 + sy
        surface.blit(art, (x, y))
        guard = pygame.Rect(rect.right - 7 + sx, rect.top + sy, 10, rect.height)
        pygame.draw.rect(surface, (158, 39, 82), guard, border_radius=4)
        pygame.draw.rect(surface, HOT, guard, 2, border_radius=4)
        for yy in range(guard.top + 12, guard.bottom - 2, 24):
            pygame.draw.line(surface, CYAN, (guard.left+2, yy),
                             (guard.right-3, yy), 2)
        # Small hit markers identify the actual damageable guard.
        pygame.draw.circle(surface, GOLD, (rect.right-2 + sx, rect.centery+sy),
                           int(5 + 2 * pulse), 2)

    # Boss type and remaining HP stay tethered to the moving sprite.
    top = min(segment.rect.top for segment in boss.segments) if kind == "split" else boss.rect.top
    top = max(111, top - 26)
    font = pygame.font.Font(None, 23)
    label = font.render(f"{kind.upper()}  HP {boss.hp}/{boss.hp_max}",
                        True, (255, 223, 231))
    surface.blit(label, (max(16, boss.rect.right - 148 + sx), top + sy))
