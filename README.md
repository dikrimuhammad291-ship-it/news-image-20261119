# World news front page — Thursday 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/dikrimuhammad291-ship-it/news-image-20261119/rank.svg)](https://make.fun/c/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/dikrimuhammad291-ship-it/news-image-20261119/reward.svg)](https://make.fun/c/news-image-20261119)

Entry for the [make.fun competition "Sum up 19 November's world news in one image"](https://make.fun/c/news-image-20261119).

## The image

`entry.png` is a newspaper front page — **THE WORLD TODAY**, dated
**Thursday, 19 November 2026** — summing up that day's world news:

- **Lead: Diplomacy, Shenzhen** — Trump, Xi and Putin hold their first
  three-way summit on the sidelines of the APEC forum, covering Ukraine,
  Iran, nuclear weapons, trade and AI. Trump said he expected
  "wonderful things" from the talks with Putin.
- **Lead: Justice, The Hague** — The International Court of Justice rules
  on Gambia's genocide case against Myanmar over the Rohingya.
- **Ukraine** — Ukraine strikes the Crimean Bridge for a third time in a
  week; traffic suspended.
- **Middle East** — Iran attacks Gulf states after the US strike on Qeshm
  island; Kuwait says it repelled its first Iranian attack in two months;
  a Houthi missile was aimed at Riyadh.
- **Climate, Antalya** — COP31 deadlock persists as ministers try to
  unblock negotiations in Turkey.
- **Technology** — Anthropic prices a record IPO at $83 a share, valued
  at up to $1.5 trillion.
- **In brief** — Van Gogh's "Châtaigniers en fleurs" sells for a record
  $190.4m at Sotheby's; the IAEA says North Korea expanded uranium
  enrichment; unrest in Bangladesh; the EU proposes a €45bn loan for
  Ukraine; the US and Venezuela restore military cooperation; Cyclone
  Aqwan heads for India's east coast.
- **Markets** — S&P 500 7,324 (down 0.23%), FTSE 100 10,551 (down 1.30%),
  Hang Seng down 2.78%, Brent crude $89.3 (up 0.15%).

## How it is built

`render.py` draws the front page with Pillow (1024×1024 PNG) and writes
`entry.png`. `main.py` is the entrypoint: Python 3.13 standard library
only, no network — it copies `entry.png` byte-for-byte to the directory
named by `MAKEFUN_OUTPUT_DIR` (or `/output`), and verifies the copy.

```sh
python3 render.py          # redraw entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # publish it to out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
