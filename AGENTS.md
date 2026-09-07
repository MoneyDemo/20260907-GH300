# Project Guidelines

## Architecture

Two apps share one calculation core, kept intentionally decoupled:

- [app.py](app.py) — console BMI calculator. `calculate_bmi(weight_pounds, height_meters)` and `classify_bmi(bmi)` are pure functions and are the **single source of truth** for BMI logic (thresholds 18.5 / 24 / 27, per Taiwan HPA 成人健康體位標準 — not the common WHO 25/30 cutoffs).
- [web/server.py](web/server.py) — Flask app that reuses those same functions via `sys.path` injection (`sys.path.insert(0, parent_of_web_dir)` then `from app import calculate_bmi, classify_bmi`). **Never re-implement BMI math/classification in JS** — the frontend ([web/static/js/main.js](web/static/js/main.js)) calls `POST /api/bmi` and only handles rendering/animation with the returned `{bmi, category, label}`.
- [web/prototypes/](web/prototypes) holds 3 static, self-contained HTML design concepts (A/B/C) generated when exploring visual directions; concept A ("BMI 噗噗星球") was selected and is what `web/server.py` serves. These are historical references — don't delete, but don't extend them as if they were the live app.

## Build and Test

Always use `uv` (never bare `python`/`pip`; see [~/.copilot/copilot-instructions.md] for the registry/toolchain rule):

```bash
uv run pytest              # all tests: console (tests/) + web (web/tests/)
uv run python app.py       # console calculator
uv run flask --app web/server run   # web app at http://127.0.0.1:5000/
```

`pytest.ini` sets `pythonpath = .`, so both `tests/` and `web/tests/` can `from app import ...` / `from web.server import app` without a package install.

## Conventions

- **Test style**: one test case per function, one test file per unit under test (e.g. [tests/test_calculate_bmi.py](tests/test_calculate_bmi.py), [tests/test_classify_bmi.py](tests/test_classify_bmi.py)). Every test follows explicit Arrange/Act/Assert with a Chinese comment block above it explaining the case — match this format for new tests.
- **Console app units**: weight is in **pounds**, height in **meters** (mixed units by original design) — don't silently switch to kg/cm.
- **Web API boundary validation** (in `web/server.py`): missing fields, non-numeric input, and `height <= 0` must return HTTP 400 with `{"error": "..."}`, not a 500 — `calculate_bmi` raises `ZeroDivisionError` on `height == 0` and it must be caught at the API layer.
- **GSAP CDN gotcha**: the plain `gsap.min.js` CDN bundle used in `web/static/js/main.js` does **not** support the `bezier` special property (fails silently with a console warning, no exception) — use chained two-leg tweens instead, or load `MotionPathPlugin` explicitly if a true curved path is needed.
- **GSAP tween ordering gotcha**: don't attach hover/mousemove-triggered tweens on an element while its entrance tween is still running — they fight over the same `transform`, and the entrance animation can get stuck mid-fade. Bind hover listeners inside the entrance tween's `onComplete` (see `main.js`).
