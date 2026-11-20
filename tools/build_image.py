"""Render entry.png: a broadsheet front page for Friday 20 November 2026.

Local build tool only (uses Pillow); the graded program is main.py, which
copies the picture this script writes. Every story below was reported on
20 November 2026 (see the day's news wires): the historic Trump-Xi-Putin
trilateral summit in China, the world court's genocide ruling on Myanmar,
Cyclone Akvan's landfall in India, Voyager 1's light-day milestone,
Anthropic's first day of trading, the India-New Zealand Test, GTA VI's
sales record and the Prince and Princess of Wales in New Delhi.

Run:  python3 tools/build_image.py   (writes ../entry.png, 1024x1024)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (17, 17, 17)
ACCENT = (142, 22, 22)
GREY = (84, 80, 72)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, width, fill=INK, leading=1.25):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def story(draw, xy, width, kicker, headline, body, head_size=22):
    x, y = xy
    draw.text((x, y), kicker, font=font(SANS_B, 13), fill=ACCENT)
    y += 19
    y = text_block(draw, (x, y), headline, font(SERIF_B, head_size), width, leading=1.12)
    y += 3
    y = text_block(draw, (x, y), body, font(SERIF, 14), width, leading=1.26)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 44
    right = W - margin

    # Masthead
    d.line([(margin, 30), (right, 30)], fill=INK, width=2)
    title = "The World Today"
    tf = font(SERIF_B, 66)
    d.text(((W - d.textlength(title, font=tf)) / 2, 40), title, font=tf, fill=INK)
    dateline = "FRIDAY, 20 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS IN ONE PAGE"
    df = font(SANS_B, 16)
    d.text(((W - d.textlength(dateline, font=df)) / 2, 122), dateline, font=df, fill=ACCENT)
    d.line([(margin, 152), (right, 152)], fill=INK, width=4)
    d.line([(margin, 160), (right, 160)], fill=INK, width=1)

    # Lead story: the trilateral summit in China
    y = 176
    d.text((margin, y), "DIPLOMACY  ·  APEC SUMMIT, SHENZHEN", font=font(SANS_B, 14), fill=ACCENT)
    y += 24
    y = text_block(d, (margin, y), "Trump, Xi and Putin Meet in a Historic Three-Way Summit",
                   font(SERIF_B, 41), right - margin, leading=1.08)
    y += 6
    y = text_block(d, (margin, y),
                   "The three presidents sit down together for the first time, in China, to talk "
                   "about nuclear arms control and global security — Trump saying no peace was "
                   "ever forged by declining opportunities — as APEC leaders in Shenzhen debate "
                   "trade, investment and new technology.",
                   font(SERIF, 17), right - margin, leading=1.3)
    y += 10
    d.line([(margin, y), (right, y)], fill=INK, width=1)
    y += 10

    # Second lead: the world court's ruling on Myanmar
    y = text_block(d, (margin, y), "World Court Rules Myanmar Committed Genocide Against the Rohingya",
                   font(SERIF_B, 27), right - margin, leading=1.12)
    y += 4
    y = text_block(d, (margin, y),
                   "The International Court of Justice finds Myanmar's military likely intended "
                   "to destroy a substantial part of the Rohingya minority in its 2017 crackdown, "
                   "a landmark ruling under the genocide convention.",
                   font(SERIF, 15), right - margin, leading=1.28)
    y += 12
    d.line([(margin, y), (right, y)], fill=INK, width=2)
    y += 14

    # Two columns of the day's other news
    col_w = (right - margin - 28) // 2
    lx, rx = margin, margin + col_w + 28
    ly = story(d, (lx, y), col_w, "WEATHER",
               "Cyclone Akvan Makes Landfall on India's East Coast",
               "Hundreds of thousands are evacuated in Odisha and Andhra Pradesh as the severe "
               "cyclone comes ashore, with schools closed and hundreds of rescue teams deployed.",
               head_size=22)
    ly += 12
    ly = story(d, (lx, ly), col_w, "SCIENCE",
               "Voyager 1 Reaches One Light-Day From Home",
               "NASA confirms its farthest probe has crossed a distance light itself needs a full "
               "day to travel, nearly fifty years after launch.",
               head_size=22)
    ly += 12
    ly = story(d, (lx, ly), col_w, "BUSINESS",
               "Anthropic Shares Jump 17% on First Day of Trading",
               "The AI company's stock market debut closes sharply higher, with reports putting "
               "its value near $1.5 trillion as investors pile into artificial intelligence.",
               head_size=22)

    ry = story(d, (rx, y), col_w, "SPORT",
               "Nicholls' Unbeaten Century Steadies New Zealand",
               "Henry Nicholls scores 113 not out on the opening day of the first Test against "
               "India at the Basin Reserve in Wellington, reviving the hosts after early wickets.",
               head_size=22)
    ry += 12
    ry = story(d, (rx, ry), col_w, "CULTURE",
               "GTA VI Sales Pass The Odyssey's $1.8 Billion",
               "Grand Theft Auto VI's global sales overtake a Hollywood blockbuster's entire run, "
               "days after the game's long-awaited launch.",
               head_size=22)
    ry += 12
    ry = story(d, (rx, ry), col_w, "ROYALTY",
               "Modi Meets Prince and Princess of Wales in Delhi",
               "India's prime minister welcomes the royal couple to New Delhi to talk about "
               "strengthening India-UK relations and strategic cooperation.",
               head_size=22)

    # Footer strip (must stay inside the page: it starts wherever the taller
    # column ended, and the text is sized so its three lines end above y=1010)
    fy = max(ly, ry) + 12
    d.line([(margin, fy), (right, fy)], fill=INK, width=2)
    fy += 9
    text_block(d, (margin, fy),
               "ALSO TODAY:  Trump pushes any Iran war decision to 2027  ·  Japan's Hayabusa2 "
               "abandons its asteroid landing after engine trouble  ·  South Korea's top court "
               "clears former PM Han Duck-soo  ·  Europe ready for talks with Russia on ending "
               "the Ukraine war  ·  US and Venezuela restore military cooperation  ·  World "
               "Children's Day",
               font(SANS, 12), right - margin, fill=GREY, leading=1.3)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
