"""Remaining content: strength/mobility circuits, last climbing drills, level ladders for tests, banners for rest/mental days."""

import os

from build import (
    BOLD, SEMI, D, O, P, P2, W, Y, arrow, bar, card, ground, hang_front, hang_one_arm, head, line, panels,
    pill, plank, side_plank, squat_side, superman, text,
)
from fiches import fiche, wrap

ILLUS = {}
GY = 124  # ground line of the 100x130 pose box


# ---------- extra poses (100x130 box, facing right) ----------


def stand(arms="down", leg=None):
    s = ground(10, 90, GY + 2)
    s += line([(50, 46), (50, 84)], P, 12)
    s += line([(50, 84), (46, 104), (44, GY)], P2) if leg != "up" else line([(50, 84), (66, 92), (64, 110)], P2)
    s += line([(50, 84), (54, 104), (56, GY)])
    if arms == "forward":
        s += line([(50, 52), (74, 56), (92, 56)])
    elif arms == "side":
        s += line([(50, 52), (28, 66)]) + line([(50, 52), (72, 66)], P2)
    else:
        s += line([(50, 52), (46, 70), (46, 86)])
    return s + head(52, 34, 9)


def lunge():
    s = ground(10, 90, GY + 2)
    s += line([(48, 78), (70, 96), (70, GY)]) + line([(48, 78), (30, 104), (16, GY - 2)], P2)
    return s + line([(48, 78), (48, 40)], P, 12) + line([(48, 46), (50, 66), (52, 78)]) + head(50, 26, 9)


def pushup():
    s = ground(0, 100, GY + 2)
    s += line([(82, 92), (84, GY)]) + line([(82, 92), (18, 112)], P, 12) + line([(18, 112), (6, GY)])
    return s + head(92, 86, 8)


def wall_sit():
    s = line([(20, 30), (20, GY + 2)], D, 3) + ground(10, 90, GY + 2)
    s += line([(26, 50), (26, 90)], P, 12) + line([(26, 90), (60, 92), (60, GY)]) + line([(26, 58), (40, 74), (56, 76)])
    return s + head(30, 36, 9)


def step_up():
    s = f'<rect x="54" y="{GY - 26}" width="40" height="28" rx="3" fill="{P2}"/>' + ground(6, 94, GY + 2)
    s += line([(44, 78), (64, 84), (66, GY - 26)]) + line([(44, 78), (36, 102), (34, GY)], P2)
    return s + line([(44, 78), (46, 40)], P, 12) + line([(46, 48), (44, 66), (48, 80)]) + head(48, 26, 9)


def hinge():
    s = ground(10, 90, GY + 2)
    s += line([(40, 76), (40, 100), (40, GY)]) + line([(40, 76), (78, 64)], P, 12)
    s += line([(72, 66), (72, 100)]) + f'<rect x="58" y="100" width="28" height="6" rx="3" fill="{D}"/>'
    return s + head(88, 58, 8)


def twist():
    s = stand("forward") + arrow(84, 40, 64, 30, O) + arrow(18, 40, 38, 30, O)
    return s


def stretch():
    s = ground(0, 100, GY + 2)
    s += line([(30, 112), (70, 116)], P, 12) + line([(70, 116), (92, GY)]) + line([(30, 112), (12, 100), (6, 86)])
    return s + head(16, 116, 8)


def lying_back():
    s = ground(0, 100, GY + 2)
    s += line([(30, 116), (66, 116)], P, 12) + line([(66, 116), (76, 92), (92, 92)]) + line([(34, 114), (40, 90)])
    return s + head(20, 114, 8)


def quadruped(extend=True):
    s = ground(0, 100, GY + 2)
    s += line([(36, 90), (72, 90)], P, 12) + line([(72, 90), (72, GY)]) + line([(36, 90), (40, 112), (30, GY - 6)], P2)
    if extend:
        s += line([(72, 90), (96, 82)], P2) + line([(36, 90), (6, 88)])
    else:
        s += line([(36, 90), (38, GY)])
    return s + head(82, 80, 8)


