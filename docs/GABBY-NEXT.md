# Gabby: where we are and what's next

Working notes for continuing the Gabby demo (`/gabby/`) at Hackathon Store Lungegårdsvann, Saturday 31 October 2026. Issue #15.

## Direction (30 Oct, evening)

The owner's call after seeing the examples:

> Gabby isn't the main thing, the fjord that day is. We need to visualise the fjord's condition that day in a way that speaks to the average local who's just checking in.

So each post's first picture should show **the fjord's condition that day**, and Gabby becomes a small mascot (reacting, signing off), not the subject. The new post types below are still useful, as long as the fjord stays the subject.

## The fjord picture ("the fjord bowl"), built

Every post now opens with the fjord that day (`card` → `fjOf`, `fjText`, `fjSym`, `fjFeed`, `fjTile`; strings in `T.*.fj`).

**How it was chosen.** Four concepts were drafted from the real data: a weather-app style card, a cut-through "window into the water", a sample jar, and a plain-words front page. Three judges then scored them: an average local on the bus, the organisers' data and honesty reviewer, and the front-end developer. The weather-app card won on the 3-second test, and the window won on honesty. The merged design takes the card's layout and the window's measured layers, plus the front page's record/streak chip.

**What it shows:**
- **The bowl:** a cross-section of the fjord right under the buoy, painted from that day's mean depth profiles:
  - pale fresh-water layer on top, down to where salinity first reaches 22 PSU (labelled "Ferskvann ca. 3 m");
  - brown with specks only when the surface is murky (≥ 1 FTU);
  - green with dots only on algae days (moodOf's rule);
  - dark bottom water from where oxygen stays under 40 % ("Lite oksygen").
  - The top 5 m get 55 % of the height so thin layers show; the feed picture has a ruler.
- **A mark above the bowl:** inflow arrows (runoff), a thermometer with a down arrow (colder), a sparkle (clear sea water), or nothing.
- **Beside it:** the surface temperature, a word (Kjølig / Mildt, the main page's 6/12/17 °C cut-offs) and the change since yesterday from the shown values. A chip ("Kaldest hittil i oktober", "3. dag på rad") appears only when that is true.
- **Below:**
  - the headline;
  - four level bars at the main page's thresholds: how salty, clarity, algae vs. the level since 20 Sep, oxygen from 9 m down;
  - Gabby's sign-off: the runoff/bacteria line on runoff days, otherwise the bio's "I don't measure bacteria" line.
- **Gabby** floats small on the waterline with the day's face, and the CTD cable hangs down through the layers, so the picture reads as "measured at this one point".
- **Grid tile:** the bowl and the temperature only, so the month reads like a forecast's day list.

**Decisions to review:**
- The fjord picture comes first on every post, including the six days with an extra cover; those covers are now the second picture. The other order is one line in `slidesOf`: `[...lead,card(d),sheet(d)]`.
- The footer mentions swimming on non-runoff days (the bio's own wording). If that feels too close to the line, shorten it to "Jeg måler ikke bakterier." / "I don't measure bacteria."
- The oxygen row says "Lavt / Low" on all 20 days. A judge suggested a comparison, or wording that says this is normal for the basin, so it doesn't alarm every day.
- Calm days look alike on the grid (10 and 11 Oct are identical tiles), on purpose: nothing is invented to tell them apart. In the feed every pair differs in at least three ways.
- The chip's width is estimated from its character count. "Freshest so far in September" would overflow, so make it wrap or measure it before other months.

## What else this branch has

These are extra pictures after the fjord picture, built from `data.json` in the browser:

| Day (Oct 2026) | Extra picture | Rule |
|---|---|---|
| 5, 15 | **Dive by dive**: the day's dives as columns over the top 10 m, in the main page's salinity colours, with each dive's surface value | the surface swings 8 PSU or more between dives (`swingOf`) |
| 6 | **Top 3**: "6.2 PSU, 3rd freshest of the 1,705 days I've measured" | `REC`, hard-coded for now |
| 11, 18 | **Week recap**: the ISO week number, the week's 7 Gabby faces, dives, salinity range, temperature start → end | a Sunday whose Monday-Sunday week is all in the month (`isRecap`) |
| 14 | **Quiz**: "How much oxygen did I measure 17.5 m down today?" with three real values, answer on the next picture | `QUIZ`, one fixed day for now |
Posts can now have any number of pictures (`slidesOf`); the counter and dots follow. The old mood card (Gabby big in the middle) is gone.

Captions are picked from the day's context (`captionEx`), falling back to the mood's own template:

- algae streaks: "Still green, day 3: 3.61 µg/l at the surface, up from 2.15 yesterday", and "the greenest day so far" on 4 Oct;
- calm days rotate: same as yesterday (11, 18 Oct), deep oxygen (8, 12 Oct), change since yesterday (10 Oct), the original (7, 20 Oct);
- cold days: "Coldest day of the month so far" (17 Oct), "Brr, again!" (19 Oct), only when it really is the month's lowest;
- clear days: "Last Tuesday the top was down at 6.2 PSU. Today: 23.0 PSU" (13 Oct), when salinity moved 10 PSU or more in a week;
- runoff days keep the bacteria sentence and add when it happened: "from 24.9 PSU at 03:00 to 7.8 PSU at 21:00" (15 Oct).

## How to see it

```bash
python scripts/build.py
python -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Then open <http://127.0.0.1:8765/gabby/?lang=en>. To test the CSP headers too, use `npx wrangler dev --ip 127.0.0.1` instead.

## Idea list, checked against the data

Ideas from four angles (social formats, data stories, voice, visuals). A sceptical reviewer recomputed every number from `data.json` and `data/*.csv`. Ranked:

| # | Idea | When | Status |
|---|---|---|---|
| 1 | Dive-by-dive cover and a "when it happened" caption line | 5, 15 Oct (cover); 7, 16 Oct could get it as a slide | in the branch |
| 2 | Big-number cover for records, seasonal firsts and dive milestones | 6 Oct (3rd freshest); 9 Oct coldest surface since 26 May (10.3 °C); 17 Oct first day under 11 °C this autumn; dive no. 17,000 on 1 Oct | only 6 Oct, hard-coded |
| 3 | Caption engine: templates picked by context | every day | first version in the branch |
| 4 | Sunday week recap | 11, 18 Oct | in the branch |
| 5 | Same date in other years (2016, 2025): surface temperature and deep oxygen side by side | Thursdays; caption lines on 6, 12, 19 Oct | not started; needs `prep_data.py` |
| 6 | Wednesday quiz, swipe for the answer | 7, 14 Oct | 14 Oct only |
| 7 | "Day 70 of low oxygen deep down" badge: days in a row under 40 % from 9 m down, since 3 Aug | every card | not started; needs `prep_data.py` |
| 8 | Fresh-water spell, "day n" chip | 5-8 and 15-18 Oct | not started |
| 9 | Today's water column: a depth-profile slide, "5.5 m down it's still 12.3 °C" | 6, 9, 19 Oct | not started |
| 10 | Before/after split, one week apart | 13 Oct | caption only |

Things the reviewer caught, worth keeping in mind:

- The record has almost no data from mid-2020 to 2025, so say "in my records" or give a rank, never a bare "since 2016".
- The CSV has duplicate (time, depth) rows; average them before computing records.
- `D.heat` is a sliding 30-day window, so "since 20 September" is the start of the page's data, not a fact about the fjord.
- Say "what looks like runoff", keep the bacteria sentence, and never word a recovery as an all-clear.
- Never say "the bottom" when you mean "17.5 m, averaged over today's dives".

## Next steps

1. Look at the fjord picture on a real phone, and settle the "Decisions to review" above.
2. Compute `REC` in `scripts/prep_data.py` (pandas, per-cell dedupe), then add the other records and firsts from idea 2.
3. Turn `QUIZ` into a Wednesday rule with rotating questions.
4. Check every picture at tile size on a phone, in both themes and both languages.
5. Before merging: update the CLAUDE.md data-shape list if `data.json` gets new fields.

## Rules that still apply

See CLAUDE.md. In short: never say it's safe (or unsafe) to swim; don't compare turbidity or fluorescence across years; every string in NO and EN; colours as light/dark tokens (data colours excepted); animations off under reduced motion; no Instagram branding and no fake accounts.
