"""Header cards for talks, health and stories: a sport landscape + the week's key points or the chapter's challenge."""

import glob
import html
import os
import random
import re

from build import BOLD, SEMI, D, O, P, P2, W, Y, card, esc, line, pill, text

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "../..")
SPORTS = {"": "climb", "gravel": "gravel", "trail": "trail", "surf": "surf", "skate": "skate", "ski": "ski"}
SKIES = [("#EDE5FD", Y), ("#FEF3C7", O), ("#FCE7F3", O), ("#E0F2FE", Y)]
SX, SY, SW, SH = 10, 10, 320, 104  # scene box


def hills(rng, base, amp, color, n=5, opacity=1):
    pts = [(SX, SY + SH)]
    xs = sorted(rng.uniform(SX, SX + SW) for _ in range(n))
    pts += [(SX, base)] + [(x, base - rng.uniform(0.3, 1) * amp) for x in xs] + [(SX + SW, base), (SX + SW, SY + SH)]
    d = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    return f'<polygon points="{d}" fill="{color}" opacity="{opacity}"/>'


def peaks(rng, base, amp, color, n=4, snow=False):
    s, step = "", SW / n
    for i in range(n):
        cx = SX + step * (i + 0.5) + rng.uniform(-14, 14)
        h = amp * rng.uniform(0.6, 1)
        w = step * rng.uniform(0.8, 1.2)
        s += f'<polygon points="{cx - w:.0f},{base} {cx:.0f},{base - h:.0f} {cx + w:.0f},{base}" fill="{color}"/>'
        if snow:
            s += f'<polygon points="{cx - w * 0.28:.0f},{base - h * 0.72:.0f} {cx:.0f},{base - h:.0f} {cx + w * 0.28:.0f},{base - h * 0.72:.0f} {cx + w * 0.1:.0f},{base - h * 0.66:.0f} {cx - w * 0.1:.0f},{base - h * 0.7:.0f}" fill="{W}"/>'
    return s