def band():
    s = stand("side").replace(f'stroke="{P}"', f'stroke="{P}"', 1) + line([(28, 66), (72, 66)], Y, 3)
    return s


def run():
    s = ground(10, 90, GY + 2)
    s += line([(50, 80), (66, 100), (60, GY)]) + line([(50, 80), (34, 98), (22, 104)], P2)
    s += line([(50, 80), (54, 44)], P, 12) + line([(54, 50), (70, 62), (78, 52)]) + line([(54, 50), (38, 64)], P2)
    return s + head(58, 30, 9)


def swim():
    s = f'<rect x="0" y="90" width="100" height="36" fill="#DBEAFE"/>'
    s += line([(20, 96), (70, 94)], P, 11) + line([(70, 94), (96, 82)]) + line([(20, 96), (4, 100)])
    return s + head(80, 96, 8)


def jump():
    return squat_side(0, False, 12) + arrow(86, 104, 86, 62, O)


def breath_pose():
    return lying_back() + text(50, 60, "inspire 3 s", 11, BOLD, P) + text(50, 76, "expire 6 s", 11, BOLD, O)


def head_think():
    s = head(50, 80, 18) + f'<ellipse cx="72" cy="40" rx="24" ry="16" fill="{W}" stroke="{P}" stroke-width="2"/>'
    return s + f'<circle cx="56" cy="62" r="4" fill="{W}" stroke="{P}" stroke-width="2"/>'


POSES = [  # keyword -> pose; the first match wins
    ("squat sauté", jump), ("saut", jump), ("bond", jump), ("drop jump", jump), ("pliom", jump),
    ("chaise", wall_sit), ("step-up", step_up), ("soulevé", hinge), ("fente", lunge), ("squat", lambda: squat_side(1)),
    ("latéral", side_plank), ("superman", superman), ("dead bug", lying_back), ("planche", lambda: plank("classic")),
    ("gainage", lambda: plank("classic")), ("pompe", pushup), ("burpee", pushup), ("pop-up", pushup),
    ("balance", lambda: stand("side", "up")), ("unipodal", lambda: stand("side", "up")), ("équilibre", lambda: stand("side", "up")),
    ("rotation", twist), ("twist", twist), ("woodchop", twist), ("médecine", twist), ("élastique", band), ("y-t-w", band),
    ("traction", lambda: hang_front(1)), ("tirage", lambda: hang_front(1)), ("suspension", lambda: hang_front(0)),
    ("mollet", lambda: stand()), ("nage", swim), ("crawl", swim), ("vélo", run), ("cardio", run), ("footing", run),
    ("respir", breath_pose), ("visualis", head_think), ("quatre pattes", quadruped), ("cobra", stretch), ("pigeon", stretch),
    ("étire", stretch), ("mobilité", stretch), ("cercles", lambda: stand("side")), ("enroulé", stretch), ("enfant", stretch),
    ("90/90", stretch), ("foam", lying_back), ("flexion de cheville", lunge), ("pig dog", lunge),
]


def pose_for(item):
    low = item.lower()
    for k, fn in POSES:
        if k in low:
            return fn()
    return stand()


def circuit(name, title, rounds, items):
    """Numbered stations, each with a small pose and its prescription."""
    s = text(16, 24, title, 13, BOLD, D, "start") + text(16, 42, rounds, 11, SEMI, P, "start")
    y = 54
    for i, it in enumerate(items):
        lines = wrap(it, 40)[:2]
        s += f'<rect x="12" y="{y}" width="316" height="56" rx="10" fill="{W}"/>'
        s += f'<g transform="translate(20,{y - 2}) scale(0.45)">{pose_for(it)}</g>'
        s += f'<circle cx="76" cy="{y + 28}" r="9" fill="{Y}"/>' + text(76, y + 32, str(i + 1), 11, BOLD, D)
        for k, l in enumerate(lines):
            s += text(94, y + 32 - 7 * (len(lines) - 1) + k * 14, l, 11, SEMI, D, "start")
        y += 62
    ILLUS[name] = card(y + 4, s)


