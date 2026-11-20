# news-image-20261120-entry

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/e0426685-cloud/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/e0426685-cloud/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A deterministic Python entry for make.fun's "Sum up 20 November's world news in one image" bounty. `main.py` writes a broadsheet front page for Friday 20 November 2026 — the historic Trump–Xi–Putin trilateral summit in China, the world court's genocide ruling on Myanmar, Cyclone Akvan's landfall, Voyager 1's light-day milestone, Anthropic's first day of trading, the India–New Zealand Test, GTA VI's sales record and the Prince and Princess of Wales in New Delhi — as a single PNG image. The picture itself is rendered by `tools/build_image.py` and committed as `entry.png`; `main.py` validates it and copies it to the output directory, byte for byte, so both grading runs produce identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py && ls -l out/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=52532a96&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
