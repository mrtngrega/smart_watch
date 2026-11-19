"""Draw the image assets for the watch face (design E) into ../assets/gts4-mini/.

Everything is drawn 4x and scaled down for smooth edges. Fonts are the Segoe UI files that ship with Windows.
Run: python -I tools/make_assets.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "gts4-mini"
OUT.mkdir(parents=True, exist_ok=True)

W, H, CORNER = 336, 384, 80
CX, CY = W / 2, H / 2
S = 4  # supersampling
FONTS = Path("C:/Windows/Fonts")
LIGHT, REGULAR, SEMIBOLD = FONTS / "segoeuil.ttf", FONTS / "segoeui.ttf", FONTS / "seguisb.ttf"

DAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def save(img, name):
    img.save(OUT / name)


def down(img):
    return img.resize((img.width // S, img.height // S), Image.LANCZOS)


def edge_point(deg, inset):
    """Point on the rounded-rect screen edge, `inset` px inward, at a clock angle (0 = 12 o'clock)."""
    a = math.radians(deg)
    dx, dy = math.sin(a), -math.cos(a)
    hx, hy, r = W / 2 - inset, H / 2 - inset, max(CORNER - inset, 1)
    t = min(hx / abs(dx) if dx else 1e9, hy / abs(dy) if dy else 1e9)
    px, py = t * dx, t * dy
    if abs(px) > hx - r and abs(py) > hy - r:
        ox, oy = math.copysign(hx - r, px), math.copysign(hy - r, py)
        b = dx * ox + dy * oy
        c = ox * ox + oy * oy - r * r
        t = b + math.sqrt(b * b - c)
        px, py = t * dx, t * dy
    return CX + px, CY + py


def dial(with_glow):
    """Dial: ticks (3 small between hours) and the numbers 12/3/6/9. Black, or a faint centre glow."""
    img = Image.new("RGB", (W * S, H * S), (0, 0, 0))
    if with_glow:
        glow = Image.new("RGB", (W * S, H * S))
        px = glow.load()
        for y in range(0, H * S):
            for x in range(0, W * S):
                d = math.hypot((x / S - CX) / (W * 0.7), (y / S - CY) / (H * 0.7))
                v = max(0.0, 1 - d / 0.7)
                c = int(22 * v)
                px[x, y] = (c, c + 1, c + 2)
        img = glow
    d = ImageDraw.Draw(img)
    white = (255, 255, 255)
    for k in range(48):
        big = k % 4 == 0
        deg = k * 7.5
        x1, y1 = edge_point(deg, 8)
        x2, y2 = edge_point(deg, 8 + (18 if big else 7))
        width = (4 if big else 2) * S
        d.line([(x1 * S, y1 * S), (x2 * S, y2 * S)], fill=white, width=width)
        for x, y in ((x1, y1), (x2, y2)):  # round caps
            d.ellipse([x * S - width / 2, y * S - width / 2, x * S + width / 2, y * S + width / 2], fill=white)
    font = ImageFont.truetype(str(SEMIBOLD), 16 * S)
    for deg, n in ((0, "12"), (90, "3"), (180, "6"), (270, "9")):
        x, y = edge_point(deg, 40)
        d.text((x * S, y * S), n, font=font, fill=white, anchor="mm")
    return down(img)


def blade(width, length, glass, edge_alpha=190):
    """Pointed hand pointing up: tip at the top, widest at the base. Returns (image, pivot_x, pivot_y).
    Image width is odd (Zepp requires that for pointers); the pivot is the middle of the base."""
    w_img = width + 1 if width % 2 == 0 else width
    img = Image.new("RGBA", (w_img * S, length * S), (255, 255, 255, 0))
    left, right = (w_img - width) / 2 * S, (w_img + width) / 2 * S
    poly = [(w_img / 2 * S, 0), (right, length * S), (left, length * S)]
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    fill = Image.new("RGBA", img.size, (255, 255, 255, 0))
    fp = fill.load()
    for x in range(img.width):
        u = (x - left) / max(right - left, 1)
        u = min(max(u, 0), 1)
        # glass: bright at both edges, clear in the middle (alpha 0..255)
        a = 0.38 - 0.28 * min(u, 1 - u) * 2 if glass else 1.0
        a = max(a, 0.08) if glass else 1.0
        for y in range(img.height):
            fp[x, y] = (255, 255, 255, int(255 * a))
    img.paste(fill, (0, 0), mask)
    if glass:
        ImageDraw.Draw(img).polygon(poly, outline=(255, 255, 255, edge_alpha), width=max(S * 3 // 4, 1))
    return down(img), w_img // 2, length - 1


def second_hand():
    """Thin steel needle with a white core and a short tail; pivot 142 px from the top."""
    length, tail = 142, 26
    img = Image.new("RGBA", (5 * S, (length + tail) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = 2.5 * S
    d.polygon([(cx, 0), (cx + 1.5 * S, length * S), (cx + 1.0 * S, (length + tail) * S),
               (cx - 1.0 * S, (length + tail) * S), (cx - 1.5 * S, length * S)], fill=(125, 133, 142, 255))
    d.line([(cx, 3 * S), (cx, (length + tail - 2) * S)], fill=(255, 255, 255, 255), width=int(1.2 * S))
    return down(img), 2, length


def cap():
    """Glass dome for the centre, 16x16."""
    size = 16 * S
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    for y in range(size):
        for x in range(size):
            dx, dy = (x + 0.5 - size / 2) / (size / 2), (y + 0.5 - size / 2) / (size / 2)
            r = math.hypot(dx, dy)
            if r <= 1:
                hl = max(0.0, 1 - math.hypot(dx + 0.35, dy + 0.4) / 0.9)  # highlight, upper left
                a = 0.16 + 0.55 * hl + (0.45 if r > 0.9 else 0)  # clear body, bright rim
                px[x, y] = (255, 255, 255, int(255 * min(a, 1)))
    return down(img)


def text_cells(items, font_path, size, cell_w=None, pad=0, spacing=0):
    """One transparent PNG per string, white text. cell_w gives every image the same width (tabular digits)."""
    font = ImageFont.truetype(str(font_path), size * S)
    asc, desc = font.getmetrics()
    height = (asc + desc) // S + 2 * pad
    out = {}
    for name, s in items:
        # width with letter spacing
        adv = [font.getlength(ch) / S for ch in s]
        total = sum(adv) + spacing * (len(s) - 1)
        w = cell_w or int(math.ceil(total)) + 2 * pad
        img = Image.new("RGBA", (w * S, height * S), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        x = (w - total) / 2 if cell_w else pad
        for ch, a in zip(s, adv):
            d.text((x * S, pad * S), ch, font=font, fill=(255, 255, 255, 255))
            x += a + spacing
        out[name] = down(img)
    return out


if __name__ == "__main__":
    save(dial(True), "dial.png")
    save(dial(False), "dial_aod.png")

    img, px_, py_ = blade(16, 82, True)
    save(img, "hour.png"); print("hour", img.size, "pivot", px_, py_)
    img, px_, py_ = blade(12, 134, True)
    save(img, "minute.png"); print("minute", img.size, "pivot", px_, py_)
    img, px_, py_ = blade(16, 82, False)
    save(img, "hour_aod.png")
    img, px_, py_ = blade(12, 134, False)
    save(img, "minute_aod.png")
    img, px_, py_ = second_hand()
    save(img, "second.png"); print("second", img.size, "pivot", px_, py_)
    save(cap(), "cap.png")

    # Time digits 0-9 and ":" (Segoe UI Light 48 px, same width for every digit).
    cells = text_cells([(str(i), str(i)) for i in range(10)], LIGHT, 48, cell_w=27)
    cells.update(text_cells([("colon", ":")], LIGHT, 48, cell_w=14))
    for name, im in cells.items():
        save(im, f"time_{name}.png")
    print("time digit", cells["0"].size)

    # Date: day digits, weekday and month words, and the dot (Segoe UI 18 px, letter spacing 3).
    # Every image of a kind has the same width so the whole date stays centred whatever the day.
    # Weekdays are written Monday first (Zepp's week order, to be confirmed in the simulator).
    font18 = ImageFont.truetype(str(REGULAR), 18)

    def widest(words):
        return int(max(sum(font18.getlength(c) for c in w) + 3 * (len(w) - 1) for w in words)) + 2

    wk_w, mon_w = widest(DAYS), widest(MONTHS)
    monday_first = DAYS[1:] + DAYS[:1]
    parts = {}
    parts.update(text_cells([(f"day_{i}", str(i)) for i in range(10)], REGULAR, 18, cell_w=12, spacing=0))
    parts.update(text_cells([(f"wk_{i}", w) for i, w in enumerate(monday_first)], REGULAR, 18, cell_w=wk_w, spacing=3))
    parts.update(text_cells([(f"mon_{i}", m) for i, m in enumerate(MONTHS)], REGULAR, 18, cell_w=mon_w, spacing=3))
    parts.update(text_cells([("dot", "·")], REGULAR, 18, cell_w=14))
    for name, im in parts.items():
        save(im, f"date_{name}.png")
    h = parts["dot"].height
    print(f"date cells: weekday {wk_w}, month {mon_w}, day digit 12, dot 14, height {h}; total {wk_w + 14 + 24 + 14 + mon_w}")
    # Preview / icon: the face at 10:09:36 (Zepp's default preview time), scaled to 228x260.
    face = Image.open(OUT / "dial.png").convert("RGBA")

    def paste_hand(name, deg, pivot):
        hand = Image.open(OUT / name).convert("RGBA")
        canvas = Image.new("RGBA", face.size, (0, 0, 0, 0))
        canvas.paste(hand, (int(CX - pivot[0]), int(CY - pivot[1])))
        face.alpha_composite(canvas.rotate(-deg, resample=Image.BICUBIC, center=(CX, CY)))

    x = int(CX - 61)
    for name in ("time_1", "time_0", "time_colon", "time_0", "time_9"):
        im = Image.open(OUT / f"{name}.png"); face.alpha_composite(im, (x, 232)); x += im.width
    for name, dx in (("date_wk_3", 0), ("date_dot", 53), ("date_day_1", 69), ("date_day_9", 81), ("date_mon_10", 100)):
        face.alpha_composite(Image.open(OUT / f"{name}.png"), (int(CX - 73 + dx), 293))
    paste_hand("hour.png", 304.5, (8, 81))
    paste_hand("minute.png", 54.6, (6, 133))
    paste_hand("second.png", 216, (2, 142))
    face.alpha_composite(Image.open(OUT / "cap.png"), (int(CX - 8), int(CY - 8)))
    face.convert("RGB").save(OUT / "preview_full.png")
    face.convert("RGB").resize((228, 260), Image.LANCZOS).save(OUT / "icon.png")
    print("wrote", len(list(OUT.glob("*.png"))), "files to", OUT)