# ---------- strength & mobility circuits ----------

circuit("ski-c5.s1.d2", "Renforcement lourd", "Échauf. 10′ cardio + mobilité · retour au calme 5′",
        ["4 × 6 squats lourds (80 % du max), récup 2′", "3 × 8 step-ups lestés par jambe", "3 × 45″ de gainage avec charge"])
circuit("ski-c5.s2.d1", "Renforcement excentrique", "Échauf. 10′ · retour au calme 5′",
        ["4 × 8 squats excentriques (descente 5 s)", "3 × 30″ de chaise au mur + 3 × 10 fentes arrière", "3 × 10 descentes de marche sur une jambe"])
circuit("ski-c5.s3.d2", "Force maximale", "Échauf. 10′ cardio + mobilité · retour au calme 5′",
        ["4 × 6 squats lourds", "3 × 8 fentes bulgares", "3 × 30″ de chaise au mur", "3 × 12 soulevés de terre jambe tendue (léger)"])
circuit("ski-c5.s4.d1", "Rappel de force (léger)", "Échauf. 10′ · retour au calme 5′",
        ["2 × 6 squats à 70 %", "2 × 8 fentes", "2 × 40″ de gainage", "10′ de mobilité"])
circuit("surf-c1.s2.d2", "Mobilité épaules et dos", "3 tours",
        ["10 cercles de bras avec un bâton", "10 extensions en cobra", "10 rotations thoraciques à quatre pattes / côté", "30″ d'étirement du grand dorsal au mur"])
circuit("surf-c1.s3.d2", "Gainage du surfeur", "3 tours · 1′ de repos",
        ["40″ de planche", "30″ de planche latérale par côté", "15 superman", "20 dead bugs"])
circuit("surf-c1.s6.d2", "Équilibre", "3 tours",
        ["1′ sur balance board (ou une jambe sur un coussin)", "10 squats en position de surf", "10 pop-ups, arrivée stable 3 s"])
circuit("surf-c2.s8.d2", "Rotation du tronc", "3 tours",
        ["12 lancers de médecine-ball au mur / côté", "12 woodchops à l'élastique / côté", "30″ de Russian twists", "10 fentes avec rotation"])
circuit("surf-c2.s9.d2", "Force des épaules", "3 tours",
        ["15 rotations externes à l'élastique / bras", "12 Y-T-W allongé sur le ventre", "10 tractions ou tirages horizontaux", "30″ de suspension à une barre"])
circuit("surf-c2.s11.d2", "Mobilité des hanches", "Enchaîne",
        ["2′ de 90/90 par côté", "2′ de squat profond tenu", "1′ de pigeon par côté", "10 rotations de hanches à quatre pattes"])
circuit("surf-c3.s13.d2", "Pliométrie jambes", "4 tours · 30″ de repos",
        ["8 squats sautés", "8 fentes sautées par jambe", "6 sauts sur un banc ou une caisse", "Pour finir : 2 × 12 squats sur une jambe"])
circuit("surf-c3.s16.d2", "Mobilité chevilles et genoux", "3 tours",
        ["1′ de flexion de cheville, genou au mur", "10 squats profonds lents", "1′ en position pig dog", "10 fentes latérales"])
circuit("surf-c4.s19.d2", "Pliométrie et réception", "4 tours · 1′ de repos",
        ["6 drop jumps, réception stable 3 s", "8 sauts latéraux", "8 squats sautés avec rotation de 90°"])
circuit("surf-c4.s20.d2", "Mobilité thoracique", "3 tours",
        ["10 rotations thoraciques sur le côté", "10 extensions sur foam roller", "1′ d'enroulé-déroulé du dos", "1′ en position de l'enfant"])
