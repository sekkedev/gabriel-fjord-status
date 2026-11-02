# Gabriel Fjord Status (hackathon prototype)

A friendly public page for the Gabriel buoy in Store Lungegårdsvann, Bergen. Gabriel greets the visitor, sums up in a few sentences how the fjord is doing, shows what has changed, and invites them further down to explore the data: a 30-day depth-by-time heatmap (pick a dive there to see it in the summary tiles at the top), a short story about why the bottom water runs out of oxygen, plain explanations of each measurement, and the latest dive's oxygen on the way down and on the way up, showing why the slow descent is the more accurate reading. Norwegian and English, light and dark theme, phone to wide screen.

Made as a concept for **Hackathon Store Lungegårdsvann**, Saturday 31 October 2026 (UiB). It was sketched before the event; the plan is to say so openly and build on it during the day. See [docs/HACKATHON.md](docs/HACKATHON.md).

> Prototype, not an official UiB page. Gabriel does not measure bacteria, so the page never says whether it is safe to swim.

## Quick start

Needs Python 3.10+ (and pandas only if you rebuild the data).

```bash
python scripts/build.py       # pages + data + assets -> dist/index.html, dist/gabby/ and dist/screen/ (self-contained files)
```

Open `dist/index.html` in a browser, or serve it so it behaves like a hosted page:

```bash
python -m http.server 8765 --directory dist
```

Then visit <http://localhost:8765/?lang=no> or `?lang=en`. Without `?lang`, the page uses the saved choice, then the browser language.

Add `diving` to the query (`?diving` or `?lang=en&diving`) to show Gabriel in the middle of a dive. This is a demo for presenting. The CTD goes down and back up on a 50-second loop, and the pill under the greeting shows depth and temperature from the latest real dive. The page labels it "demo". Under reduced motion there is no timed dive, and the CTD only follows the scroll as usual.

The page needs no network: images and fonts are built into the file.

`/gabby/` is a demo of the organisers' "Gabby" idea, the buoy posting daily about how the fjord is doing, without a real social media account. It is laid out like the Instagram mobile app's profile: a top bar with the handle, an avatar with a ring, posts/followers/following, a bio, Follow and "Fjord status" buttons, a highlight per mood, a grid of 3:4 tiles, and a "Posts" feed. It has no Instagram name, logo or login UI, uses its own icons, says in the footer that it is not affiliated with Instagram or Meta, and carries a demo strip on top. Follower and like counts are illustrative and labelled as such. Colours and sizes come from instagram.com's CSS tokens and mobile-web measurements on 30 Oct 2026 (Follow #4A5DF9, dark background #0C1014, 1 px grid gaps); the native app can differ.

There is one post per day for the month of the latest dive, computed in the browser from that day's dives in `data.json`: surface (0–2 m) temperature, salinity, turbidity and fluorescence, and deep (9 m and below) oxygen. A mood is picked from fixed rules (fresh-water runoff, algae, colder, clear, calm), and the NO/EN caption comes from fixed templates, picked by the day's context where one fits (streaks, change since yesterday). Tapping a tile opens the feed at that post. Each post's first picture is the fjord that day: a cross-section "bowl" painted from that day's dive profiles, with the fresh-water layer on top, brown when the surface is murky, green on algae days, and the low-oxygen bottom water. The surface temperature sits beside it, and four plain-word level bars (how salty, clarity, algae, deep oxygen) sit below, all using the main page's thresholds. Gabby floats small on the waterline. In the grid each tile is just the bowl and the temperature. Some days get an extra picture picked by rules (dive by dive, a top-3 record, a Sunday week recap, a quiz), and every post ends with the day's numbers. Swipe, use the arrow buttons, or press Left/Right. Escape or the back button returns to the grid. Runoff posts say Gabriel can't measure bacteria, and no post says whether it is safe to swim.

