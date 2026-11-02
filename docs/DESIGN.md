# Design notes

## Concept

Visiting the page, Gabriel welcomes you, tells you in a few friendly sentences how the fjord is doing, shows what changed in the last week or month, then invites you further down for details and explanations. Aimed at the general public, not scientists.

## Page structure (top to bottom)

1. **Header:** Gabriel mark (the buoy's face), nav, theme toggle (sun/moon), NO/EN toggle. Below 760 px the nav becomes a row of chips under the brand.
2. **Hero:** "Hei! Jeg er Gabriel." + last dive time + a layered scene: sky, sea gradient, light rays, waves, bubbles, a passing fish, and the buoy art (4 solar panels, masts with weather station and light, GPS, electronics box with a friendly face). The buoy bobs and rocks, the face blinks and its eyes follow the pointer (or look down as you scroll), and the CTD hangs on a cable and lowers as you scroll past the hero.
3. **Today's summary:** Gabriel's avatar and a speech bubble. A typing indicator shows first, then the friendly AI-style text (pre-written in the demo) fades in word by word. 4 tiles with 30-day sparklines: surface temperature, surface salinity, clarity (turbidity), oxygen at the bottom. Each tile has a state pill; numbers count up and sparklines draw in.
4. **What's changed:** week / month / normal October. Three layers (surface 0.5-1.5 m, middle 2.5-8.5 m, deep 9.5 m and below) with temperature, salinity, oxygen and deltas.
5. **The fjord, top to bottom:** canvas heatmap, depth x time, last 30 days, switch between 5 parameters. Tooltip by pointer, tap or arrow keys.
6. **Story:** why the bottom is short of oxygen, a fjord cross-section diagram (fresh lid, salty bottom, sill) and a bar chart of deep oxygen by year (12.5 m and deeper; 2015 and 2018 are September only).
7. **Learn more:** parameter cards with icons, "Can I swim?" note (Gabriel doesn't measure bacteria), links to Ekte data.
8. **Footer:** "Prototype, sketched before the event, not an official UiB page" + exact data citation and the data cut-off date.
9. **"Dive with me" gauge:** fixed rail on the right from 1460 px, a bottom pill on narrower screens that appears after the hero. Scroll position maps to the latest dive's depths and shows its temperature and oxygen at that depth.

## Style

Follows ektedata.uib.no: white background, Raleway headings, Open Sans body, blue accent, light-blue rounded cards, black pill buttons, soft blob shapes. All colors are CSS tokens on `:root` with dark-mode overrides, including the scene's sky and sea.

Both fonts are built into the page as variable-weight WOFF2 (SIL OFL 1.1), so the page works offline:
- **Raleway** is the full upstream font, only compressed. Its license reserves the name "Raleway", and a subset would count as a modified font that may not use it.
- **Open Sans** is Google Fonts' latin subset. That subset lacks ₂, which Google served from a separate file, so "O₂" in the gauge falls back to the system font. Open Sans has no trend arrows at all, so those always used the system font.

Illustrations are AI-generated soft flat vector art (`prototype/assets/`), one shared palette: signal yellow, deep navy panels, charcoal, light grey, ocean blue. They sit on transparent backgrounds so they work in both themes. To make a new one, use the same style brief (flat shapes, two-tone cel shading, transparent background, no text) so the set stays consistent.

## Motion

Passive and calm: buoy bob, waves, bubbles, a fish every ~24 s, blinking. On scroll: sections fade up, the summary types and reveals, tiles count up, the heatmap sweeps in, bars grow. All of it is switched off under `prefers-reduced-motion`, and reveal states only apply when JS runs.

The `?diving` demo replaces the scroll-driven CTD with a timed dive: 30 s down, 14 s up and 6 s at the surface, on a loop. That is much faster than a real dive. Gabriel's eyes follow the CTD down. The pill under the greeting shows the depth and temperature of the latest dive's nearest 1 m row, with a "demo" tag. At 360 px and narrower the temperature is hidden so the pill never wraps.

## Breakpoints

1460 px+ side gauge rail (it needs a ~150 px gutter) · 999 px learn cards 3-up · 960 px tiles 2-up, single-column changes and story · 760 px stacked hero with a wide scene, nav chips · 699 px learn cards 2-up · 560 px compact summary, smaller heatmap, row-style learn cards · 420 px tiles as rows with the sparkline on the right · 360 px nav chips may wrap.

## Behaviour

- **Language:** `?lang=` URL param, then saved choice (localStorage `gabriel-lang`), then `navigator.languages` (nb/nn/no → Norwegian, else English). No IP geolocation, on purpose.
- **Theme:** follows `prefers-color-scheme`. The toggle sets `data-theme` on `<html>` and saves to localStorage `gabriel-theme`.
- **`?diving`:** a demo of a dive in progress for presentations. It replays the latest dive and is always labelled "demo" on the page, so it is never mistaken for live data.
- Respects `prefers-reduced-motion`.

## AI summary approach

Don't let the AI decide anything. Compute the facts in code (values, deltas, comparisons, runoff detection), then have the LLM only turn those facts into friendly text in NO and EN. Cache the result per dive (every 3 h). Keeps it accurate, cheap, and easy to defend.

## Next steps

- Live data: fetch fresh data on a schedule (needs an endpoint from UiB, see DATA.md), regenerate `data.json`
- Live dive state: show the real "diving now" state and depth from the live feed in place of the `?diving` demo
- Real LLM summary pipeline (facts JSON → prompt → cached NO/EN text)
- Runoff detector as a proper feature (surface salinity drop + turbidity rise)
- Weather data (wind, air temperature) from the separate download
- "Gabby" daily post image generated from the same facts
- Split template into components (e.g. Vite + React) if it grows
- Deploy as a static site (GitHub Pages / Netlify)
