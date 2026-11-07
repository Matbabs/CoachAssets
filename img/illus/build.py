"""Builds the content illustrations (SVG) in the app's look: purple figures, yellow effort cues, Inter.

Run: python3 img/illus/build.py  (from the online assets root). Output: img/illus/*.svg
The app draws them with react-native-svg (components/HtmlSvg.tsx): stick to basic shapes,
no <marker>, no CSS; text is font-family="Inter, sans-serif" + font-weight 400/600/700 only.
"""

import os

OUT = os.path.dirname(os.path.abspath(__file__))

# App palette (styles.tsx)
P, P2, PF = "#6D28D9", "#B9A2EE", "#F4EEFC"  # secondary, far limbs, secondary flat on white
Y, O, D, W = "#FBBF24", "#F97316", "#1A0F2B", "#FFFFFF"
BOLD, SEMI, REG = 700, 600, 400  # Inter weights; the app maps them to its loaded Inter_* faces

W_CARD = 340


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=11, font=SEMI, fill=D, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="Inter, sans-serif" font-weight="{font}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'


def card(h, body, w=W_CARD):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f'<rect width="{w}" height="{h}" rx="15" fill="{PF}"/>{body}</svg>'
    )


def line(pts, color=P, w=8):
    d = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def head(x, y, r=8, color=P):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def arrow(x1, y1, x2, y2, color=Y, w=3.5):
    import math

    a = math.atan2(y2 - y1, x2 - x1)
    L = 7
    p1 = (x2 - L * math.cos(a - 0.5), y2 - L * math.sin(a - 0.5))
    p2 = (x2 - L * math.cos(a + 0.5), y2 - L * math.sin(a + 0.5))
    bx, by = x2 - 0.6 * L * math.cos(a), y2 - 0.6 * L * math.sin(a)
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
        f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>'
    )


def pill(cx, cy, s, fill=Y, color=D, size=10):
    w = len(s) * size * 0.62 + 12
    return (
        f'<rect x="{cx - w / 2:.1f}" y="{cy - 9}" width="{w:.1f}" height="18" rx="9" fill="{fill}"/>'
        + text(cx, cy + 3.5, s, size, BOLD, color)
    )


def bar(x1, x2, y):
    return f'<rect x="{x1}" y="{y - 3}" width="{x2 - x1}" height="6" rx="3" fill="{D}"/>'


def ground(x1, x2, y):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{P2}" stroke-width="2" stroke-linecap="round"/>'


def panels(steps, h=190, title=None):
    """steps: list of (caption lines, svg drawn in a 100x130 box)."""
    n = len(steps)
    top = 30 if title else 0
    pw = (W_CARD - 20) / n
    body = text(16, 22, title, 13, BOLD, D, "start") if title else ""
    for i, (cap, art) in enumerate(steps):
        x = 10 + i * pw
        ox = x + (pw - 100) / 2
        body += f'<g transform="translate({ox:.1f},{top + 8})">{art}</g>'
        if n > 1:
            body += f'<circle cx="{x + 14:.1f}" cy="{top + 16}" r="9" fill="{Y}"/>' + text(
                x + 14, top + 20, str(i + 1), 11, BOLD, D
            )
        lines = cap if isinstance(cap, list) else [cap]
        for k, l in enumerate(lines):
            body += text(x + pw / 2, top + 150 + k * 14, l, 11, SEMI, D)
        if i:
            body += f'<line x1="{x:.1f}" y1="{top + 14}" x2="{x:.1f}" y2="{top + 172}" stroke="{P2}" stroke-width="1" stroke-dasharray="3 4"/>'
    return card(h + top, body)


# ---------- poses (100x130 box) ----------