circuit("surf-c4.s24.d2", "Récupération active", "Une fois",
        ["30′ de nage douce ou de vélo léger", "20′ d'étirements : épaules, hanches, ischios, dos", "5′ de respiration lente"])
circuit("surf-c3.s18.d2", "Endurance de rame longue", "Au choix",
        ["Piscine : 1500 à 2000 m de crawl continu", "Jour plat : 45′ de rame continue le long du bord"])
circuit("surf-c4.s23.d2", "Préparation mentale", "Avant ta session",
        ["10′ de visualisation : ta session complète", "Note 3 objectifs précis pour la prochaine session"])


# ---------- last climbing drills ----------


def hold(x, y, w):
    return f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="6" rx="3" fill="{D}"/>'


wall = f'<rect x="0" y="0" width="100" height="130" rx="6" fill="{P2}" opacity="0.5"/>'
route = [(20, 118), (34, 98), (24, 80), (46, 66), (36, 48), (60, 36), (54, 18), (76, 10)]
w = wall + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{Y}"/>' for x, y in route)
w += f'<polyline points="{" ".join(f"{x},{y}" for x, y in route)}" fill="none" stroke="{P}" stroke-width="2" stroke-dasharray="3 4"/>'
tl = "".join(
    f'<rect x="{4 + i * 33}" y="54" width="20" height="40" rx="3" fill="{O}"/><rect x="{25 + i * 33}" y="82" width="10" height="12" rx="2" fill="#DDD6FE"/>'
    for i in range(3)
) + text(50, 112, "3 circuits", 10, BOLD, O) + text(50, 126, "5′ entre chaque", 10, SEMI, P)
ILLUS["circuits-blocs"] = panels([(["20 à 30 mouvements", "par circuit"], w), (["Full intensité,", "zéro triche"], tl)])

ILLUS["isometrique-doigts-2-bras"] = panels([
    (["Suspendu à 2 bras,", "prise de préférence en tendu"], hang_front(0) + pill(84, 50, "≈ 5 s")),
    (["Serre aussi fort que possible,", "jusqu'à tes limites"], f'<g transform="translate(0,0)">{hang_front(0.1)}</g>' + pill(50, 124, "3 rép. / 3′")),
])


def two_bars(level, grip_low=False):
    s = bar(14, 86, 4) + bar(14, 86, 24)
    return s + f'<g transform="translate(0,{12 if grip_low else -6})">{hang_front(level)}</g>'


ILLUS["pliometrie-moyenne"] = panels([
    (["Accroché à la", "latte du haut"], two_bars(0.6)),
    (["Lâche, tombe sur", "la latte du dessous"], two_bars(0.5, True) + arrow(94, 40, 94, 74, O)),
    (["Rebondis vers le haut", "sans temps d'arrêt"], two_bars(0.8) + arrow(94, 90, 94, 50, O)),
])
ILLUS["core-crawl"] = panels([
    (["À quatre pattes,", "genoux décollés de 2-3 cm"], quadruped(False) + arrow(30, GY + 0, 30, GY - 12, O)),
    (["Bras et jambe opposés tendus,", "30″ par côté"], quadruped(True) + pill(50, 50, "30″")),
])
ILLUS["planche-instable"] = panels([(
    ["Main sur un support instable, jambe opposée levée,", "tronc et bassin alignés"],
    f'<g transform="translate(-10,-30) scale(1.2)">{plank("one_leg")}<ellipse cx="80" cy="{GY - 4}" rx="14" ry="6" fill="{Y}"/></g>',
)])


def pyramid():
    lv = [("Débutant", 3), ("Intermédiaire", 4), ("Avancé", 5), ("Expert", 6)]
    s = text(16, 24, "Tractions pyramide", 13, BOLD, D, "start") + text(16, 42, "30″ de repos à chaque série", 11, SEMI, P, "start")
    y = 60
    for label, top in lv:
        reps = list(range(1, top + 1)) + list(range(top - 1, 0, -1))
        s += text(16, y + 14, label, 11, SEMI, D, "start")
        for i, r in enumerate(reps):
            s += f'<rect x="{110 + i * 19}" y="{y + 20 - r * 3.4:.1f}" width="15" height="{r * 3.4:.1f}" rx="2" fill="{O if r == top else P}"/>'
        y += 34
    ILLUS["tractions-pyramide"] = card(y + 6, s)


