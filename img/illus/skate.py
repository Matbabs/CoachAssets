"""Skate trick cards, built from the trick name: stance, rotation, board motion, contact, module."""

from build import BOLD, SEMI, D, O, P, P2, W, Y, arrow, card, esc, line, pill, text

LEDGE_FILL, RAMP_FILL = "#DDD6FE", "#E4D9FA"
CONTACT = {"tail": (-38, -4), "nose": (38, -4), "back": (-22, 6), "front": (22, 6), "middle": (0, 1)}


def board(x, y, a=0, contact=None, wheels=True, mirror=False):
    """Profile view, tail on the left (x<0); mirror puts the tail on the right."""
    s = f'<g transform="translate({x:.1f},{y:.1f}) rotate({a}){' scale(-1,1)' if mirror else ''}">'
    s += line([(-40, -6), (-33, 0), (33, 0), (40, -6)], D, 4)
    for tx in (-22, 22):
        s += f'<rect x="{tx - 5}" y="2" width="10" height="4" rx="1" fill="{D}"/>'
        if wheels:
            s += f'<circle cx="{tx}" cy="9" r="4.5" fill="{Y}" stroke="{D}" stroke-width="1.5"/>'
    if contact:
        cx, cy = CONTACT[contact]
        s += f'<circle cx="{cx}" cy="{cy}" r="5" fill="none" stroke="{O}" stroke-width="2.5"/>'
    return s + "</g>"


def board_top(x, y, a=0, contact=None):
    """Top view, tail on the left."""
    s = f'<g transform="translate({x:.1f},{y:.1f}) rotate({a})">'
    for tx in (-22, 22):
        for ty in (-12, 7):
            s += f'<rect x="{tx - 4}" y="{ty}" width="8" height="5" rx="1.5" fill="{Y}"/>'
    s += f'<rect x="-42" y="-10" width="84" height="20" rx="10" fill="{D}"/>'
    if contact:
        cx = {"tail": -32, "nose": 32, "middle": 0}[contact]
        s += f'<circle cx="{cx}" cy="0" r="6" fill="none" stroke="{O}" stroke-width="2.5"/>'
    return s + "</g>"


def curved(x1, y1, cx, cy, x2, y2, color=Y, w=3):
    import math

    a = math.atan2(y2 - cy, x2 - cx)
    L = 7
    p1 = (x2 - L * math.cos(a - 0.5), y2 - L * math.sin(a - 0.5))
    p2 = (x2 - L * math.cos(a + 0.5), y2 - L * math.sin(a + 0.5))
    return (
        f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="1 6"/>'
        f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>'
    )


def ground(y=150):
    return f'<line x1="14" y1="{y}" x2="326" y2="{y}" stroke="{P2}" stroke-width="2" stroke-linecap="round"/>'


# ---------- parsing ----------


def parse(name):
    n = name.lower().replace("five-0", "5-0").replace("fivo", "5-0")
    t = {"stance": None, "rot": None, "flip": None, "contact": None, "side": None, "kind": None}
    if "halfcab" in n:
        t["stance"], t["rot"] = "Fakie", "BS 180"
    elif "switch" in n:
        t["stance"] = "Switch"
    elif "fakie" in n and "to fakie" not in n and "slide fakie" not in n:
        t["stance"] = "Fakie"
    elif "nollie" in n:
        t["stance"] = "Nollie"
    for k, v in (("360 flip", "360 flip"), ("varial", "Varial flip"), ("heelflip", "Heelflip"), ("kickflip", "Kickflip"), ("flip ", "Kickflip")):
        if k in n:
            t["flip"] = v
            break
    if "shove" in n:
        t["flip"] = "Shove-it FS" if "frontside pop" in n else "Shove-it"
    side = "frontside" if "frontside" in n else "backside" if "backside" in n else None
    if "180" in n and not t["rot"]:
        t["rot"] = ("FS 180" if side == "frontside" else "BS 180")
        side = None
    elif "180" in n:
        t["rot"] += " + " + ("FS 180" if "frontside 180" in n else "BS 180")
    t["side"] = side
    grinds = [
        ("crooked", "front", "Truck avant + nose"), ("nose grind", "front", "Truck avant"), ("5-0", "back", "Truck arrière"),
        ("smith", "back", "Truck arrière, avant plongé"), ("feeble", "back", "Truck arrière, avant par-dessus"),
        ("50-50", "both", "Les 2 trucks"), ("axle stall", "both", "Les 2 trucks calés"), ("grind", "both", "Les 2 trucks"),
    ]
    slides = [("boardslide", "middle", "Milieu de planche"), ("nose slide", "nose", "Nose"), ("tail slide", "tail", "Tail")]
    stalls = [
        ("drop in", "Tail sur le coping, bascule"), ("rock to fakie", "Milieu sur le coping"), ("halfcab rock", "Milieu sur le coping"),
        ("disaster", "Milieu sur le coping"), ("tailside", "Tail sur le coping"), ("tail stall", "Tail sur le coping"),
        ("nose stall", "Nose sur le coping"), ("nose roll", "Nose par-dessus le coping"), ("kick turn", "Pivot en haut de la courbe"),
        ("pivot", "Truck arrière sur le coping"),
    ]
    for k, c, label in slides:
        if k in n:
            t.update(kind="slide", contact=c, label=label)
            return t
    for k, label in stalls:
        if k in n:
            t.update(kind="stall", stall=k, label=label)
            return t
    for k, c, label in grinds:
        if k in n:
            t.update(kind="grind", contact=c, grind=k, label=label)
            return t
    t["kind"] = "flat"
    return t