def hang_front(level=0.0, dx=0, gap=0):
    """Two-arm hang seen from the front. level 0 = arms straight, 1 = chin over the bar.
    gap lifts the bar off the hands (hands let go)."""
    by = 16
    cx = 50 + dx
    sy = by + 42 - 34 * level  # shoulders rise
    bend = min(1.0, level * 1.4)
    s = bar(14 + dx, 86 + dx, by - gap)
    for sgn in (-1, 1):
        hand, sh = (cx + sgn * 20, by), (cx + sgn * 11, sy)
        mid = ((hand[0] + sh[0]) / 2, (hand[1] + sh[1]) / 2)
        bent = (cx + sgn * 25, sy + 8)
        el = (mid[0] + (bent[0] - mid[0]) * bend, mid[1] + (bent[1] - mid[1]) * bend)
        s += line([hand, el, sh])
    s += line([(cx - 11, sy), (cx + 11, sy)], P, 8)
    s += line([(cx, sy), (cx, sy + 34)], P, 12)
    s += line([(cx - 5, sy + 34), (cx - 7, sy + 52), (cx - 6, sy + 68)])
    s += line([(cx + 5, sy + 34), (cx + 7, sy + 52), (cx + 6, sy + 68)])
    s += head(cx, sy - 13, 9)
    return s


def hang_one_arm(level=0.0, band=False):
    """One-arm hang/pull, side-ish view."""
    by = 14
    hand = (50, by)
    sy = by + 36 - 28 * level
    s = bar(30, 70, by)
    if level < 0.3:
        s += line([hand, (52, sy - 2), (54, sy)])
    else:
        s += line([hand, (38, (by + sy) / 2 + 6), (52, sy)])
    s += line([(54, sy), (56, sy + 40)], P, 12)
    s += line([(54, sy + 6), (68, sy + 22), (72, sy + 36)], P2)  # free arm
    if band:
        s += line([(72, sy + 36), (60, by + 2)], Y, 3)
    s += line([(56, sy + 40), (60, sy + 62), (58, sy + 82)])
    s += line([(56, sy + 40), (52, sy + 62), (54, sy + 82)], P2)
    s += head(48, sy - 10, 9)
    return s


def squat_side(depth=0.0, one_leg=False, jump=0):
    """Side view, facing right. depth 0 = standing, 1 = below 90 deg."""
    gy = 124 - jump
    knee_fwd = 6 + 20 * depth
    hip = (44 - 14 * depth, gy - 60 + 30 * depth)
    knee = (hip[0] + knee_fwd + 14 * depth, gy - 32 + 4 * depth)
    foot = (knee[0] - 6 - 6 * depth, gy - 2)
    sh = (hip[0] + 6 + 18 * depth, hip[1] - 40 + 4 * depth)
    s = ground(10, 90, 126) if jump else ground(10, 90, 126)
    if one_leg:
        s += line([hip, (hip[0] - 4, knee[1] - 4), (hip[0] - 16, knee[1] + 6)], P2)
    else:
        s += line([hip, (knee[0] - 4, knee[1]), (foot[0] - 4, foot[1])], P2)
    s += line([hip, sh], P, 12)
    s += line([hip, knee, foot])
    s += line([foot, (foot[0] + 10, foot[1])], P, 6)
    s += line([(sh[0], sh[1] + 4), (sh[0] + 16, sh[1] + 14), (sh[0] + 30, sh[1] + 12)])
    s += head(sh[0] + 6, sh[1] - 12, 9)
    return s


def plank(kind="classic"):
    """Side view plank on the forearms, head right. kinds: classic, one_leg, superman."""
    gy = 118
    sh, hip, ft = (78, gy - 26), (42, gy - 20), (6, gy - 4)
    s = ground(0, 100, gy + 4)
    if kind == "superman":
        s += line([sh, (96, sh[1] - 6)], P2)  # far arm reaching forward
    else:
        s += line([sh, (sh[0] - 2, gy), (sh[0] + 16, gy)], P2)
    if kind in ("one_leg", "superman"):
        s += line([hip, (8, gy - 40)], P2)  # lifted leg
        s += line([hip, ft])
    else:
        s += line([hip, ft], P2)
        s += line([hip, (ft[0] + 2, ft[1])])
    s += line([sh, hip], P, 12)
    s += line([sh, (sh[0], gy), (sh[0] + 18, gy)])
    s += head(sh[0] + 12, sh[1] - 6, 8)
    return s


def superman(kind="basic"):
    gy = 116
    s = ground(0, 100, gy + 4)
    s += line([(38, gy - 4), (66, gy - 6)], P, 12)
    s += line([(66, gy - 8), (96, gy - 20)])
    s += line([(38, gy - 4), (6, gy - 16)])
    s += head(74, gy - 18, 8)
    if kind == "loaded":
        s += f'<rect x="91" y="{gy - 30}" width="10" height="16" rx="3" fill="{D}"/>'
    s += arrow(20, gy - 22, 18, gy - 36) + arrow(86, gy - 28, 88, gy - 42)
    return s