pyramid()


def close_grip(level):
    return hang_front(level).replace('<polyline points="30', '<polyline points="44').replace('<polyline points="70', '<polyline points="56')


ILLUS["traction-prise-serree"] = panels([(["Mains presque", "collées"], close_grip(0.2)), (["Tire jusqu'en haut,", "4 à 10 rép."], close_grip(1))])
ILLUS["controle-muerte"] = panels([
    (["Monte à 2 bras", "en haut"], hang_front(1)),
    (["Lâche un bras", "(faible d'abord)"], hang_one_arm(1)),
    (["Descends très", "lentement"], hang_one_arm(0.4) + arrow(90, 50, 90, 96, O)),
])
ILLUS["traction-1-bras-90"] = panels([
    (["Bloqué à 90°", "à deux mains"], hang_front(0.7)),
    (["Lâche un bras et", "termine le mouvement"], hang_one_arm(1) + arrow(90, 100, 90, 60, O)),
])
ILLUS["traction-1-bras-saute"] = panels([
    (["Pieds au sol, une main", "à la barre"], bar(30, 70, 14) + line([(50, 14), (52, 50)]) + squat_side(0.4).replace(ground(10, 90, 126), "")),
    (["Pousse fort sur les jambes", "puis tracte"], hang_one_arm(1) + arrow(90, 110, 90, 60, O)),
])
ILLUS["traction-1-bras-poignet"] = panels([
    (["Une main à la barre,", "l'autre tient le poignet"], hang_one_arm(0.3) + line([(56, 40), (54, 22)], P2)),
    (["Monte, puis passe", "au bras seul"], hang_one_arm(1)),
])
ILLUS["traction-bras-privilegie"] = panels([
    (["Centre de gravité sous", "le bras qui travaille"], hang_front(0.3, dx=-10)),
    (["L'autre bras ne fait", "qu'aider"], hang_front(1, dx=-10) + arrow(90, 100, 90, 60, O)),
])
ILLUS["traction-max"] = panels([
    (["Bien échauffé,", "bras tendus"], hang_front(0)),
    (["Le plus de tractions possible,", "note ton score"], hang_front(1) + pill(84, 50, "max")),
])


def leg_up():
    s = hang_front(0)
    return s.replace('<polyline points="55,92 57,110 56,126"', '<polyline points="55,92 72,96 86,92"')


ILLUS["suspension-jambe-levee"] = panels([
    (["Bras tendus,", "stable"], hang_front(0)),
    (["Lève lentement une jambe", "vers l'avant, 10″ / côté"], hang_front(0) + line([(55, 92), (74, 94), (92, 90)], Y, 6)),
])
ILLUS["suspension-doigt"] = panels([
    (["Suspendu bras tendus"], hang_front(0)),
    (["Relâche un doigt 1 s,", "reprends, alterne"], hang_front(0) + f'<circle cx="70" cy="16" r="8" fill="none" stroke="{O}" stroke-width="2.5"/>' + pill(84, 40, "1 s")),
])
ILLUS["toucher-croise"] = panels([
    (["Suspendu,", "position passive"], hang_front(0)),
    (["Genou droit vers coude", "gauche, puis change"], hang_front(0) + line([(55, 92), (40, 80), (34, 66)], Y, 6)),
])
ILLUS["appuis-croises"] = panels([
    (["Genoux à", "droite"], hang_front(0) + line([(50, 92), (70, 96), (78, 82)], Y, 6)),
    (["Genoux à", "gauche"], hang_front(0) + line([(50, 92), (30, 96), (22, 82)], Y, 6)),
    (["Position en L,", "tiens 2 s"], hang_front(0) + line([(50, 92), (86, 92)], Y, 6)),
])
ILLUS["micro-mobilite-plantaire"] = panels([(
    ["Pieds nus sur un support souple : transferts de poids", "avant-arrière et gauche-droite, 30″"],
    stand("forward") + f'<ellipse cx="50" cy="{GY + 2}" rx="30" ry="6" fill="{Y}"/>' + arrow(20, 112, 6, 112, O) + arrow(80, 112, 94, 112, O),
)])
ILLUS["appuis-yeux-fermes"] = panels([(
    ["Yeux fermés, bras tendus devant : rotation très lente", "du buste à droite puis à gauche, 20″"],
    twist() + pill(84, 20, "yeux fermés"),
)])