# ---------- scenes ----------


def flat_scene(t):
    s = ground()
    fakie = t["stance"] in ("Fakie", "Switch")
    nollie = t["stance"] == "Nollie"
    s += board(46, 138)
    s += board(118, 128, 24 if nollie else -24, "nose" if nollie else "tail")
    s += board(200, 82)
    s += board(290, 138)
    s += curved(130, 108, 165, 50, 196, 66, P, 2.5) + curved(214, 66, 250, 52, 282, 118, P, 2.5)
    lab = []
    if t["flip"]:
        if "flip" in t["flip"].lower():  # roll around the long axis
            s += f'<ellipse cx="200" cy="82" rx="14" ry="24" fill="none" stroke="{O}" stroke-width="3" stroke-dasharray="5 4"/>'
            s += arrow(212, 66, 214, 74, O)
        if "Shove" in t["flip"] or "Varial" in t["flip"] or "360" in t["flip"]:  # spin flat
            s += f'<ellipse cx="200" cy="82" rx="46" ry="11" fill="none" stroke="{Y}" stroke-width="3" stroke-dasharray="5 4"/>'
            s += arrow(160, 88, 168, 92, Y)
    if t["rot"]:
        s += curved(150, 44, 200, 6, 250, 44, O, 3) + text(200, 24, "180°", 11, BOLD, O)
    s += arrow(30, 166, 90, 166, P, 2.5) + text(98, 170, "fakie (tail devant)" if fakie else "sens de roulage", 10, SEMI, P, "start")
    return s + "".join(lab)


GRIND_POSE = {"both": (0, 104), "front": (12, 101), "back": (-12, 101)}


def grind_scene(t, park):
    s = ""
    edge = 108
    if park:
        s += f'<rect x="90" y="{edge}" width="236" height="42" fill="{RAMP_FILL}"/>'
        s += line([(90, edge), (326, edge)], D, 6)
        s += text(320, edge + 30, "coping (face de la rampe)", 10, SEMI, P, "end")
    else:
        s += f'<rect x="90" y="{edge}" width="236" height="42" rx="3" fill="{LEDGE_FILL}"/>'
        s += line([(90, edge), (326, edge)], D, 3)
        s += text(320, edge + 30, "ledge", 10, SEMI, P, "end")
    s += ground()
    c, g = t["contact"], t.get("grind", "")
    a, y = GRIND_POSE[c]
    if "smith" in g:
        a, y = 16, 100
    if "feeble" in g:
        a, y = 6, 101
    if "crooked" in g:
        a, y = 14, 100
    contact = {"both": "middle", "front": "front", "back": "back"}[c]
    if "crooked" in g:
        contact = "nose"
    s += board(46, 138, -18, "tail")
    s += curved(60, 120, 90, 70, 132, 86, P, 2.5)
    s += board(190, y, a, contact)
    if "stall" not in g:
        s += arrow(246, 80, 300, 80, O) + text(274, 70, "glisse", 10, BOLD, O)
    return s


def slide_scene(t):
    s = f'<rect x="20" y="96" width="306" height="54" rx="4" fill="{LEDGE_FILL}"/>'
    s += line([(20, 96), (326, 96)], D, 3) + text(320, 140, "ledge (vu de dessus)", 10, SEMI, P, "end")
    c = t["contact"]
    yc = {"middle": 96, "nose": 70, "tail": 70}[c]
    a = 90 if c == "nose" else -90  # nose / tail pointing down onto the ledge
    s += board_top(170, yc, a, c)
    s += arrow(60, 66, 120, 66, P, 2.5) + text(60, 56, "approche", 10, SEMI, P, "start")
    s += arrow(206, 116, 280, 116, O) + text(244, 108, "glisse", 10, BOLD, O)
    return s


