"""Rough watch face mockups for the Amazfit GTS 4 Mini (336x384 px, portrait).

Writes three SVGs next to this script. Shows 10:09:36, Thu 19 Nov.
Corner radius 80 is from Zepp's Device Basic Information table (unit not stated, read as px).
"""
import math
from pathlib import Path

W, H = 336, 384
CX, CY = W / 2, H / 2
CORNER = 80
TEAL = "#2ec4b6"
OUT = Path(__file__).parent

HOUR, MINUTE, SECOND = 10, 9, 36


def angles():
    s = SECOND * 6
    m = MINUTE * 6 + SECOND * 0.1
    h = (HOUR % 12) * 30 + MINUTE * 0.5
    return h, m, s


def edge_point(deg, inset):
    """Point on the rounded-rect screen edge (inset px inward) at a clock angle."""
    a = math.radians(deg)
    dx, dy = math.sin(a), -math.cos(a)
    hx, hy, r = W / 2 - inset, H / 2 - inset, max(CORNER - inset, 1)
    t = min(hx / abs(dx) if dx else 1e9, hy / abs(dy) if dy else 1e9)
    px, py = t * dx, t * dy
    if abs(px) > hx - r and abs(py) > hy - r:
        ox, oy = math.copysign(hx - r, px), math.copysign(hy - r, py)
        # ray/circle intersection: |t*d - o| = r
        b = dx * ox + dy * oy
        c = ox * ox + oy * oy - r * r
        t = b + math.sqrt(b * b - c)
        px, py = t * dx, t * dy
    return CX + px, CY + py


def ticks(inset, long_len, short_len, long_w, short_w, color="#ddd", short_color="#555", between=4):
    """Hour ticks plus `between` small ticks inside each hour."""
    out = []
    step = 30 / (between + 1)
    for k in range(12 * (between + 1)):
        i = k * step
        major = k % (between + 1) == 0
        ln = long_len if major else short_len
        x1, y1 = edge_point(i, inset)
        x2, y2 = edge_point(i, inset + ln)
        out.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color if major else short_color}" stroke-width="{long_w if major else short_w}" stroke-linecap="round"/>'
        )
    return "\n".join(out)


def hand(deg, length, width, color, tail=0, cap="round"):
    a = math.radians(deg)
    x2, y2 = CX + length * math.sin(a), CY - length * math.cos(a)
    x1, y1 = CX - tail * math.sin(a), CY + tail * math.cos(a)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="{cap}"/>')


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            f'<defs><clipPath id="screen"><rect width="{W}" height="{H}" rx="{CORNER}"/></clipPath>\n'
            # chrome: bright/dark bands across the screen; userSpaceOnUse so thin vertical lines still get it
            f'<linearGradient id="chrome" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">'
            '<stop offset="0" stop-color="#f4f6f8"/><stop offset="0.18" stop-color="#9aa1a9"/>'
            '<stop offset="0.36" stop-color="#ffffff"/><stop offset="0.52" stop-color="#7b838c"/>'
            '<stop offset="0.7" stop-color="#e3e7ea"/><stop offset="0.86" stop-color="#8d949c"/>'
            '<stop offset="1" stop-color="#f4f6f8"/></linearGradient>\n'
            # chrome text: sharp horizontal bands over the date line's width
            f'<linearGradient id="chromeText" gradientUnits="userSpaceOnUse" x1="{CX-100}" y1="0" x2="{CX+100}" y2="0">'
            '<stop offset="0" stop-color="#b9c0c7"/><stop offset="0.2" stop-color="#ffffff"/>'
            '<stop offset="0.32" stop-color="#6c747d"/><stop offset="0.5" stop-color="#f6f8fa"/>'
            '<stop offset="0.68" stop-color="#7f8790"/><stop offset="0.82" stop-color="#ffffff"/>'
            '<stop offset="1" stop-color="#aab1b8"/></linearGradient>\n'
            # chrome dome for the centre cap
            '<radialGradient id="chromeDome" cx="0.35" cy="0.3" r="0.8">'
            '<stop offset="0" stop-color="#ffffff"/><stop offset="0.35" stop-color="#c9ced3"/>'
            '<stop offset="0.6" stop-color="#6a727b"/><stop offset="0.85" stop-color="#d9dde1"/>'
            '<stop offset="1" stop-color="#8b939b"/></radialGradient></defs>\n'
            f'<rect width="{W}" height="{H}" fill="#111"/>\n'
            f'<g clip-path="url(#screen)"><rect width="{W}" height="{H}" fill="#000"/>\n{body}\n</g></svg>\n')


FONT = "font-family=\"Segoe UI, Roboto, sans-serif\""


