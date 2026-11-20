"""Draw the 20 November 2026 front page (entry.png, 1024x1024).

Build-time renderer only — it runs here, on this machine, with Pillow.
The graded program is main.py, which ships the finished picture. All
stories below were first reported on Friday 20 November 2026: the
Trump-Xi-Putin meeting in China, the ICJ genocide ruling on Myanmar,
Cyclone Akvan, Voyager 1, Anthropic's market debut, the Wellington Test,
GTA VI sales and the Waleses in Delhi.

Run:  python3 tools/build_image.py
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

PAGE = 1024
MARGIN = 40
GUTTER = 24
BG = (248, 244, 234)
FG = (18, 18, 18)
RED = (150, 24, 24)
MUTED = (90, 86, 76)

FONTS = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}


def load(name, size):
    return ImageFont.truetype(FONTS[name], size)


def lines_for(draw, text, fnt, width):
    """Split text into lines that fit width, measured with the real font."""
    out = []
    for chunk in text.split("\n"):
        # Re-wrap by measuring, so long words still break cleanly at the
        # pixel width.
        words = chunk.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = word
        if cur:
            out.append(cur)
    return out


def para(draw, x, y, text, fnt, width, fill=FG, gap=None):
    """Draw a wrapped paragraph; return the y just below its last line."""
    step = int(fnt.size * 1.28) if gap is None else gap
    for line in lines_for(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def kicker_headline(draw, x, y, width, tag, head, body, head_px=23):
    draw.text((x, y), tag, font=load("sans_b", 13), fill=RED)
    y += 20
    y = para(draw, x, y, head, load("serif_b", head_px), width, gap=int(head_px * 1.14))
    y += 4
    y = para(draw, x, y, body, load("serif", 14), width)
    return y


LEAD_HEAD = "Trump, Xi and Putin Hold a First Three-Way Summit in China"
LEAD_BODY = (
    "The three presidents meet face to face in China to discuss nuclear arms "
    "control and global security, with Trump saying no peace was ever forged "
    "by declining opportunities, while APEC leaders gathered in Shenzhen "
    "debate trade, investment and new technology."
)
SECOND_HEAD = "World Court Finds Myanmar Guilty of Genocide Against the Rohingya"
SECOND_BODY = (
    "The International Court of Justice rules that Myanmar's military likely "
    "intended to destroy a substantial part of the Rohingya minority in its "
    "2017 crackdown — a landmark judgment under the genocide convention."
)

COLUMNS = [
    [
        ("WEATHER", "Cyclone Akvan Comes Ashore on India's East Coast",
         "Hundreds of thousands are evacuated in Odisha and Andhra Pradesh as "
         "the severe cyclone makes landfall, schools close and hundreds of "
         "rescue teams are deployed."),
        ("SCIENCE", "Voyager 1 Crosses One Light-Day From Earth",
         "NASA confirms its most distant probe has travelled a distance light "
         "itself needs a full day to cover, nearly fifty years after launch."),
        ("BUSINESS", "Anthropic Stock Leaps 17% on Its First Trading Day",
         "The AI firm's shares close sharply higher on debut, with reports "
         "valuing the company near $1.5 trillion as investors rush into "
         "artificial intelligence."),
    ],
    [
        ("SPORT", "Nicholls' Hundred Rescues New Zealand in Wellington",
         "Henry Nicholls makes 113 not out on day one of the first Test "
         "against India at the Basin Reserve, steadying the hosts after "
         "early wickets fell."),
        ("CULTURE", "GTA VI Overtakes The Odyssey's $1.8bn Box Office",
         "Grand Theft Auto VI's worldwide sales pass a Hollywood hit's entire "
         "cinema run, only days after the game's long-awaited launch."),
        ("ROYALTY", "Modi Welcomes the Prince and Princess of Wales",
         "India's prime minister receives the royal couple in New Delhi for "
         "talks on closer India-UK relations and strategic cooperation."),
    ],
]

FOOTER = (
    "ALSO TODAY:  Trump puts any decision on war with Iran off until 2027  ·  "
    "Japan's Hayabusa2 gives up its asteroid landing after engine trouble  ·  "
    "South Korea's highest court clears former PM Han Duck-soo  ·  Europe says "
    "it is ready to talk to Russia about ending the Ukraine war  ·  The US and "
    "Venezuela restore military cooperation  ·  World Children's Day"
)


def build():
    canvas = Image.new("RGB", (PAGE, PAGE), BG)
    d = ImageDraw.Draw(canvas)
    edge = PAGE - MARGIN

    # Masthead: thin rule, nameplate, dateline, heavy rule pair.
    d.line([(MARGIN, 28), (edge, 28)], fill=FG, width=2)
    name = "The World Today"
    nf = load("serif_b", 64)
    d.text(((PAGE - d.textlength(name, font=nf)) / 2, 38), name, font=nf, fill=FG)
    date = "FRIDAY 20 NOVEMBER 2026  ·  THE DAY IN ONE PAGE"
    df = load("sans_b", 16)
    d.text(((PAGE - d.textlength(date, font=df)) / 2, 118), date, font=df, fill=RED)
    d.line([(MARGIN, 148), (edge, 148)], fill=FG, width=4)
    d.line([(MARGIN, 156), (edge, 156)], fill=FG, width=1)

    # Lead story, full width.
    y = 172
    d.text((MARGIN, y), "DIPLOMACY  ·  APEC, SHENZHEN", font=load("sans_b", 14), fill=RED)
    y += 24
    y = para(d, MARGIN, y, LEAD_HEAD, load("serif_b", 42), edge - MARGIN, gap=46)
    y += 8
    y = para(d, MARGIN, y, LEAD_BODY, load("serif", 17), edge - MARGIN)
    y += 10
    d.line([(MARGIN, y), (edge, y)], fill=FG, width=1)
    y += 10

    # Second story, full width.
    y = para(d, MARGIN, y, SECOND_HEAD, load("serif_b", 27), edge - MARGIN, gap=31)
    y += 5
    y = para(d, MARGIN, y, SECOND_BODY, load("serif", 15), edge - MARGIN)
    y += 12
    d.line([(MARGIN, y), (edge, y)], fill=FG, width=2)
    y += 14

    # Two columns, each drawn from its story list.
    col_w = (edge - MARGIN - GUTTER) // 2
    bottom = y
    for i, stories in enumerate(COLUMNS):
        x = MARGIN + i * (col_w + GUTTER)
        cy = y
        for tag, head, body in stories:
            cy = kicker_headline(d, x, cy, col_w, tag, head, body)
            cy += 12
        bottom = max(bottom, cy)

    # Footer strip under the taller column.
    fy = bottom + 2
    d.line([(MARGIN, fy), (edge, fy)], fill=FG, width=2)
    para(d, MARGIN, fy + 10, FOOTER, load("sans", 12), edge - MARGIN, fill=MUTED)

    target = Path(__file__).resolve().parent.parent / "entry.png"
    canvas.save(target, optimize=True)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
