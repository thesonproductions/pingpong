"""Keyboard/mouse level-selection screen, designed for fast Lab Tour turnover."""
import pygame
from . import arena
from ..campaign import CHALLENGES
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT


def cards():
    return [(level.number, pygame.Rect(95, 158 + (level.number-1)*101,
                                       SCREEN_WIDTH-190, 88))
            for level in CHALLENGES]


def select_at(pos):
    return next((n for n, rect in cards() if rect.collidepoint(pos)), None)


def draw(surface, fonts, selected=1):
    arena.draw(surface, "medium", pygame.time.get_ticks())
    title_font = arena.lab_font(38, wide=True)
    ui_font = arena.lab_font(20)
    label_font = arena.lab_font(16)
    title = title_font.render("HUMAN VS AI  /  5 CHALLENGES", True, (236, 246, 255))
    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 67)))
    hint = ui_font.render("CHOOSE A LEVEL (1-5)  |  ESC: MENU", True, (137, 197, 229))
    surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, 112)))
    mouse = pygame.mouse.get_pos()
    for level in CHALLENGES:
        number, rect = cards()[level.number-1]
        accent = arena.stage_color(level.difficulty)
        hovered = rect.collidepoint(mouse)
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (8, 26, 51, 238), panel.get_rect(), border_radius=13)
        pygame.draw.rect(panel, (*accent, 255 if hovered else 155),
                         panel.get_rect(), 2, border_radius=13)
        pygame.draw.rect(panel, accent, (0, 0, 5, rect.height), border_radius=2)
        surface.blit(panel, rect.topleft)
        num = title_font.render(f"{number:02d}", True, accent)
        surface.blit(num, (rect.x+17, rect.y+16))
        name = ui_font.render(level.name, True, (241, 248, 255))
        surface.blit(name, (rect.x+103, rect.y+12))
        details = label_font.render(level.objective, True, (153, 181, 211))
        surface.blit(details, (rect.x+103, rect.y+49))
        meta = label_font.render(f"{level.points} PTS  /  {level.seconds}s",
                                 True, accent)
        surface.blit(meta, meta.get_rect(midright=(rect.right-20, rect.centery)))
    footer = label_font.render("Rule-based AI with 3 Cyberball bosses and 7 power-ups",
                               True, (161, 198, 215))
    surface.blit(footer, footer.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-36)))
