# The World in One Image — 13 November 2026

A make.fun bounty entry: **"Sum up 13 November's world news in one image"**
(`news-image-01`, $250 prize, deadline Sunday 15 Nov 2026 03:00 WIB).

`main.py` is a self-contained Python program (standard library only) that
writes a single newspaper-style poster/infographic summarising the real
world news of **Friday, 13 November 2026** to `/output/entry.png`, the
path the make.fun grader reads. The poster image lives in this repo as
`world_news_13_nov_2026.png` and is read by `main.py` at run time; it
is drawn by `render_poster.py` (build-time, Pillow).

## Bounty requirements (verified from the make.fun API, 14 Nov 2026)

- The program writes one image to `/output/entry.png`.
- Gate: a whole PNG or JPEG of **at most 1 MiB and 1024 by 1024 pixels**.
  This poster: PNG **1024×1024 px, 129,203 bytes**.
- No network; the program runs twice and both runs must write the same
  bytes (this program writes fixed bytes — fully deterministic).
- Runtime: Python 3.13, `python3 -P -s` (stdlib only — no Pillow in the
  grader), 60 s wall budget, 1 CPU, 512 MiB RAM, repo mounted read-only.

## What it produces

One PNG poster, **1024 × 1024 px**: `world_news_13_nov_2026.png`
(a copy of what the program writes to `entry.png`)

- Masthead: "THE WORLD IN ONE IMAGE — Friday, 13 November 2026"
- Lead story: **Nvidia chief Jensen Huang resigns** after 33 years as CEO
- A "by the numbers" strip (Brent $95.82, IEA 105M b/d, 4+ hour FAA halt,
  130,000+ Microsoft outage reports, 33 years)
- Nine more story cards in a 3 × 3 grid, each with a category tag and a
  hand-drawn geometric icon
- A sources footer

## News summarised (all real events reported on 13 Nov 2026)

1. **Nvidia CEO Jensen Huang resigns** amid personal-relationship reports;
   CFO Colette Kress becomes interim CEO; Huang summoned to testify before
   Congress. *(DigiTimes Asia, BBC News, The Guardian)*
2. **Europe joins Ukraine peace talks** — US envoys Witkoff & Kushner briefed
   Zelensky near Dublin after meeting Putin; EU agreed a five-country team for
   the next round. *(Reuters, France 24, BBC News)*
3. **Microsoft 365 global outage** — Outlook, Teams and Copilot recovering
   after an outage that began 12 Nov; 130,000+ US reports. *(The Guardian)*
4. **FAA lifts nationwide ground stop** after a communications failure halted
   US departures for more than four hours. *(AP / Profile News)*
5. **Iran claims strike on a US radar in Bahrain**; tanker strikes escalate in
   the Strait of Hormuz. *(Middle East Eye, FeedCast)*
6. **China stages large unannounced Pacific drills** around Taiwan, Taiwanese
   security officials told Reuters. *(Reuters via The Raisina Post)*
7. **IEA forecasts a Q4 oil surplus** — supply 105M b/d vs demand, +1.7M b/d —
   while Brent rebounded to $95.82. *(IEA via The Raisina Post)*
8. **Qatar and Turkey sign a mutual defence agreement** in Istanbul. *(Qatar
   Amiri Diwan via Profile News)*
9. **Three Palestinians killed by Israeli tank fire** in central Gaza, Al-Aqsa
   Martyrs Hospital told AP; strikes also reported in south Lebanon. *(AP)*
10. **Measles elimination ruling looms** — PAHO commission reviewing whether
    measles has circulated for a year in the US and Mexico (5,100+ US cases,
    20,500+ in Mexico in 2026). *(AP via The Raisina Post)*

No story was invented: every item above was cross-checked against at least
two independent sources dated 13 November 2026 (see BUILD-TRANSCRIPT.md).

## How to run

```bash
python3 main.py                                    # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py        # local testing override
```

`main.py` needs only Python 3.8+ (standard library). If `/output` is not
writable, it falls back to `./output/entry.png`. The program self-checks
the gate (PNG format, ≤1 MiB, ≤1024×1024) on every run, with a stdlib
PNG parser (no Pillow).

To change the poster, edit `render_poster.py` and re-render:

```bash
pip install pillow        # only needed for rendering, not for the entry
python3 render_poster.py  # regenerates world_news_13_nov_2026.png
```

which overwrites `world_news_13_nov_2026.png` — `main.py` reads that
file at run time, so nothing else needs updating (see
BUILD-TRANSCRIPT.md §7).
The renderer asserts every card's text fits, so a layout overflow fails
loudly at build time instead of shipping a broken poster.

## Files

| File | Purpose |
| --- | --- |
| `main.py` | The program (entry point; stdlib only, reads the poster PNG) |
| `render_poster.py` | Build-time poster renderer (Pillow; not run by the grader) |
| `world_news_13_nov_2026.png` | Poster produced by `render_poster.py` (1024×1024) |
| `LICENSE` | MIT License (OSI-approved) |
| `README.md` | This file |
| `BUILD-TRANSCRIPT.md` | Build log, test results, and bundling notes, including the compliance verification of 14 Nov 2026 |

## License

MIT — see `LICENSE`. Copyright (c) 2026 Januar.