def side_plank(kind="basic"):
    """Front-facing side plank, head right."""
    gy = 118
    sh, hip, ft = (74, gy - 30), (42, gy - 18 - (10 if kind != "basic" else 0)), (8, gy - 2)
    s = ground(0, 100, gy + 4)
    s += line([sh, (sh[0] - 2, gy), (sh[0] + 14, gy)])
    s += line([sh, hip], P, 12)
    s += line([hip, ft])
    if kind == "top":
        s += line([hip, (10, ft[1] - 26)], P2)
        s += line([sh, (sh[0] + 4, sh[1] - 34)], P2)
    else:
        s += line([(sh[0] - 4, sh[1] + 2), (hip[0] + 6, hip[1] - 2)], P2, 6)
    if kind != "basic":
        s += arrow(42, gy - 2, 42, gy - 16) if kind == "dynamic" else ""
    s += head(sh[0] + 10, sh[1] - 10, 8)
    return s


# ---------- illustrations ----------

ILLUS = {}


def illus(name):
    def deco(fn):
        ILLUS[name] = fn
        return fn

    return deco


@illus("traction-complete")
def _():
    return panels(
        [
            (["Bras fléchis", "à 120°"], hang_front(0.3) + pill(82, 40, "120°")),
            (["Omoplates basses", "et en arrière"], hang_front(0.3) + arrow(8, 36, 8, 56) + arrow(92, 36, 92, 56)),
            (["Menton au-dessus", "de la barre"], hang_front(1) + arrow(90, 100, 90, 60)),
        ]
    )


@illus("traction-isometrique")
def _():
    return panels(
        [
            (["Monte en haut", "(banc si besoin)"], hang_front(0.6) + arrow(90, 100, 90, 60)),
            (["Tiens le menton", "au-dessus de la barre"], hang_front(1) + pill(84, 50, "10 s")),
        ]
    )


@illus("traction-excentrique")
def _():
    return panels(
        [
            (["Pars en haut", "(banc si besoin)"], hang_front(1)),
            (["Descends", "lentement"], hang_front(0.5) + arrow(92, 40, 92, 96) + pill(50, 124, "lentement")),
            (["Bras tendus", "en bas"], hang_front(0)),
        ]
    )


@illus("statodynamique-bras")
def _():
    return panels(
        [
            (["Pause 1-2 s", "entre 120° et 90°"], hang_front(0.5) + pill(84, 46, "1-2 s")),
            (["BOUM ! menton", "au-dessus"], hang_front(1) + arrow(90, 100, 90, 56, O)),
            (["Relâche direct", "et enchaîne"], hang_front(0) + arrow(90, 56, 90, 96)),
        ]
    )


@illus("statodynamique-jambes")
def _():
    return panels(
        [
            (["Descends sous 90°", "à 2 jambes"], squat_side(1)),
            (["1 jambe : remonte", "un peu, pause 1-2 s"], squat_side(0.75, True) + pill(76, 30, "1-2 s")),
            (["BOUM ! explose,", "réception 2 pieds"], squat_side(0, True, 10) + arrow(88, 100, 88, 60, O)),
        ]
    )


@illus("concentrique-bras")
def _():
    return panels(
        [
            (["1 bras à 120°", "(élastique pour aider)"], hang_one_arm(0.25, True)),
            (["Tire jusqu'en haut", "1 à 3 max par bras"], hang_one_arm(1) + arrow(88, 100, 88, 60, O)),
        ]
    )


@illus("traction-un-deux-bras")
def _():
    return panels(
        [
            (["2 à 3 tractions", "à un bras"], hang_one_arm(1)),
            (["Sans pause : 3", "explosives à 2 bras"], hang_front(1) + arrow(90, 100, 90, 56, O)),
        ]
    )


def hold(x, y, size):
    return f'<rect x="{x - size / 2}" y="{y}" width="{size}" height="{max(4, size / 3)}" rx="3" fill="{D}"/>'


