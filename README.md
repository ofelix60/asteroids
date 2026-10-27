# asteroids

An Asteroids clone in Python + pygame. Built from the boot.dev guided project, then
taken past where the course stops.

![Python](https://img.shields.io/badge/python-3.12-blue) ![pygame](https://img.shields.io/badge/pygame-2.6.1-green)

## Run it

```bash
uv sync
uv run asteroids
```

| key | |
|---|---|
| `W` / `↑`, `S` / `↓` | thrust forward / back |
| `A` / `←`, `D` / `→` | rotate |
| `space` | shoot (0.3s cooldown) |

## Beyond the course

The guided project ends at "asteroids split when shot." These were added afterwards:

- **Lives and a game-over state machine** — not just an instant restart
- **Spawn invulnerability with a blinking ship**, driven off a timer rather than a flag,
  so the two can't disagree
- **Scoring by asteroid size** (`{1: 100, 2: 50, 3: 20}`), with a startup check that the
  score table actually covers every asteroid kind — a mismatch raises at import rather
  than silently scoring zero
- **A HUD** that re-renders when the score changes, instead of caching one surface at
  construction and freezing
- **`src/` layout, type annotations, ruff** (`E,F,I,UP,B,SIM`), and an event logger

## Known issues

- `player_died` is logged unconditionally in `player_hit`, which runs once per asteroid
  per frame — so a single death produces hundreds of events. The log call belongs inside
  the hit branch.
- mypy stopped running after the move to `src/` ("Source file found twice under different
  module names") and needs `[tool.mypy]` configuration.
- `PLAYER_INVULN_TIMER` names a duration, not a timer.

## Not the portfolio piece

This is coursework. For something closer to real work — a service deployed four ways with
probes, persistence, ingress and RBAC — see
**[scoreboard](https://github.com/ofelix60/scoreboard)**.
