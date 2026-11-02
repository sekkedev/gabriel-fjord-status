# CLAUDE.md

Prototype for **Hackathon Store Lungegårdsvann** (UiB, Sat 31 Oct 2026): a public-facing "fjord status" page for the Gabriel buoy. Read `docs/HACKATHON.md`, `docs/DATA.md` and `docs/DESIGN.md` before making changes.

## How it works

- `prototype/template.html` is the whole app: one file with CSS, markup and vanilla JS. No framework, no build step beyond injecting data.
- Data is injected where the template says `const D = __DATA__;`. Images and fonts in `prototype/assets/` are inlined as data URIs wherever the template says `__ASSET_<name>__` (file name without extension), so the built page needs no network.
- `?diving` is a demo-only timed dive (`DIVE`, `divePhase`, `diveFrame`). It owns the hero CTD's `--k` while it runs, and the page must always label it "demo".
- Art used more than once (buoy, CTD, fish) is defined once in the hidden `<svg class="defs">` and reused with `<use href="#art-…">`. Gabriel's face is SVG drawn over the empty grey panel of the buoy art (`FACE`, in the buoy's 600×736 coordinates).
- `scripts/prep_data.py` (pandas) turns `data/*.csv` into `prototype/data.json`.
- `scripts/build.py` writes `dist/index.html` and `dist/gabby/index.html` (`PAGES`). Run both from the project root.
- `prototype/base.css` holds the fonts, color tokens and base styles for both pages; `build.py` inlines it at `/*__BASE_CSS__*/`. New tokens shared by both pages go there, with light and dark values.
- `prototype/gabby.html` is the Gabby demo: one post per day of the latest month, computed in the browser from `D.heat` (surface = depths < 2 m, deep = 9 m and below, the main page's layers). Mood rules live in `moodOf`, captions in `T.*.cap` (fixed templates; an AI step may only rephrase these facts). Each post's first picture is the fjord that day (`card` → `fjOf`/`fjText`/`fjSym`, strings in `T.*.fj`): a bowl painted from the day's per-depth profiles (`d.prof`) at the main page's thresholds, with Gabby small on the waterline. Rules can add an extra picture after it (`slidesOf`) and pick a caption from the day's context (`captionEx`, strings in `T.*.ex`). This is work in progress, see docs/GABBY-NEXT.md. It is laid out like the Instagram mobile profile, with `--ig-*` tokens (light and dark) taken from instagram.com's CSS. Never use Instagram's logo, glyph, gradient or icon artwork (draw our own icons), and add no login UI or inputs. The name appears only in the footer's "not affiliated" line. Keep the demo strip, and keep the footer note that follower and like counts are illustrative. Never show actions by real accounts ("Liked by …", "Followed by …").
- The template has no `<html>/<head>/<body>` because it was first published as a Claude artifact. `build.py` adds them.
- `npx wrangler deploy` after a build deploys `dist/` to gabriel.sekke.dev (`wrangler.toml`). `prototype/_headers` sets a CSP that allows only inline CSS/JS, `data:` images and fonts, and same-origin scripts and requests (for the script Cloudflare injects under `/cdn-cgi/challenge-platform/`). If the page ever loads anything from the network, update the CSP in the same change.

## Key data shape (`data.json`)

- `last`: timestamp of latest dive
- `profile`: latest dive rows `[depth, temperature, salinity, oxygen, turbidity, fluorescence]`
- `cast`: latest dive's raw samples in the same row shape, split at the deepest sample into `down` and `up` (in-air samples dropped), from `data/raw_*.csv`
- `heat`: last 30 days, `ts[]`, `depths[]`, and one `[dive][depth]` matrix per parameter
- `week` / `month`: `{now, prev}` means per layer (surface/middle/deep) for temperature, salinity, oxygen
- `normal`: 1-20 Oct this year vs earlier years with data (`years`, `past`, `now`)
- `deepOxygen`: Sep-Oct mean oxygen at 12.5 m+ by year

## Rules

- Text lives in the `T` object in both `no` and `en`. Every new string needs both.
- All colors are CSS tokens with light and dark values. Never hard-code a color that only works in one theme (data colors in the heatmap and the buoy drawing are the exception).
- Never say it's safe to swim. Gabriel doesn't measure bacteria.
- Don't compare fluorescence or turbidity across years (sensor changes). Temperature, salinity and oxygen are fine.
- Keep the data citation and the "prototype, not official UiB" note in the footer.
- Must work at phone width with no horizontal scroll.
- Every animation must stop under `prefers-reduced-motion: reduce`, and content hidden for a reveal must only be hidden when the `js` class is on `<html>`.
