# HUS Lab Tour 2026 — Cyberball 2084, V1 gameplay + V2 visuals

**Source of truth:** `/Users/macbook/projects/hus/labtour2026/Cyberball_2084`.
Branch `labtour-v2` preserves the original `main` branch.

## Launch (Mac / Conda)

```bash
conda activate labtour-pong
cd /Users/macbook/projects/hus/labtour2026/Cyberball_2084
python main.py
```

Alternative: double-click `run_labtour.command`.

## Two modes

- **SPACE on main menu — Classic Arcade:** original Cyberball 2084,
  4 difficulty options, 11-point match, boss rotation after 5 player points,
  7 power-ups and optional local 2P.
- **L on main menu — Lab Tour Five Levels:** numbered challenge select;
  click a card or press 1–5. The original Cyberball game engine is reused.

| Level | Opponent / feature | Points | Timer |
|-------|--------------------|--------|-------|
| 1 Rookie Bot | Rule-based tracking (easy) | 3 | 65 s |
| 2 Smart Tracker | Rule-based tracking (medium) | 3 | 70 s |
| 3 Predictor Pro | Rule-based trajectory prediction (hard) | 3 | 75 s |
| 4 Chaos Arena | Extreme AI, controlled power-up spawns | 3 | 80 s |
| 5 Boss Gauntlet | Start with Titan boss, chaos power-ups | 3 | 90 s |

Winning a campaign match unlocks the **N** shortcut to the next level,
but all five are directly available from selection (better for Lab Tour).
**R** retries, **L** returns to challenges from game over.
**ESC** from a running campaign returns to level selection.

If time expires, higher score wins; equal score shows a draw. Boss stage 5
uses original boss physics and rewards; boss defeat can end the match.
Pauses don't count toward campaign time. Classic arcade gameplay is preserved;
a safety cap on simultaneously visible power-ups now also applies to Classic.

## Visuals / audio

- Four themed arenas, background from OpenGameArt CC0.
- Kenney fonts and SFX, offline asset bundle.
- HUS event branding; clearer score labels AI / HUMAN.
- Power-up HUD explicitly shows `SIZE 4.2s` and a progress meter rather
  than two unexplained orange blocks.
- Boss display safety fix: reduced red warning border (24 px instead of
  80 px) and limited collectibles to 2 in Boss Gauntlet / 3 elsewhere.
  Uncollected items expire after 360 frames (6 seconds at 60 FPS), and
  a spawn cooldown stops bursts of items appearing simultaneously.
- **Visible robot bosses:** Titan has an armoured mech sprite, Barrage a
  twin-cannon flying drone, and Split two independent sentries. They are
  drawn with original Pygame vector sprites in cyberball/ui/boss_visuals.py.
  Colliders remain in the visible arena at x=170..190, while sprite art is
  now compact (Titan 115x190, Barrage 105x125, Split 103x72 each).
  Titan's actual paddle/hitbox was reduced from 300 to 192 pixels high.
  Classic non-boss AI keeps its original x=0 paddle.

## Boss combat rules (updated)

- **Defense:** A boss successfully blocking the Pong ball returns it toward
  the human player. No HP is lost on that successful defensive hit.
- **Goal past boss:** Each ball that crosses the left goal line while a
  boss is active deals 1 HP of damage to that boss, in addition to scoring.
- **Laser strike:** A player-fired laser (laser power-up, F) hitting the boss
  deals 1 HP. Boss-fired or unrelated lasers do not reduce its HP.
- **Stage 5:** Titan starts with 3 HP to match the 3-point Lab Tour game.
  Three successful goals (or a combination of goals and laser hits) defeat
  it; bonus score multipliers cannot skip HP. Losing a point does NOT reset
  Titan's health. A boss kill ends the stage with player victory.
- **Classic:** Boss HP remains as originally configured (e.g., Titan 5 HP)
  and successful kills preserve the classic bonus-point reward. Classic
  non-boss paddle behaviour is unchanged.
- Labels in the arena explain these rules: blocks do not damage the boss,
  goals and lasers do.
- **TAB** overlays how the rule-based AI calculates/predicts ball position.

## Controls

- On main menu: **L** Lab Tour, **SPACE** classic arcade,
  **1/2/3/4** select classic difficulty, **O** settings.
- On level select: **1–5** or mouse to choose a challenge, **ESC** main menu.
- In game: **UP/DOWN** move right paddle, **F** laser when active,
  **P** pause, **TAB** decision view, **R** restart, **ESC** exit current match.
- After Lab Tour match: **R** replay, **N** next level if won,
  **L** level selection, **ESC** level selection.

## AI fidelity

This repository currently implements **rule-based AI** and scripted boss
behaviour. The separate `Ping-Pong-AI-NEAT` model was **not** copied into
Cyberball because its 5-input interface and training environment differ.
Therefore level 3 is named *Predictor Pro*, NOT *Neural Challenger*.
Do not present Cyberball as a trained RL/neuroevolution demo.

## Tests

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
python -m unittest discover -s tests -v
```

CC0 assets and provenance: `cyberball/assets/ASSET_LICENSES.md`.
Original Cyberball main branch remains available via `git switch main`
after saving any local work.