# ---------- tests: level ladders ----------


def ladder(name, title, levels, note=""):
    s = text(16, 24, title, 13, BOLD, D, "start")
    n = len(levels)
    y0 = 40
    for i, lv in enumerate(levels):
        h = 26 + i * 14
        x = 16 + i * (300 / n)
        s += f'<rect x="{x:.0f}" y="{y0 + (n - 1) * 14 + 26 - h}" width="{300 / n - 6:.0f}" height="{h}" rx="6" fill="{[P2, P, O, Y][min(i, 3)]}"/>'
        s += text(x + (300 / n - 6) / 2, y0 + (n - 1) * 14 + 26 - h + 17, f"Niv. {i + 1}", 11, BOLD, W if i in (1, 2) else D)
    y = y0 + (n - 1) * 14 + 26 + 22
    for i, lv in enumerate(levels):
        ls = wrap(lv, 44)[:2]
        s += f'<circle cx="25" cy="{y - 4}" r="9" fill="{Y}"/>' + text(25, y, str(i + 1), 11, BOLD, D)
        for k, l in enumerate(ls):
            s += text(42, y + k * 15, l, 11, SEMI, D, "start")
        y += 15 * len(ls) + 9
    if note:
        s += text(16, y + 2, note, 11, SEMI, P, "start")
        y += 18
    ILLUS[name] = card(y, s)


def test_levels(root):
    import re

    out = {}
    for t in ("grind", "manoeuvres", "dropin", "takeoff", "duckdive", "virage", "gap", "tricks"):
        raw = open(os.path.join(root, f"tests/{t}.html")).read()
        lv = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", v)).strip() for v in re.findall(r"Niveau \d+\s*:\s*(.+?)(?=<br|\n|- Niveau|$)", raw)]
        title = re.sub(r"<[^>]+>", "", re.search(r"<strong>(.*?)</strong>", raw, re.S)[1]).strip()
        ladder(f"test-{t}", title, lv, "Valide un niveau avant de passer au suivant.")
        out[t] = f"test-{t}"
    return out


ladder("test-manual", "Le Manual", ["Intermédiaire : 5 m", "Avancé : 10 m et plus", "Expert : 15 m et plus"], "Distance roulée sur les roues arrière.")
ladder("test-pop", "La hauteur de pop", ["Débutant : 10-15 cm", "Intermédiaire : 20-30 cm", "Avancé : 35-45 cm", "Expert : 50 cm et plus"], "Hauteur maximale de ton ollie.")
ladder("test-rame", "Endurance de rame (5 min)", ["Débutant : ≈ 150 m", "Intermédiaire : ≈ 250 m", "Confirmé : ≈ 350 m", "Expert : 450 m et plus"], "Mer plate, zone surveillée ou piscine.")
ladder("test-souffle", "Le Souffle (au sec)", ["Débutant : ≈ 30 s", "Intermédiaire : ≈ 60 s", "Confirmé : ≈ 90 s", "Expert : 2 min et plus"], "2′ de respiration calme, allongé, jamais dans l'eau.")
ladder("test-transition", "Transition montée → descente", ["Plus de 3 min : il y a de la marge", "Autour de 1 min 30 : déjà très efficace", "Moins de 30 s : niveau compétiteur"], "Peaux, chaussures, fixations, veste, bâtons.")