`/screen/` is a silent screen for a small public display such as Bybanen, where people look for a few seconds and can't touch it. It rotates every 8 seconds through big one-fact slides built from the latest dive: the surface temperature by Bystasjonen, the rain lying on top of the fjord (only when the surface is clearly fresher than the bottom), a question about oxygen at the bottom and then its answer. Gabby floats on an animated wave, blinks and pops in with each slide, with rain, a question mark or rising bubbles to match the slide, and the temperature counts up; all of it is off under reduced motion. The bar at the bottom has a QR code to gabriel.sekke.dev, a timer line to the next slide, the dive's date and the full data citation. It is in Norwegian unless the URL has `?lang=en`. `?slide=2` holds one slide (for testing or a screenshot), and the arrow keys or space step through them. The QR code is a static SVG in `prototype/assets/qr-site.svg`, made once with [segno](https://pypi.org/project/segno/); make it again if the address changes.

When the CSV in `data/` changes, rebuild the data first:

```bash
pip install pandas
python scripts/prep_data.py   # CSV -> prototype/data.json
```

## How it works

- `prototype/template.html` is the whole app: CSS, markup and vanilla JS in one file. There is no framework and no build step beyond injecting data, images and fonts.
- `scripts/prep_data.py` computes everything the page shows (latest profile and its raw descent and ascent, last 30 days per depth, week/month changes per layer, a normal-October baseline, deep oxygen by year) and writes `prototype/data.json`.
- `scripts/build.py` builds each page in its `PAGES` map: it inlines `prototype/base.css` where the page says `/*__BASE_CSS__*/`, replaces `__DATA__` with that JSON and every `__ASSET_<name>__` with the matching file from `prototype/assets/` (images and fonts) as a data URI, then wraps it in `<html>/<head>/<body>`. It stops with an error if an asset is missing, and copies the font licence texts to `dist/licenses/`.
- All text lives in the `T` object in both `no` and `en`. All colors are CSS tokens with light and dark values.
- The summary text is pre-written from the computed numbers in this demo. The intended pipeline is to compute facts in code, have a language model only phrase them in NO and EN, and cache the result per dive (see [docs/DESIGN.md](docs/DESIGN.md)).

## Project layout

| Path | What it is |
|---|---|
| `prototype/template.html` | The whole page (HTML, CSS, JS). Data is injected at `__DATA__`, images and fonts at `__ASSET_<name>__`. |
| `prototype/gabby.html` | Gabby's demo daily-post profile, built to `dist/gabby/index.html`. |
| `prototype/screen.html` | The silent rotating screen for Bybanen, built to `dist/screen/index.html`. |
| `prototype/base.css` | Fonts, color tokens (light and dark) and base styles shared by both pages. |
| `prototype/data.json` | Pre-computed data the pages use. |
| `prototype/assets/` | Illustrations as WebP: buoy, CTD, fish and five parameter icons. AI-generated in a soft flat vector style, transparent backgrounds. Also the fonts as WOFF2 with their license texts: full Raleway (only compressed, as its Reserved Font Name requires) and Open Sans' latin subset from Google Fonts. |
| `scripts/prep_data.py` | Builds `data.json` from the CSVs in `data/` with pandas. |
| `scripts/build.py` | Combines each page, base CSS, data and assets into `dist/`, and copies `prototype/_headers` next to them. |
| `prototype/_headers` | Response headers for the hosted page (CSP, HSTS and friends). |
| `wrangler.toml` | Cloudflare Worker that serves `dist/` at gabriel.sekke.dev. |
| `data/` | Full Gabriel dataset, 2015-05-12 to 2026-10-20, resampled to 1 m depth bins (about 34 MB), plus the raw samples for 20 Sep to 20 Oct 2026 (about 1 MB). |
| `docs/HACKATHON.md` | Event details, programme, context, contacts, entry ideas. |
| `docs/DATA.md` | Dataset notes, columns, quirks, what Gabriel does not measure, citation. |
| `docs/DESIGN.md` | Page structure, style, motion, breakpoints, next steps. |
| `CLAUDE.md` | Working notes and rules for AI coding agents in this repo. |
| `LICENSE` | MIT for our own work, and the terms of the third-party data and fonts. |

`dist/` is build output and is not committed.

## Deploy

The page is live at <https://gabriel.sekke.dev>, served by a static-assets-only Cloudflare Worker (`gabriel-fjord`, see `wrangler.toml`). To deploy, run `python scripts/build.py`, then `npx wrangler deploy` with two environment variables set:

- `CLOUDFLARE_API_TOKEN`: a token from the "Edit Cloudflare Workers" template, scoped to the account and the `sekke.dev` zone, with an expiry.
- `CLOUDFLARE_ACCOUNT_ID`: the Cloudflare account ID.

The first deploy creates the `gabriel.sekke.dev` custom domain and its DNS record. To try the hosted behaviour (headers included) locally: `python scripts/build.py`, then `npx wrangler dev --ip 127.0.0.1`.

## Rules worth keeping

- Never say or imply it is safe to swim.
- Compare temperature, salinity and oxygen across years, but not fluorescence or turbidity (the sensors changed).
- Keep the data citation and the "prototype, not official UiB" note in the footer.
- Every new string in both languages; every color as a light/dark token.
- No horizontal scroll at phone width, and every animation off under `prefers-reduced-motion`.

## Data and citation

Data from the Gabriel buoy, operated by Amalie Skram VGS, UiB and Bergen Marine Forskningsklynge, downloaded from [Ekte data](https://ektedata.uib.no/gabriel/). Cite it when publishing:

> Muilwijk, M., Drange, H., Paasche, Ø. (2017). Gabriel conductivity-temperature-depth (CTD), oxygen, fluorescence and turbidity data from Store Lungegårdsvann in Bergen [Data set]. University of Bergen, Norway.

The [Ekte data download page](https://ektedata.uib.no/gabriel/data/) says the data is free for everyone but published data must be cited correctly ("må siteres korrekt"), and asks anyone publishing Gabriel data to contact post@skolelab.uib.no. The page is public at gabriel.sekke.dev, so keep the citation in the footer and make sure Skolelab has been told.

Fonts: [Raleway](https://github.com/googlefonts/raleway) (Copyright 2010 The Raleway Project Authors, Reserved Font Name "Raleway") and [Open Sans](https://github.com/googlefonts/opensans) (Copyright 2020 The Open Sans Project Authors). Both are licensed under the SIL Open Font License 1.1; see `prototype/assets/font-*-OFL.txt`. The build copies those texts to `/licenses/` on the site, and the footers of the main page and Gabby link to them.

## Licence

Our own code, text and illustrations are under the MIT licence. The Gabriel data and the fonts keep their own terms; [LICENSE](LICENSE) lists them.

## Status

Working prototype with static data up to 20 October 2026, hosted at gabriel.sekke.dev. No live data feed yet. Next steps (live data, a real summary pipeline, a runoff detector, a daily "Gabby" post) are listed in [docs/DESIGN.md](docs/DESIGN.md).