@illus("isometrique-doigts")
def _():
    hang = hold(50, 10, 16)
    hang += line([(50, 14), (52, 48)]) + line([(52, 48), (54, 90)], P, 12)
    hang += line([(53, 54), (66, 72), (70, 88)], P2)
    hang += line([(54, 90), (57, 110), (55, 128)]) + line([(54, 90), (50, 110), (52, 128)], P2)
    hang += head(42, 34, 9) + pill(82, 50, "5-10 s")
    sizes = hold(14, 60, 26) + hold(50, 62, 16) + hold(88, 64, 8)
    sizes += text(14, 88, "bac", 10, SEMI, P) + text(50, 88, "petite", 10, SEMI, P) + text(90, 88, "fuyante", 10, SEMI, P)
    sizes += arrow(10, 104, 92, 104, O) + text(50, 122, "plus dur", 10, BOLD, O)
    return panels(
        [
            (["Bras tendu, épaule", "active, jamais arqué"], hang),
            (["Tu tiens plus de 5 s ?", "Réduis la prise"], sizes),
        ]
    )


@illus("pliometrie-basse")
def _():
    return panels(
        [
            (["Traction", "jusqu'en haut"], hang_front(1)),
            (["Lâche légèrement", "la prise"], hang_front(0.9, gap=-10) + arrow(6, 40, 6, 14, O) + arrow(94, 40, 94, 14, O)),
            (["Rattrape et", "rebondis direct"], hang_front(0.6) + arrow(94, 50, 94, 90)),
        ]
    )


@illus("gainage-global")
def _():
    def lever(knee=False):
        s = bar(22, 46, 14)
        s += line([(34, 14), (40, 52)])
        s += line([(40, 52), (72, 54)], P, 12)
        if knee:
            s += line([(72, 54), (62, 70), (82, 78)])
        else:
            s += line([(72, 54), (100, 56)])
        s += head(30, 58, 9)
        return s

    return panels(
        [
            (["Corps à l'horizontale", "bras tendus, 2-5 s"], lever() + pill(66, 100, "2-5 s")),
            (["Variante : genou", "plié pour alléger"], lever(True)),
        ]
    )


@illus("gainage-anterieur")
def _():
    return panels(
        [
            (["Niv. 1", "Classique"], plank("classic")),
            (["Niv. 2", "Une jambe"], plank("one_leg")),
            (["Niv. 3", "Superman"], plank("superman")),
        ]
    )


@illus("gainage-posterieur")
def _():
    return panels(
        [
            (["Niv. 1", "Superman basique"], superman()),
            (["Niv. 2", "Superman chargé"], superman("loaded")),
        ]
    )


@illus("gainage-lateral")
def _():
    return panels(
        [
            (["Niv. 1", "Basique"], side_plank()),
            (["Niv. 2", "Hanches en piston"], side_plank("dynamic")),
            (["Niv. 3", "Bras + jambe levés"], side_plank("top")),
        ]
    )


# ---------- effort profiles ----------

ZONE_COLORS = {1: "#DDD6FE", 2: "#A78BFA", 3: P, 4: Y, 5: O}


def zone_color(z):
    return ZONE_COLORS[min(5, max(1, int(z)))]  # 3.6 = high Z3 stays Z3


def fmt(m):
    if m >= 60:
        h, r = divmod(round(m), 60)
        return f"{h}h{r:02d}" if r else f"{h}h"
    return f"{m:g}′" if m >= 1 else f"{round(m * 60)}″"


def rep(n, *segs, between=None):
    out = []
    for i in range(n):
        out += list(segs)
        if between and i < n - 1:
            out.append(between)
    return out