def scene(sport, seed):
    rng = random.Random(seed)
    sky, sun = SKIES[seed % len(SKIES)]
    s = f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="{sky}"/>'
    s += f'<circle cx="{SX + rng.uniform(40, 280):.0f}" cy="{SY + rng.uniform(26, 44):.0f}" r="14" fill="{sun}"/>'
    g = SY + SH
    if sport == "climb":
        s += hills(rng, g - 20, 30, P2, opacity=0.7)
        x = SX + rng.uniform(150, 210)
        s += f'<polygon points="{x:.0f},{g} {x + 20:.0f},{SY + 18} {x + 70:.0f},{SY + 10} {SX + SW},{SY + 30} {SX + SW},{g}" fill="{P}"/>'
        for i in range(6):
            s += f'<circle cx="{x + 36 + rng.uniform(-8, 40):.0f}" cy="{g - 14 - i * 13:.0f}" r="3.5" fill="{Y}"/>'
        s += hills(rng, g - 8, 12, D, 4)
    elif sport in ("trail", "ski"):
        s += peaks(rng, g - 14, 70, P2, 4, snow=sport == "ski")
        s += peaks(rng, g - 4, 46, P, 3, snow=sport == "ski")
        fg = "#F5F3FF" if sport == "ski" else D
        s += hills(rng, g - 6, 14, fg, 4)
        if sport == "ski":
            z = " ".join(f"{SX + 60 + i * 26},{g - 8 - (i % 2) * 10 - i * 4}" for i in range(9))
            s += f'<polyline points="{z}" fill="none" stroke="{O}" stroke-width="2.5" stroke-dasharray="1 5" stroke-linecap="round"/>'
        else:
            s += f'<path d="M{SX + 40},{g} Q{SX + 140},{g - 30} {SX + 200},{g - 10} T{SX + 300},{g - 26}" fill="none" stroke="{Y}" stroke-width="3" stroke-dasharray="1 6" stroke-linecap="round"/>'
    elif sport == "gravel":
        s += hills(rng, g - 30, 30, P2, 6, 0.8) + hills(rng, g - 12, 24, P, 5)
        s += f'<path d="M{SX + 100},{g} Q{SX + 150},{g - 30} {SX + 230},{g - 34} T{SX + SW},{g - 46}" fill="none" stroke="{SKIES[0][0]}" stroke-width="7" stroke-linecap="round"/>'
        s += f'<path d="M{SX + 100},{g} Q{SX + 150},{g - 30} {SX + 230},{g - 34} T{SX + SW},{g - 46}" fill="none" stroke="{Y}" stroke-width="2" stroke-dasharray="4 6"/>'
    elif sport == "surf":
        sea = g - 40
        s += f'<rect x="{SX}" y="{sea}" width="{SW}" height="40" fill="#93C5FD"/>'
        x = SX + rng.uniform(150, 220)
        s += f'<path d="M{x - 120:.0f},{g} Q{x - 20:.0f},{g - 6} {x:.0f},{sea - 26} Q{x + 22:.0f},{sea - 40} {x + 40:.0f},{sea - 22} Q{x + 22:.0f},{sea - 28} {x + 18:.0f},{sea - 8} Q{x + 40:.0f},{g - 4} {x + 120:.0f},{g} Z" fill="#3B82F6"/>'
        for i in range(5):
            s += f'<circle cx="{x + 30 + i * 14:.0f}" cy="{g - 8 - (i % 2) * 6:.0f}" r="7" fill="{W}"/>'
        s += f'<rect x="{SX}" y="{g - 8}" width="{SW}" height="8" fill="#FDE68A"/>'
    elif sport == "skate":
        x = SX
        while x < SX + SW:
            w, h = rng.uniform(20, 40), rng.uniform(24, 70)
            s += f'<rect x="{x:.0f}" y="{g - 20 - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{P2}"/>'
            for wy in range(int(g - 14 - h), int(g - 26), 12):
                s += f'<rect x="{x + 6:.0f}" y="{wy}" width="5" height="5" fill="{Y}" opacity="0.8"/>'
            x += w + 4
        q = SX + rng.uniform(170, 220)
        s += f'<rect x="{SX}" y="{g - 20}" width="{SW}" height="20" fill="{D}"/>'
        s += f'<path d="M{q:.0f},{g - 20} L{q + 40:.0f},{g - 20} Q{q + 80:.0f},{g - 20} {q + 80:.0f},{g - 60} L{q + 100:.0f},{g - 60} L{q + 100:.0f},{g - 20} Z" fill="{P}"/>'
        s += f'<circle cx="{q + 80:.0f}" cy="{g - 60}" r="3" fill="{Y}"/>'
    return s


def guide(x, y):
    """Cloaked silhouette for the stories' mentors."""
    s = f'<polygon points="{x - 13},{y} {x},{y - 42} {x + 13},{y}" fill="{D}"/>'
    s += f'<circle cx="{x}" cy="{y - 46}" r="7" fill="{D}"/>'
    s += line([(x + 16, y), (x + 18, y - 54)], D, 3) + f'<circle cx="{x + 18}" cy="{y - 56}" r="3.5" fill="{Y}"/>'
    return s


def wrap(s, n=48):
    out, cur = [], ""
    s = s.replace("« ", "«\u00a0").replace(" »", "\u00a0»").replace(" ?", "\u00a0?").replace(" !", "\u00a0!")
    for w in s.split(" "):
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + [cur] if cur else out