def design_a():
    """Classic: minute ticks along the edge, slim hands, a small window below the centre."""
    h, m, s = angles()
    return svg(f"""
{ticks(8, 18, 7, 4, 2)}
<rect x="{CX-62}" y="{CY+52}" width="124" height="58" rx="12" fill="#0d1414" stroke="#244" stroke-width="1.5"/>
<text x="{CX}" y="{CY+82}" text-anchor="middle" {FONT} font-size="26" font-weight="600" fill="#eee">10:09</text>
<text x="{CX}" y="{CY+101}" text-anchor="middle" {FONT} font-size="13" letter-spacing="2" fill="{TEAL}">THU 19 NOV</text>
{hand(h, 78, 7, "#eee")}
{hand(m, 128, 5, "#eee")}
{hand(s, 140, 2, TEAL, tail=24)}
<circle cx="{CX}" cy="{CY}" r="6" fill="{TEAL}"/><circle cx="{CX}" cy="{CY}" r="2.5" fill="#000"/>
""")


def design_b():
    """Bauhaus: only 12/3/6/9 numerals and dots, broad hands, a window above the centre."""
    h, m, s = angles()
    nums = []
    for deg, n in ((0, "12"), (90, "3"), (180, "6"), (270, "9")):
        x, y = edge_point(deg, 30)
        nums.append(f'<text x="{x:.1f}" y="{y+10:.1f}" text-anchor="middle" {FONT} font-size="30" font-weight="700" fill="#eee">{n}</text>')
    dots = []
    for deg in range(0, 360, 30):
        if deg % 90:
            x, y = edge_point(deg, 22)
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#888"/>')
    return svg(f"""
{''.join(nums)}
{''.join(dots)}
<text x="{CX}" y="{CY-62}" text-anchor="middle" {FONT} font-size="30" font-weight="300" fill="#eee">10:09</text>
<text x="{CX}" y="{CY-40}" text-anchor="middle" {FONT} font-size="13" letter-spacing="2" fill="{TEAL}">THU · 19 NOV</text>
{hand(h, 72, 11, "#eee")}
{hand(m, 118, 8, "#eee")}
{hand(s, 130, 2.5, TEAL, tail=20)}
<circle cx="{CX}" cy="{CY}" r="8" fill="#eee"/><circle cx="{CX}" cy="{CY}" r="3" fill="{TEAL}"/>
""")


def design_c():
    """Inset frame: a teal hairline frame, 12 bars, a full-width digital strip under the centre."""
    h, m, s = angles()
    bars = []
    for deg in range(0, 360, 30):
        x1, y1 = edge_point(deg, 26)
        x2, y2 = edge_point(deg, 26 + (16 if deg % 90 == 0 else 9))
        bars.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#eee" stroke-width="{5 if deg % 90 == 0 else 3}" stroke-linecap="round"/>')
    return svg(f"""
<rect x="12" y="12" width="{W-24}" height="{H-24}" rx="{CORNER-12}" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0.7"/>
{''.join(bars)}
<line x1="70" y1="{CY+60}" x2="{W-70}" y2="{CY+60}" stroke="#333" stroke-width="1"/>
<text x="{CX-6}" y="{CY+96}" text-anchor="end" {FONT} font-size="28" font-weight="600" fill="#eee">10:09</text>
<text x="{CX+6}" y="{CY+82}" text-anchor="start" {FONT} font-size="12" letter-spacing="1.5" fill="{TEAL}">THU</text>
<text x="{CX+6}" y="{CY+97}" text-anchor="start" {FONT} font-size="12" letter-spacing="1.5" fill="#aaa">19 NOV</text>
{hand(h, 74, 6, "#eee", cap="butt")}
{hand(m, 124, 4, "#eee", cap="butt")}
{hand(s, 136, 1.5, TEAL, tail=22)}
<circle cx="{CX}" cy="{CY}" r="5" fill="#eee"/>
""")


def design_d():
    """The user's pick: A's ticks (3 between hours) and hands, B's digital time above the centre."""
    h, m, s = angles()
    return svg(f"""
{ticks(8, 18, 7, 4, 2, between=3)}
<text x="{CX}" y="{CY+92}" text-anchor="middle" {FONT} font-size="48" font-weight="300" fill="#eee">10:09</text>
<text x="{CX}" y="{CY+120}" text-anchor="middle" {FONT} font-size="18" letter-spacing="3" fill="url(#chromeText)">THU · 19 NOV</text>
{hand(h, 78, 7, "#eee")}
{hand(m, 128, 5, "#eee")}
{hand(s, 140, 3.5, "#7d858e", tail=24)}
{hand(s, 138, 1.2, "#ffffff", tail=22)}
<circle cx="{CX}" cy="{CY}" r="7.5" fill="url(#chromeDome)"/><circle cx="{CX}" cy="{CY}" r="2.5" fill="#000"/>
""")


if __name__ == "__main__":
    for name, fn in (("a-classic", design_a), ("b-bauhaus", design_b), ("c-frame", design_c), ("d-combined", design_d)):
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", name)