# ---------- banners for rest, race and mental days ----------


def banner(name, sport, label, tag, points):
    ILLUS[name] = fiche(name, sport, sum(map(ord, name)), tag, label, points)


banner("trail-c2.s4.d2", "trail", "Repos", "Au programme", ["Repos complet ou étirements", "Sommeil et hydratation", "Recharger les batteries"])
banner("trail-c3.s4.d2", "trail", "Repos", "Au programme", ["Repos total, sieste", "Hydratation", "Recharger l'influx nerveux"])
banner("trail-c4.s4.d2", "trail", "Repos", "Au programme", ["Repos ou 30 min de natation douce", "Détente musculaire totale", "Recharger les batteries"])
banner("trail-c5.s4.d3", "trail", "Jour J", "Ton épreuve", ["Option : 20 min de réveil musculaire le matin", "Plaisir, gestion et persévérance", "Après l'arrivée : 10 min de marche, hydratation"])
for k, label, pts in [
    ("c1.s2.d1", "Océan", ["Dos à la mousse, de l'eau jusqu'à la taille", "Rame 3 à 4 coups avant qu'elle t'atteigne", "Agrippe les rails, glisse droit jusqu'au bord"]),
    ("c1.s6.d3", "Bilan", ["5 vagues vertes en suivant l'épaule", "En respectant les priorités", "Puis tests take-off et passer la barre"]),
    ("c2.s12.d3", "Bilan", ["5 vagues avec bottom turn et top turn", "Filme ta session si possible", "Puis tests virage et manœuvres"]),
    ("c3.s15.d3", "Océan", ["Éloigne-toi de ta planche", "Tombe à plat ou en arrière, protège ta tête", "Attends que ça passe, remonte le long du leash"]),
    ("c3.s16.d3", "Océan", ["Observe 10 min avant d'aller à l'eau", "Repère où la lèvre jette loin devant", "Place-toi au pic, attends la série"]),
    ("c3.s18.d3", "Heat simulé", ["Heat de 20 min avec un ami", "Tes 2 meilleures vagues comptent", "Jugez-vous mutuellement sur 10"]),
    ("c4.s19.d1", "Océan", ["Repère une section qui se dresse", "Pumping pour un maximum de vitesse", "Remonte droit vers la lèvre, relâche la pression"]),
    ("c4.s21.d1", "Grosse houle", ["Observe 20 min : séries et zone d'impact", "Prends des repères à terre", "Reste un peu au large, commence à l'épaule"]),
    ("c4.s21.d3", "Take-off engagé", ["Planche plus longue, place-toi au pic", "Rame jusqu'à sentir la vague te porter", "Pop-up franc, poids sur le pied avant"]),
    ("c4.s23.d1", "Compétition", ["Heat de 25 min avec priorité", "Note le temps restant et les scores", "Priorité : seulement pour une vague qui score"]),
    ("c4.s23.d3", "Sous pression", ["Session de 45 min, objectif 6 vagues", "Décide en moins de 3 secondes", "Analyse tes choix après"]),
    ("c4.s24.d1", "Session de séries", ["Houle puissante adaptée à ton niveau", "Échauffe-toi longuement", "Repères de positionnement et routine mentale"]),
    ("c4.s24.d3", "Freesurf", ["Session libre, cherche ton style", "Enchaîne les manœuvres qui te ressemblent", "Termine par les tests de l'onglet Tests"]),
]:
    banner(f"surf-{k}", "surf", label, "Au programme", pts)
banner("stories-c1.s1", "climb", "Prologue", "", [])
banner("stories-c3.s1", "climb", "Prologue", "", [])


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    test_levels(os.path.join(here, "../.."))
    for n, svg in ILLUS.items():
        open(os.path.join(here, f"x-{n}.svg" if n.startswith(("surf-c", "trail-c", "ski-c", "stories-")) else f"{n}.svg"), "w").write(svg)
    print(len(ILLUS), "extra illustrations")
