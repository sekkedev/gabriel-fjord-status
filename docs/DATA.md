# Gabriel data

## The buoy

- Built by SAIV AS, deployed June 2015 in Store Lungegårdsvann, next to Amalie Skram VGS.
- Surface buoy with weather station, solar panels, mobile data link. A CTD hangs on a cable and profiles from the surface towards the bottom **every 3 hours**, all year.
- Sensors: conductivity (salinity), temperature, depth, oxygen, fluorescence, turbidity. Weather: air temperature, wind speed/direction, air pressure.
- Operated by Amalie Skram VGS, UiB and Bergen Marine Forskningsklynge.
- Pages: https://ektedata.uib.no/gabriel/ , parameters: https://ektedata.uib.no/gabriel/parametere/ , about: https://ektedata.uib.no/gabriel/om

## Download page

https://ektedata.uib.no/gabrieldata/download/ is a Plotly Dash app (no documented API). Options:

- Period (graph of dives per day shows coverage)
- Depth from/to, 0.5 to 19.5 m in 1 m bins
- Interval: all data, 3 h, 6 h, 12 h, day, week, month
- All selected depths, or average over depth
- Parameters: oxygen, temperature, turbidity, salinity, fluorescence
- Format: Excel or CSV
- Separate buttons: weather data, raw data

Live data idea: ask UiB/Skolelab for a stable CSV/JSON endpoint, or script the Dash callback (`_dash-update-component`) only with their permission.

## The CSV in `data/`

`resampled_data_2015-05-12_to_2026-10-20.csv`, about 317k rows, 17,142 dives.

| Column | Unit | Notes |
|---|---|---|
| `ts` | local time | One timestamp per dive |
| `pressure_dbar` | dbar ≈ m | Depth bin centre: 0.5, 1.5 … 19.5 |
| `oxygen` | % saturation | |
| `temperature` | °C | |
| `turbidity` | FTU | |
| `salinity` | PSU | Some gaps (NaN), mostly 2015 |
| `fluorescence` | µg/l | |

`raw_2026-09-20_to_2026-10-20.csv`: the download page's "Last ned rådata" export (CSV) for 20 Sep to 20 Oct 2026, 230 dives, about 44 samples each. One row per raw sample: `ts` (the dive's start, same as above), `id`, `sessionid`, `seq` (sample order within the dive), then `salinity`, `temperature`, `pressure_dbar`, `oxygen`, `fluorescence`, `turbidity`. The export also has a per-dive `session_data.csv` (file name, weather), not kept. `prep_data.py` uses it only for the latest dive's two legs (`cast`), so it must cover the resampled file's last dive.

## Descent and ascent

Each dive goes down slowly in steps, pausing at each depth (median 32 samples), and comes up fast (median 10 samples). The first and last samples are at about 0 dbar with salinity near 0: the sensor is still in air. On the way up the sensors lag, oxygen most of all. On 20 Oct 09:00, oxygen read 73 % at 8.8 m going down and 4 % coming up. The resampled bins don't say which leg a value came from, and plain per-bin means of all samples don't reproduce them exactly, so how UiB treats the ascent is unknown. A quick test of descent-only bins for 1-20 Oct gave fresher surface water (0.1-2.3 PSU) and lower deep oxygen (0.7-1.9 points) than the resampled file, with no day crossing the 22 PSU or 40 % lines. Ask Skolelab how the resampled file is made before switching.

## Quirks and caveats

- **Big gaps:** good coverage 2015 to early 2020, almost nothing mid-2020 to 2025 (only a bit of 2022 Q1), then 2025 onwards again.
- **Sensor changes:** fluorescence and turbidity levels jump between years (2015 fluorescence ~50, 2025 ~0.05). Only compare temperature, salinity and oxygen across years.
- Recent dives reach about 17.5 m.
- The temperature graph on ektedata.uib.no/gabriel/temperatur/ rendered empty when checked on 30 Oct 2026.

## What the data shows (Oct 2026)

- Strong layering: surface salinity ~16 (fresh runoff), ~32 at the bottom.
- Deep water nearly anoxic: ~2 % oxygen saturation below 15 m.
- Rain events visible as surface salinity crashes with turbidity spikes (about 6 Oct and 16 Oct 2026).
- Surface cooled over 2 °C in the last month.
- Deep oxygen (12.5 m+, Sep-Oct mean) varies a lot by year: 2015 25.7, 2016 21.2, 2017 1.2, 2018 9.0, 2025 35.2, 2026 8.7. No clear trend yet.

## Gabriel does NOT measure

Bacteria, pollutants, fish. One location only. Never claim it's safe to swim.

## Citation (required when publishing)

Muilwijk, M., Drange, H., Paasche, Ø. (2017). Gabriel conductivity-temperature-depth (CTD), oxygen, fluorescence and turbidity data from Store Lungegårdsvann in Bergen [Data set]. University of Bergen, Norway.

Terms, from https://ektedata.uib.no/gabriel/data/ (checked 30 Oct 2026): the data is free for everyone, published data "må siteres korrekt" (must be cited correctly), and "Ta kontakt på post@skolelab.uib.no dersom du skal publisere data fra Gabriel" (contact Skolelab if you will publish Gabriel data). No licence is named.