def fiche(name, sport, seed, tag, label, points=(), quest=None):
    clip = f"c-{name}"
    s = f'<defs><clipPath id="{clip}"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="12"/></clipPath></defs>'
    s += f'<g clip-path="url(#{clip})">{scene(sport, seed)}'
    if quest is not None:
        s += guide(SX + 40, SY + SH - 6)
    s += "</g>"
    w = len(label) * 6.6 + 16
    s += f'<rect x="{SX + 10}" y="{SY + 10}" width="{w:.0f}" height="20" rx="10" fill="{W}"/>' + text(SX + 10 + w / 2, SY + 24, label, 11, BOLD, P)
    y = SY + SH + 24
    if points:
        s += text(16, y, tag, 13, BOLD, D, "start")
        y += 22
        for i, p in enumerate(points[:4]):
            s += f'<circle cx="25" cy="{y - 4}" r="9" fill="{Y}"/>' + text(25, y, str(i + 1), 11, BOLD, D)
            for k, l in enumerate(wrap(p)[:2]):
                s += text(42, y + k * 15, l, 11, SEMI, D, "start")
            y += 15 * min(2, len(wrap(p))) + 9
    if quest:
        s += text(16, y, "Défi du chapitre", 13, BOLD, D, "start")
        y += 20
        for l in wrap(quest, 46)[:2]:
            s += text(16, y, l, 12, BOLD, P, "start")
            y += 16
        y += 4
    return card(y if (points or quest) else SY + SH + 10, s)


def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"^[^\wÀ-ÿ«\"“]+", "", s)  # leading emoji / punctuation
    return re.sub(r"\s+", " ", s).strip().rstrip(":").strip()


def pages(kind):
    for f in sorted(glob.glob(f"{ROOT}/{kind}/*.html") + glob.glob(f"{ROOT}/{kind}/*/*.html")):
        sub = os.path.basename(os.path.dirname(f))
        sport = SPORTS.get("" if sub == kind else sub, "climb")
        yield f, sport, ("" if sub == kind else sub + "-") + os.path.basename(f)[:-5]


def build():
    """Writes the cards; returns {html path: svg name}."""
    out = {}
    for kind, ktag in (("talks", "Au programme"), ("health", "À retenir")):
        for f, sport, key in pages(kind):
            tag = ktag
            t = open(f).read()
            m = re.search(r"Semaine (\d+)", t)
            week = int(m[1]) if m else 0
            heads = [clean(h) for h in re.findall(r"<p>\s*<strong>(.{3,90}?)</strong>\s*<br\s*/?>", t, re.S)]
            heads = [h for h in heads if h and not h.startswith("Semaine") and "Cette semaine" not in h][:4]
            name = f"fiche-{kind}-{key}"
            label = f"{'Talk' if kind == 'talks' else 'Santé'} · Semaine {week}" if week else ("Talk" if kind == "talks" else "Santé")
            r = re.search(r"RECETTE (N°[\d/]+)", t)
            if r:
                label, tag = f"Recette {r[1]}", "Au menu"
                heads = [clean(h) for h in re.findall(r"<strong>\s*🍽\S*\s*([^<]+)</strong>", t)]
                times = [f"{k} {v}" for k, v in re.findall(r"(Préparation|Cuisson)\s*:\s*</strong>\s*(\d+\s*(?:min|h)|aucune?)", t)][:2]
                if times:
                    heads.append(" · ".join(times))
            seed = sum(map(ord, key))  # stable across runs, varies per page
            open(os.path.join(HERE, name + ".svg"), "w").write(fiche(name, sport, seed, tag, label, heads))
            out[f] = name
    for f, sport, key in pages("stories"):
        t = open(f).read()
        m = re.search(r"CHAPITRE (\d+)", t)
        if not m:
            continue
        q = re.search(r"🎯\s*([^<]+)", t)
        quest = clean(q[1]).split(":", 1)[-1].strip().strip('"“”') if q else ""
        name = f"fiche-stories-{key}"
        open(os.path.join(HERE, name + ".svg"), "w").write(
            fiche(name, sport, sum(map(ord, key)), "", f"Chapitre {m[1]}", quest=quest))
        out[f] = name
    return out


if __name__ == "__main__":
    print(len(build()), "fiches")
