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
| 4 Chaos Arena | Extreme AI, 5x power-up spawn probability | 3 | 80 s |
| 5 Boss Gauntlet | Start with Titan boss, chaos power-ups | 3 | 90 s |

Winning a campaign match unlocks the **N** shortcut to the next level,
but all five are directly available from selection (better for Lab Tour).
**R** retries, **L** returns to challenges from game over.
**ESC** from a running campaign returns to level selection.

If time expires, higher score wins; equal score shows a draw. Boss stage 5
uses original boss physics and rewards; boss defeat can end the match.
Pauses don't count toward campaign time. Classic arcade is unchanged.

## Visuals / audio

- Four themed arenas, background from OpenGameArt CC0.
- Kenney fonts and SFX, offline asset bundle.
- HUS event branding; clearer score labels AI / HUMAN.
- Power-up HUD explicitly shows `SIZE 4.2s` and a progress meter rather
  than two unexplained orange blocks.
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