def profile(groups, total=None, title="Profil de la séance"):
    """groups: [(label, [(minutes, zone), ...])]. zone 1-5, up to 5.5 for all-out.
    total: session length in minutes; the rest is drawn as easy riding (Z1-Z2)."""
    groups = [(l, list(sg)) for l, sg in groups]
    done = sum(m for _, sg in groups for m, _ in sg)
    if total and total - done >= 5:
        groups.append(("Fin Z1-Z2", [(total - done, 1.5)]))
    x0, x1, base, unit, minw = 40, 324, 128, 17, 2.4
    segs = [(m, z) for _, sg in groups for m, z in sg]
    k = (x1 - x0) / sum(m for m, _ in segs)
    for _ in range(20):  # keep short reps visible, squeeze the long blocks
        widths = [max(minw, m * k) for m, _ in segs]
        long_ = sum(m for (m, _), w in zip(segs, widths) if w > minw)
        short = sum(w for w in widths if w <= minw)
        k = (x1 - x0 - short) / long_
    body = text(16, 24, title, 13, BOLD, D, "start")
    body += text(x1, 24, "≈ " + fmt(round(total or done)), 11, SEMI, P, "end")
    for z in range(1, 6):
        y = base - z * unit
        body += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{P2}" stroke-width="1" stroke-dasharray="2 4"/>'
        body += text(x0 - 10, y + 4, f"Z{z}", 10, SEMI, P, "end")
    x, last = x0, 0
    for label, sg in groups:
        gx = x
        for m, z in sg:
            w = max(minw, m * k)
            h = z * unit
            body += f'<rect x="{x:.2f}" y="{base - h:.1f}" width="{w + 0.3:.2f}" height="{h:.1f}" rx="1.5" fill="{zone_color(z)}"/>'
            x += w
        body += f'<line x1="{gx + 1:.1f}" y1="{base + 7}" x2="{x - 1:.1f}" y2="{base + 7}" stroke="{P2}" stroke-width="2" stroke-linecap="round"/>'
        half = len(label) * 2.9
        cx = min(max((gx + x) / 2, 12 + half), W_CARD - 12 - half)
        if cx - half > last + 6:  # skip a label that would collide with the previous one
            body += text(cx, base + 22, label, 10, SEMI, D)
            last = cx + half
    body += f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{D}" stroke-width="1.5"/>'
    return card(base + 34, body)


def prof(name, groups, total=None, title="Profil de la séance"):
    ILLUS[name] = lambda: profile(groups, total, title)


W20, W15, W25 = ("Échauf. 20′", [(20, 2)]), ("Échauf. 15′", [(15, 2)]), ("Échauf. 25′", [(25, 2)])
C10, C15 = ("Calme 10′", [(10, 1)]), ("Calme 15′", [(15, 1)])
TEST = "Profil du test"

# Tests
prof("test-6min", [("Échauf. 20′", [(20, 1.5)]), ("6′ à fond", [(6, 5.5)]), C15], title=TEST)
prof("test-3min", [("Échauf. 20′", [(20, 1.5)]), ("3′ à fond", [(3, 5.5)]), C15], title=TEST)
prof("test-12min-montee", [W20, ("12′ max", [(12, 5)]), ("Transition", [(3, 1)])], title=TEST)

# Trail
prof("trail-c1.s2.d1", [("Z2", [(20, 2)]), ("5 × 100 m en côte", rep(5, (0.5, 4.5), (1.5, 1))), ("Z2", [(20, 2)])])
prof("trail-c1.s3.d2", [W20, ("4 × (3′ seuil / 2′ trot)", rep(4, (3, 4), (2, 1)))])
prof("trail-c2.s1.d2", [W20, ("10 × 30″ en côte", rep(10, (0.5, 5), (1.5, 1)))])
prof("trail-c2.s2.d2", [W20, ("3 × 8′ seuil en côte", rep(3, (8, 4), (3, 1)))])
prof("trail-c2.s3.d2", [W20, ("2 × 15′ tempo / 5′ Z2", rep(2, (15, 3), (5, 2)))])
prof("trail-c3.s1.d2", [W20, ("10 × 400 m / 1′ trot", rep(10, (1.5, 4.6), (1, 1)))])
prof("trail-c3.s2.d2", [W20, ("2 × 15′ progressives", rep(2, (5, 3), (5, 3.5), (5, 4), (5, 2)))])
prof("trail-c3.s3.d2", [W20, ("12 × (30″ côte / 30″ plat)", rep(12, (0.5, 5), (0.5, 4), (1, 1)))])
prof("trail-c4.s1.d2", [W20, ("2 × 10 × 30/30", rep(10, (0.5, 5), (0.5, 1)) + [(3, 1)] + rep(10, (0.5, 5), (0.5, 1)))])
prof("trail-c4.s2.d2", [W20, ("5 × 3′ / 1′30 trot", rep(5, (3, 4.5), (1.5, 1)))])
prof("trail-c4.s3.d2", [W20, ("3 × 10′ seuil en côte", rep(3, (10, 4), (4, 1)))])
prof("trail-c5.s1.d2", [W20, ("10 × 300 m / 1′ trot", rep(10, (1, 5), (1, 1)))])
prof("trail-c5.s2.d2", [W20, ("2 × 10′ seuil en côte", rep(2, (10, 4), (4, 1)))])
prof("trail-c5.s3.d2", [W20, ("6 × 30″ côte / 2′ marche", rep(6, (0.5, 5.5), (2, 1)))])
prof("trail-c5.s4.d2", [W15, ("3 × 1′ Z3 / 1′ Z1", rep(3, (1, 3), (1, 1)))])