def quarter():
    # quarter pipe in profile: flat, transition, coping, deck
    s = f'<path d="M14,150 L190,150 Q280,150 280,62 L326,62 L326,160 L14,160 Z" fill="{RAMP_FILL}"/>'
    s += f'<path d="M14,150 L190,150 Q280,150 280,62" fill="none" stroke="{P2}" stroke-width="2"/>'
    s += line([(280, 62), (326, 62)], P2, 2)
    s += f'<circle cx="280" cy="62" r="5" fill="{D}"/>' + text(292, 82, "coping", 10, SEMI, P, "start")
    return s


STALL_POSE = {  # angle, contact on the coping, mirrored (tail on the right)
    "drop in": (-25, "tail", True),
    "rock to fakie": (0, "middle", False),
    "halfcab rock": (0, "middle", False),
    "disaster": (0, "middle", False),
    "tailside": (-30, "tail", True),
    "tail stall": (-60, "tail", True),
    "nose stall": (-60, "nose", False),
    "nose roll": (-4, "nose", False),
    "kick turn": (-55, "back", False),
    "pivot": (-40, "back", False),
}


def on_coping(a, contact, mirror):
    """Board centre that puts the contact point on the coping (280, 62)."""
    import math

    cx, cy = CONTACT[contact]
    cy += 4  # sit on top of the pipe
    if mirror:
        cx = -cx
    r = math.radians(a)
    return 280 - (cx * math.cos(r) - cy * math.sin(r)), 62 - (cx * math.sin(r) + cy * math.cos(r))


def stall_scene(t):
    k = t["stall"]
    a, c, mirror = STALL_POSE[k]
    x, y = on_coping(a, c, mirror)
    s = quarter()
    if k == "drop in":
        s += curved(240, 80, 230, 140, 130, 140, O, 3) + text(120, 128, "descends, poids devant", 10, BOLD, O)
    elif k in ("kick turn", "pivot"):
        s += curved(200, 112, 250, 110, 250, 70, P, 2.5) + curved(236, 46, 250, 22, 288, 34, O, 3) + text(214, 24, "tourne", 10, BOLD, O)
    else:
        s += curved(150, 140, 250, 140, 262, 72, P, 2.5) + text(140, 128, "monte", 10, SEMI, P)
        s += curved(244, 42, 220, 60, 200, 110, O, 3) + text(186, 64, "redescends", 10, BOLD, O)
    s += board(x, y, a, c, mirror=mirror)
    return s


def trick(name, day):
    t = parse(name)
    if t["kind"] == "flat":
        scene = flat_scene(t)
    elif t["kind"] == "slide":
        scene = slide_scene(t)
    elif t["kind"] == "stall":
        scene = stall_scene(t)
    else:
        scene = grind_scene(t, day == "PARK")
    tags = [x for x in (t["stance"], t["rot"], t["flip"], t.get("label")) if x]
    if t["kind"] == "flat":
        tags.insert(0, "Pop du nose" if t["stance"] == "Nollie" else "Pop du tail")
    elif t["side"]:
        tags.append("Face au module" if t["side"] == "frontside" else "Dos au module")
    tags.insert(0, {"STREET": "Flat", "PARK": "Park", "LEDGE": "Ledge"}.get(day, day))
    s = text(16, 24, name, 13, BOLD, D, "start")
    s += f'<g transform="translate(0,6)">{scene}</g>'
    x, y = 16, 188
    for tag in tags:
        w = len(tag) * 6.2 + 14
        if x + w > 326:
            x, y = 16, y + 24
        s += pill(x + w / 2, y, tag, P, W, 10).replace(f'width="{w - 2:.1f}"', f'width="{w:.1f}"')
        x += w + 6
    return card(y + 18, s)


def slug(s):
    import re, unicodedata

    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def sessions(root):
    """[(html path, day, trick)] for every skate session."""
    import glob, re

    out = []
    for f in sorted(glob.glob(f"{root}/sessions/skate/*.html")):
        m = re.search(r"<strong>Jour \d+: (\w+) \| ([^<]+)</strong>", open(f).read())
        if m:
            out.append((f, m[1], m[2].strip()))
    return out


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    seen = {}
    for f, day, name in sessions(os.path.join(here, "../..")):
        n = f"skate-{slug(day)}-{slug(name)}"
        if n not in seen:
            seen[n] = trick(name, day)
            open(os.path.join(here, n + ".svg"), "w").write(seen[n])
    print(len(seen), "skate cards")
