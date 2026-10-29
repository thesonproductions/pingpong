# HUS Lab Tour 2026 - Cyberball 2084 (V2 visual upgrade)

**Correct source repository:** Cyberball_2084. The original v4 boss and
power-up engine remains in place. The NEAT experiment in Ping-Pong-AI-NEAT
is a separate repository and is NOT used by Cyberball.

## Run on Mac

```bash
conda activate labtour-pong
cd /Users/macbook/projects/hus/labtour2026/Cyberball_2084
python main.py
```

Or double-click `run_labtour.command` in Finder.

## Improvements

- 4 individual arena themes mapped to difficulty selection (keys 1-4).
- Downloaded CC0 space background, Kenney Future fonts and Kenney SFX.
- HUS lab branding on main menu and game window title.
- Live scene preview on menu; dark space, perspective grid, theme accents.
- TAB: show/hide an honest AI policy/ball-prediction view in the match.
- Original bosses, 7 power-ups, combo, laser, physics, scoring, settings and
  persistent statistics are unchanged.
- The AI paddle uses rule-based tracking / trajectory prediction. Do not
  present it as a pretrained neural network or reinforcement learning agent.

## Controls

On menu: 1/2/3/4 chooses arena+difficulty, SPACE starts, M toggles 1P/2P.
In game: UP/DOWN moves the right player; TAB shows AI policy, F fires when
laser power-up active, P pauses, ESC menu, R restarts match.
O on menu opens settings. All assets are bundled for offline use.

## Test

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m unittest discover -s tests -v
```

Asset provenance: `cyberball/assets/ASSET_LICENSES.md`.
Branch `labtour-v2` isolates custom changes from original `main`.

**Known limitation:** Arena stages are different visual themes assigned to
the four built-in difficulties, NOT a campaign with level progression.
Boss battles remain based on points, just like Cyberball v4.