# Ski de rando
prof("ski-c1.s3.d2", [W20, ("3 × 8′ Z4 / 4′", rep(3, (8, 4), (4, 1))), C15])
prof("ski-c1.s3.d3", [("Z2", [(30, 2)]), ("15′ Z3", [(15, 3)]), ("Z2", [(30, 2)]), ("15′ Z3", [(15, 3)]), ("Z2", [(30, 2)])])
prof("ski-c1.s4.d1", [W20, ("4 × 10′ Z3 / 3′", rep(4, (10, 3), (3, 2))), C10])
prof("ski-c1.s4.d2", [W25, ("8 × 1′ Z5 / 2′", rep(8, (1, 5), (2, 1))), C15])
prof("ski-c1.s4.d3", [("Z2", [(25, 2)]), ("2 × 12′ Z3", [(12, 3), (10, 2), (12, 3)]), ("Z2", [(15, 2)]), ("5 × 30″", rep(5, (0.5, 5), (1.5, 2))), ("Z2", [(21, 2)])])
prof("ski-c2.s2.d2", [W20, ("3 × 12′ Z3 / 4′", rep(3, (12, 3), (4, 2))), C10])
prof("ski-c2.s3.d1", [W20, ("4 × 10′ pente raide", rep(4, (10, 3), (3, 1))), C10])
prof("ski-c2.s4.d2", [("Z2", [(30, 2)]), ("6 × 20″ Z4", rep(6, (0.33, 4), (2, 2))), ("Z2", [(16, 2)])])
prof("ski-c3.s1.d1", [W20, ("3 × 15′ au SV1", rep(3, (15, 2.6), (5, 1))), C10])
prof("ski-c3.s1.d3", [W20, ("3 × 12′ sweet spot", rep(3, (12, 3.6), (4, 1))), C10])
prof("ski-c3.s2.d1", [W20, ("4 × 8′ seuil / 4′", rep(4, (8, 4), (4, 1)))])
prof("ski-c3.s2.d3", [W20, ("5 × 5′ à 105 % / 5′", rep(5, (5, 5), (5, 1))), C10])
prof("ski-c3.s3.d1", [W20, ("3 × 9′ over-under", rep(3, *rep(3, (2, 4), (1, 5)), (5, 1))), C10])
prof("ski-c3.s3.d3", [W20, ("2 × 20′ sweet spot", rep(2, (20, 3.6), (6, 1))), C10])
prof("ski-c3.s4.d1", [W15, ("2 × 12′ SV1", rep(2, (12, 2.6), (4, 1))), C10])
prof("ski-c3.s4.d3", [W20, ("3 × 4′ VAMc / 4′", rep(3, (4, 4), (4, 1))), C15])
prof("ski-c4.s1.d1", [W20, ("2 × 10 × 30/30", rep(10, (0.5, 5), (0.5, 1)) + [(5, 1)] + rep(10, (0.5, 5), (0.5, 1))), C15])
prof("ski-c4.s1.d2", [W20, ("6 × 2′ Z5 / 2′", rep(6, (2, 5), (2, 1))), C15])
prof("ski-c4.s2.d1", [W20, ("2 × 8 × 40/20", rep(8, (2 / 3, 5), (1 / 3, 1)) + [(5, 1)] + rep(8, (2 / 3, 5), (1 / 3, 1))), C15])
prof("ski-c4.s2.d2", [W20, ("4 × 4′ Z5 / 3′", rep(4, (4, 5), (3, 1))), C15])
prof("ski-c4.s3.d1", [W20, ("2 × 6 × 15″/45″", rep(6, (0.25, 5.5), (0.75, 4)) + [(6, 1)] + rep(6, (0.25, 5.5), (0.75, 4))), C15])
prof("ski-c4.s3.d3", [W20, ("3 montées 12′ Z4 + descentes", rep(3, (12, 4), (10, 1))), C15])
prof("ski-c4.s4.d1", [W20, ("5 × 1′ Z5 / 2′", rep(5, (1, 5), (2, 1))), C10])
prof("ski-c5.s1.d1", [W25, ("8 × 10″ sprint / 2′", rep(8, (1 / 6, 5.5), (2, 1))), ("Calme 20′", [(20, 1)])])
prof("ski-c5.s2.d2", [W20, ("6 × 30″ à fond / 3′", rep(6, (0.5, 5.5), (3, 1))), C15])
prof("ski-c5.s2.d3", [("4 boucles : 15′ Z3 en montée + descente", rep(4, (15, 3), (15, 1)))])

# Gravel
prof("gravel-c1.s3.d2", [("5 × 3′ à la PC / 3′ souple", rep(5, (3, 4), (3, 1)))])
prof("gravel-c1.s4.d1", [("6 × 3′ Z3 / 2′ Z1", rep(6, (3, 3), (2, 1)))])
prof("gravel-c1.s4.d2", [("8 × 15″ all-out / 4′ Z1", rep(8, (0.25, 5.5), (4, 1)))])
prof("gravel-c1.s4.d3", [("2h Z2", [(120, 2)]), ("20′ Z3", [(20, 3)]), ("5 × 1′", rep(5, (1, 5), (3, 1)))])
prof("gravel-c2.s2.d2", [W20, ("3 × 15′ Z3 / 5′ Z2", rep(3, (15, 3), (5, 2)))], total=120)
prof("gravel-c3.s1.d1", [W20, ("3 × 15′ SV1 / 5′", rep(3, (15, 2.6), (5, 1)))], total=90)
prof("gravel-c3.s1.d3", [W15, ("2 × 20′ sweet spot / 8′", rep(2, (20, 3.6), (8, 1)))], total=75)
prof("gravel-c3.s2.d1", [W20, ("4 × 8′ seuil / 4′", rep(4, (8, 4), (4, 1)))], total=75)
prof("gravel-c3.s2.d3", [W20, ("5 × 5′ à 105 % / 5′", rep(5, (5, 5), (5, 1)))], total=70)
prof("gravel-c3.s3.d3", [W15, ("3 × 20′ sweet spot / 5′", rep(3, (20, 3.6), (5, 1)))], total=105)
prof("gravel-c3.s4.d1", [W15, ("2 × 10′ SV1 / 5′", rep(2, (10, 2.6), (5, 1)))], total=60)
prof("gravel-c3.s4.d3", [W20, ("3 × 3′ à la PC / 6′", rep(3, (3, 4), (6, 1))), C15])
prof("gravel-c4.s1.d1", [W20, ("2 × 10 × 30/30", rep(10, (0.5, 5), (0.5, 1)) + [(5, 1)] + rep(10, (0.5, 5), (0.5, 1)))], total=75)
prof("gravel-c4.s1.d2", [W20, ("5 × 3′ Z5 / 3′ Z2", rep(5, (3, 5), (3, 2)))], total=80)
prof("gravel-c4.s2.d1", [W20, ("2 × 8 × 40/20", rep(8, (2 / 3, 5), (1 / 3, 1)) + [(8, 1)] + rep(8, (2 / 3, 5), (1 / 3, 1)))], total=80)
prof("gravel-c4.s2.d2", [W25, ("4 × 4′ Z5 / 4′", rep(4, (4, 5), (4, 1.5)))], total=90)
prof("gravel-c4.s4.d1", [W20, ("6 × 30/30", rep(6, (0.5, 5), (0.5, 1))), ("Calme 30′", [(30, 1.5)])], total=60)
prof("gravel-c5.s1.d2", [("5 × 4′ Z3 à 40-50 rpm / 4′", rep(5, (4, 3), (4, 1)))], total=90)
prof("gravel-c5.s2.d1", [("6 × 2′ force Z4 + sprint / 4′", rep(6, (1.83, 4), (1 / 6, 5.5), (4, 1)))], total=90)
prof("gravel-c5.s2.d2", [W20, ("6 × 30″ max / 5′", rep(6, (0.5, 5.5), (5, 1)))], total=90)
prof("gravel-c5.s3.d1", [W25, ("10 × 20″ sprint en côte", rep(10, (1 / 3, 5.5), (2, 1)))], total=90)
prof("gravel-c5.s3.d2", [("4 × 6′ force Z4 / 6′", rep(4, (6, 4), (6, 1)))], total=105)
prof("gravel-c5.s4.d1", [W20, ("3 × 3′ Z3 / 5′", rep(3, (3, 3), (5, 1)))], total=60)
prof("gravel-c5.s4.d2", [W20, ("5 × 6″ sprint / 5′", rep(5, (0.1, 5.5), (5, 1)))], total=60)

# Escalade : 30-30 à la corde
prof("puissance-cardiaque", [("10′ de 30-30 à la corde à sauter", rep(10, (0.5, 4), (0.5, 2)))], title="30″ vif / 30″ calme")


prof("test-12min", [W20, ("12′ réguliers, finis à fond", [(4, 4.4), (4, 4.6), (4, 5)])], title=TEST)


def weight(x, y):
    return f'<rect x="{x - 9}" y="{y}" width="18" height="14" rx="4" fill="{D}"/>' + text(x, y + 11, "kg", 8, BOLD, W)


@illus("test-barre")
def _():
    return panels(
        [
            (["Bras tendus, jambes", "relâchées mais tendues"], hang_front(0) + pill(84, 54, "chrono")),
            (["Sans bouger les mains,", "le plus longtemps possible"], hang_front(0) + arrow(8, 50, 8, 92, O) + text(92, 80, "max", 11, BOLD, O)),
        ]
    )


@illus("test-poutre")
def _():
    sy = 16 + 42 - 34 * 0.15
    art = hang_front(0.15) + line([(52, sy + 34), (68, sy + 50)], D, 2)  # weight belt
    art += f'<rect x="62" y="{sy + 48}" width="18" height="14" rx="4" fill="{D}"/>' + text(71, sy + 59, "kg", 8, BOLD, W)
    return panels(
        [
            (["Réglette 20 mm, 5 s, gainé,", "le plus de lest possible"], art + pill(-20, 16, "20 mm") + pill(-20, 60, "5 s")),
        ]
    )


@illus("test-traction")
def _():
    def lest(level):
        sy = 16 + 42 - 34 * level
        return line([(50, sy + 34), (50, sy + 48)], D, 2) + weight(30, sy + 46).replace('x="21"', 'x="41"').replace('x="30"', 'x="50"')

    return panels(
        [
            (["Lesté, départ", "bras tendus"], hang_front(0) + lest(0)),
            (["Menton au-dessus,", "une seule rép, sans élan"], hang_front(1) + lest(1) + arrow(92, 100, 92, 56, O)),
        ]
    )


def lever_pose(kind):
    s = bar(22, 46, 14) + line([(34, 14), (40, 52)]) + line([(40, 52), (46, 90)], P, 12)
    if kind == "tuck":
        s += line([(46, 90), (70, 82), (72, 104)])
    elif kind == "pike":
        s += line([(46, 90), (92, 86)])
    else:
        s = bar(22, 46, 14) + line([(34, 14), (40, 52)]) + line([(40, 52), (72, 54)], P, 12) + line([(72, 54), (100, 56)])
        return s + head(30, 58, 9)
    return s + head(38, 40, 9)


@illus("test-gainage")
def _():
    return panels(
        [
            (["Chaise", "genoux pliés"], lever_pose("tuck")),
            (["Chaise", "jambes tendues"], lever_pose("pike")),
            (["Front lever", "(drapeau)"], lever_pose("lever")),
        ]
    )


if __name__ == "__main__":
    for name, fn in ILLUS.items():
        with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
            f.write(fn())
    print(len(ILLUS), "illustrations")
