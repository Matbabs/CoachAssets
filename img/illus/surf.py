"""Surf illustrations: maneuver lines on the wave face, top views of the beach, sequences, swell and tide."""

import os

from build import (
    BOLD, SEMI, D, O, P, P2, W, Y, arrow, card, head, line, panels, pill, profile, rep, text,
)

SEA, SEA_D, FOAM, SAND = "#DBEAFE", "#3B82F6", "#FFFFFF", "#FDE68A"
ILLUS = {}


def smooth(pts):
    """Catmull-Rom through the points, as a cubic path."""
    d = f"M{pts[0][0]},{pts[0][1]}"
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}"
    return d


def path(pts, color=P, w=3.5, dash=None):
    import math

    s = f'<path d="{smooth(pts)}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"'
    s += f' stroke-dasharray="{dash}"/>' if dash else "/>"
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    L = 9
    p1 = (x2 - L * math.cos(a - 0.5), y2 - L * math.sin(a - 0.5))
    p2 = (x2 - L * math.cos(a + 0.5), y2 - L * math.sin(a + 0.5))
    return s + f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>'


def step(x, y, n):
    return f'<circle cx="{x}" cy="{y}" r="9" fill="{Y}"/>' + text(x, y + 4, str(n), 11, BOLD, D)


def lip(x):
    return 56 + max(0, x - 100) * 0.27


# ---------- wave face (right-hander seen from the channel) ----------


def wave(tube=False, section=None):
    s = f'<path d="M14,150 L14,64 Q40,40 80,48 Q100,52 110,59 L326,{lip(326):.0f} L326,150 Z" fill="{SEA}"/>'
    s += f'<path d="M110,59 L326,{lip(326):.0f}" stroke="{SEA_D}" stroke-width="3" stroke-linecap="round"/>'
    if tube:  # the lip throwing over the pocket
        s += f'<path d="M14,64 Q40,40 80,48 Q118,58 116,100 Q112,86 96,78 Q60,66 14,90 Z" fill="{SEA_D}" opacity="0.55"/>'
    for cx, cy, r in ((24, 120, 16), (44, 132, 14), (30, 142, 12), (60, 142, 10), (20, 98, 10), (66, 128, 9)):
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FOAM}"/>'
    if section:  # foam section breaking on the face
        x1, x2 = section
        for x in range(x1, x2, 10):
            s += f'<circle cx="{x}" cy="{lip(x) + 4:.0f}" r="7" fill="{FOAM}"/>'
    s += f'<line x1="14" y1="150" x2="326" y2="150" stroke="{SEA_D}" stroke-width="1.5" opacity="0.4"/>'
    s += text(322, 106, "épaule", 10, SEMI, SEA_D, "end") + text(22, 60, "mousse", 10, SEMI, SEA_D, "start")
    return s


def face(name, title, pts, notes, tube=False, section=None, extra=""):
    """notes: [(point index, label)] numbered along the line; legend under the wave."""
    s = text(16, 24, title, 13, BOLD, D, "start")
    body = wave(tube, section) + path(pts) + extra
    for i, (k, _) in enumerate(notes):
        x, y = pts[k]
        body += step(x, y, i + 1)
    s += f'<g transform="translate(0,14)">{body}</g>'
    y = 186
    for i, (_, label) in enumerate(notes):
        s += step(24, y - 4, i + 1) + text(40, y, label, 11, SEMI, D, "start")
        y += 22
    ILLUS[name] = card(y - 4, s)


def spray(x, y):
    return "".join(
        line([(x, y), (x + dx, y + dy)], Y, 3) for dx, dy in ((-8, -14), (0, -18), (9, -14), (15, -6))
    )


face("surf-bottom-turn-frontside", "Bottom turn frontside",
     [(84, 62), (110, 110), (150, 142), (200, 134), (228, 100)],
     [(1, "Descends la vague, regard vers l'épaule"), (2, "Compresse, appui orteils, épaules ouvertes"), (4, "Remonte vers la lèvre")])
face("surf-bottom-turn-backside", "Bottom turn backside",
     [(84, 62), (110, 110), (150, 142), (200, 134), (228, 100)],
     [(1, "Descends, regard par-dessus l'épaule"), (2, "Appui talons, buste qui tourne"), (4, "Remonte vers la lèvre")])
face("surf-top-turn", "Top turn",
     [(120, 140), (180, 118), (220, 92), (236, 96), (250, 124), (276, 142)],
     [(0, "Bottom turn, prends de la vitesse"), (2, "Pivote sous la lèvre"), (5, "Redescends vers le creux")])
face("surf-cutback", "Cutback",
     [(120, 120), (210, 112), (288, 124), (300, 140), (270, 146), (200, 136), (150, 126)],
     [(1, "Prends de la vitesse sur l'épaule"), (3, "Tourne, regard vers la mousse"), (6, "Reviens dans la partie puissante")])
face("surf-roundhouse-cutback", "Roundhouse cutback",
     [(130, 118), (230, 116), (296, 132), (270, 146), (180, 136), (100, 122), (94, 104), (130, 100), (190, 118)],
     [(2, "Cutback large"), (5, "Rebondis sur la mousse"), (8, "Change de rail et repars")])
face("surf-floater", "Floater",
     [(130, 142), (180, 120), (222, 92), (250, 94), (276, 104), (300, 140)],
     [(1, "Monte vers la section qui casse"), (3, "Glisse sur la lèvre, poids centré"), (5, "Redescends en amortissant")], section=(220, 282))
face("surf-re-entry", "Re-entry",
     [(140, 146), (190, 126), (218, 96), (226, 92), (214, 112), (204, 144)],
     [(1, "Bottom turn appuyé"), (3, "Frappe la lèvre quand elle casse"), (5, "Redescends avec elle")], section=(214, 240), extra=spray(226, 86))
face("surf-snap", "Snap",
     [(140, 146), (194, 124), (220, 94), (226, 90), (210, 116), (198, 144)],
     [(1, "Bottom turn vertical"), (3, "Virage sec en haut, jet d'eau"), (5, "Redescends vite")], extra=spray(226, 84))
face("surf-fin-release", "Fin release",
     [(140, 146), (194, 124), (220, 94), (230, 92), (214, 116), (200, 144)],
     [(1, "Monte vite vers la lèvre"), (3, "Pousse le tail : les dérives décrochent"), (5, "Rattrape et repars")], extra=spray(234, 86))
face("surf-carving-360", "Carving 360",
     [(110, 130), (180, 120), (230, 104), (250, 124), (226, 144), (196, 130), (210, 108), (270, 120)],
     [(1, "Prends de la vitesse"), (3, "Appui continu sur le rail"), (7, "Boucle complète, repars")])
face("surf-frontside-air", "Frontside air",
     [(140, 146), (196, 120), (222, 84), (240, 64), (262, 74), (276, 108), (292, 142)],
     [(1, "Vitesse max, vise une rampe"), (3, "Décolle de la lèvre, genoux serrés"), (5, "Réception centrée, jambes souples")])
face("surf-late-drop", "Late drop",
     [(104, 58), (108, 96), (120, 136), (160, 146), (210, 134)],
     [(0, "Pop-up rapide en haut de la vague"), (2, "Descends vertical, poids devant"), (4, "Bottom turn")])
face("surf-take-off-angle", "Take-off en angle",
     [(110, 62), (150, 92), (200, 112), (260, 122)],
     [(0, "Planche orientée 30-45° vers l'épaule"), (2, "Poids sur le rail côté vague"), (3, "Vise la partie non cassée")])
face("surf-trim", "Trim haut sur l'épaule",
     [(110, 82), (170, 90), (230, 104), (300, 122)],
     [(0, "Reste près de la lèvre"), (2, "Poids un peu en avant"), (3, "Là où la vague va le plus vite")])
face("surf-pumping", "Pumping",
     [(100, 110), (130, 92), (160, 120), (190, 100), (220, 128), (250, 108), (290, 130)],
     [(1, "Monte : détends les jambes"), (2, "Descends : compresse"), (6, "Garde le rythme de la vague")])
face("surf-tube", "Position de tube",
     [(118, 116), (96, 120), (60, 124), (30, 128)][::-1] + [(150, 128), (200, 132)],
     [(1, "Compact, genoux fléchis"), (3, "Main qui traîne pour freiner"), (5, "Regarde la sortie")], tube=True)
face("surf-sortir-du-tube", "Sortir du tube",
     [(40, 126), (80, 122), (120, 118), (170, 120), (230, 126)],
     [(0, "Regarde la sortie, pas la lèvre"), (2, "Pompe pour garder la vitesse"), (4, "Sors sur l'épaule")], tube=True)
face("surf-enchainer", "Enchaîner les lignes",
     [(90, 70), (130, 140), (190, 130), (224, 98), (250, 120), (296, 130), (284, 146), (230, 138)],
     [(1, "Bottom turn"), (3, "Top turn"), (6, "Cutback, et ainsi de suite")])
face("surf-combo-snap-floater", "Combo snap et floater",
     [(120, 146), (170, 124), (196, 88), (190, 112), (210, 140), (250, 120), (276, 100), (300, 104), (316, 140)],
     [(2, "Snap"), (4, "Bottom turn sans perdre de vitesse"), (7, "Floater sur la section")], section=(270, 316), extra=spray(198, 82))


# ---------- top views of the beach ----------


def beach(lines=(60, 92, 122), gap=None):
    s = f'<rect x="14" y="34" width="312" height="114" fill="{SEA}"/>'
    s += f'<rect x="14" y="148" width="312" height="30" fill="{SAND}"/>'
    for y in lines:
        if gap:
            s += line([(24, y), (gap[0], y + 3)], FOAM, 6) + line([(gap[1], y + 3), (316, y)], FOAM, 6)
        else:
            s += line([(24, y), (316, y)], FOAM, 6)
    return s + text(320, 172, "plage", 10, SEMI, D, "end") + text(320, 48, "large", 10, SEMI, SEA_D, "end")


def flag(x, y, color):
    return line([(x, y), (x, y - 22)], D, 2) + f'<polygon points="{x},{y - 22} {x + 14},{y - 17} {x},{y - 12}" fill="{color}"/>'


def surfer_dot(x, y, color=P, label=None):
    s = f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" stroke="{W}" stroke-width="2"/>'
    return s + (text(x, y - 11, label, 10, BOLD, D) if label else "")


def top(name, title, body, legend):
    s = text(16, 24, title, 13, BOLD, D, "start") + body
    y = 200
    for i, l in enumerate(legend):
        s += text(16, y + i * 18, l, 11, SEMI, D, "start")
    ILLUS[name] = card(y + 18 * len(legend) - 4, s)


top("surf-baines", "Lire la plage : la baïne",
    beach(gap=(140, 200)) + f'<rect x="140" y="34" width="60" height="114" fill="{SEA_D}" opacity="0.18"/>'
    + arrow(170, 140, 170, 60, O) + text(170, 50, "courant", 10, BOLD, O)
    + arrow(220, 80, 290, 80, P) + text(255, 72, "rame parallèle", 10, BOLD, P)
    + flag(70, 168, "#10B981") + flag(100, 168, "#EF4444") + text(85, 186, "zone surveillée", 10, SEMI, D),
    ["Eau plus sombre et calme, pas de vagues : c'est le chenal.", "Emporté ? Ne lutte pas, rame parallèle à la plage."])
top("surf-line-up", "Priorité au pic",
    beach(lines=(90,)) + line([(110, 70), (316, 90)], FOAM, 6) + f'<circle cx="110" cy="70" r="10" fill="{FOAM}"/>'
    + text(110, 56, "pic", 10, BOLD, SEA_D) + surfer_dot(132, 108, Y, "priorité") + surfer_dot(230, 112, P, "attends")
    + arrow(140, 118, 230, 132, Y) + line([(250, 100), (262, 112)], "#EF4444", 3) + line([(262, 100), (250, 112)], "#EF4444", 3),
    ["Le plus proche du pic a la priorité.", "Un surfeur par vague : ne pars jamais devant (drop-in)."])
top("surf-ramer-au-pic", "Ramer jusqu'au pic",
    beach(gap=(150, 210)) + path([(180, 160), (182, 110), (176, 60), (140, 42)], P, 3, "1 6")
    + surfer_dot(140, 42, Y, "") + text(108, 46, "line-up", 10, BOLD, D),
    ["Observe les séries 5 min, repère le chenal.", "Pars juste après la dernière vague d'une série."])
top("surf-passer-la-barre", "Passer la barre par gros jour",
    beach(lines=(54, 80, 106, 130), gap=(150, 210)) + path([(180, 160), (182, 110), (176, 60), (150, 40)], P, 3, "1 6")
    + text(240, 152, "chenal", 10, BOLD, SEA_D),
    ["Attends l'accalmie entre deux séries.", "Rame sans t'arrêter dans le chenal, duck dive si besoin."])


def mini_break(kind):
    s = f'<rect x="0" y="0" width="96" height="80" rx="8" fill="{SEA}"/>'
    if kind == "droite":
        s += line([(14, 44), (82, 52)], FOAM, 5) + f'<circle cx="14" cy="44" r="7" fill="{FOAM}"/>' + arrow(20, 62, 76, 68, O)
    elif kind == "gauche":
        s += line([(14, 52), (82, 44)], FOAM, 5) + f'<circle cx="82" cy="44" r="7" fill="{FOAM}"/>' + arrow(76, 62, 20, 68, O)
    else:
        s += line([(14, 48), (82, 48)], FOAM, 8) + line([(38, 60), (58, 72)], "#EF4444", 3) + line([(58, 60), (38, 72)], "#EF4444", 3)
    return s


top("surf-choisir-sa-vague", "Droite, gauche ou fermeture ?",
    "".join(f'<g transform="translate({16 + i * 106},40)">{mini_break(k)}</g>' + text(64 + i * 106, 138, l, 11, BOLD, D)
            for i, (k, l) in enumerate((("droite", "Droite"), ("gauche", "Gauche"), ("fermeture", "Fermeture")))),
    ["Vue depuis le line-up, face à la plage.", "Une vague qui casse d'un coup partout : laisse-la passer."])


def spot(kind):
    s = f'<rect x="0" y="0" width="96" height="86" rx="8" fill="{SEA}"/>'
    if kind == "beach":
        s += f'<rect x="0" y="62" width="96" height="24" rx="4" fill="{SAND}"/>' + line([(10, 40), (40, 42)], FOAM, 5) + line([(56, 30), (86, 34)], FOAM, 5)
    elif kind == "reef":
        s += f'<ellipse cx="48" cy="44" rx="26" ry="10" fill="#A78BFA" opacity="0.6"/>' + line([(26, 34), (72, 38)], FOAM, 5)
        s += f'<rect x="0" y="70" width="96" height="16" fill="{SAND}"/>'
    else:
        s += '<path d="M0,86 L0,20 Q30,26 46,86 Z" fill="#92400E" opacity="0.5"/>' + path([(36, 24), (54, 46), (70, 72)], FOAM, 5)
    return s


top("surf-reef-point-break", "Beach break, reef, point break",
    "".join(f'<g transform="translate({16 + i * 106},40)">{spot(k)}</g>' + text(64 + i * 106, 146, l, 11, BOLD, D)
            for i, (k, l) in enumerate((("beach", "Beach break"), ("reef", "Reef"), ("point", "Point break")))),
    ["Reef : chaussons, chute à plat, jamais les pieds au fond.", "Respecte strictement la priorité au pic."])
top("surf-mousse", "Glisser droit dans la mousse",
    beach(lines=(70, 110)) + path([(170, 100), (170, 150)], P, 3.5) + surfer_dot(170, 96, Y)
    + text(196, 128, "planche perpendiculaire", 10, BOLD, P, "start") + text(196, 142, "à la mousse", 10, BOLD, P, "start"),
    ["Pars juste devant la mousse, rame 3 coups de plus.", "Regard loin devant, poids centré."])
top("surf-virages-mousse", "Premiers virages dans la mousse",
    beach(lines=(70, 110)) + path([(170, 96), (130, 116), (200, 132), (150, 152)], P, 3.5) + surfer_dot(170, 96, Y)
    + text(214, 116, "regard et épaules", 10, BOLD, P, "start") + text(214, 130, "d'abord", 10, BOLD, P, "start"),
    ["Tourne la tête et les épaules du côté voulu.", "Garde les jambes fléchies pendant le virage."])
top("surf-surfskate-carving", "Surfskate : carving",
    f'<rect x="14" y="34" width="312" height="120" rx="6" fill="#E5E7EB"/>'
    + path([(30, 90), (80, 60), (130, 120), (180, 60), (230, 120), (300, 80)], P, 3.5)
    + text(80, 50, "buste", 10, BOLD, O) + text(130, 140, "compression", 10, BOLD, O),
    ["Génère la vitesse par la rotation du buste,", "sans pousser au pied. Frontside et backside."])


# ---------- sequences ----------


def lying(dx=0, chest=0):
    gy = 100
    s = f'<rect x="{6 + dx}" y="{gy}" width="88" height="8" rx="4" fill="{Y}"/>'
    s += line([(30 + dx, gy - 6), (72 + dx, gy - 6 - chest)], P, 11)
    s += line([(30 + dx, gy - 6), (8 + dx, gy - 4)])
    s += head(82 + dx, gy - 14 - chest, 8)
    return s


def popup_steps():
    gy = 100
    board = f'<rect x="6" y="{gy}" width="88" height="8" rx="4" fill="{Y}"/>'
    s1 = lying(chest=6) + line([(66, 88), (64, 100)])
    s2 = board + line([(34, 86), (74, 70)], P, 11) + line([(74, 70), (72, 98)]) + line([(34, 86), (40, 98)]) + head(84, 62, 8)
    s3 = board + line([(30, 98), (40, 76), (50, 56)]) + line([(70, 98), (62, 78), (50, 56)]) + line([(50, 56), (52, 34)], P, 11)
    s3 += line([(52, 40), (28, 46)]) + line([(52, 40), (78, 44)]) + head(56, 22, 8)
    return [(["Mains sous", "la poitrine"], s1), (["Pousse, pied", "arrière en travers"], s2 + arrow(26, 76, 40, 92, O)), (["Jambes fléchies,", "regard loin"], s3)]


ILLUS["surf-pop-up"] = panels(popup_steps())


def water(y=96):
    return f'<rect x="0" y="{y}" width="100" height="40" fill="{SEA}"/>' + line([(0, y), (100, y)], SEA_D, 2)


def turtle():
    s1 = water() + lying(chest=4) + f'<path d="M100,96 Q90,70 70,72 Q86,80 84,96 Z" fill="{FOAM}" stroke="{SEA_D}" stroke-width="1.5"/>'
    s2 = water() + f'<rect x="6" y="88" width="88" height="8" rx="4" fill="{Y}"/>' + line([(30, 108), (72, 110)], P, 11) + head(82, 112, 8)
    s2 += line([(66, 96), (66, 106)]) + line([(40, 96), (40, 106)]) + f'<path d="M60,88 Q50,60 20,66 Q40,72 40,88 Z" fill="{FOAM}" stroke="{SEA_D}" stroke-width="1.5"/>'
    s3 = water() + lying(chest=6) + arrow(10, 60, 80, 60, P)
    return panels([(["Rame face", "à la mousse"], s1), (["Retourne-toi sous", "la planche"], s2), (["Remonte et", "repars en ramant"], s3)])


ILLUS["surf-canard"] = turtle()


def duck():
    def b(x, y, a):
        return f'<rect x="{x - 40}" y="{y - 4}" width="80" height="8" rx="4" fill="{Y}" transform="rotate({a} {x} {y})"/>'

    s1 = water(70) + b(50, 72, 0) + line([(30, 64), (72, 62)], P, 11) + head(82, 56, 8) + arrow(20, 50, 70, 50, P)
    s2 = water(70) + b(50, 92, 20) + line([(40, 80), (70, 90)], P, 11) + line([(70, 90), (84, 100)]) + head(76, 78, 8) + arrow(84, 70, 90, 98, O)
    s3 = water(50) + b(50, 108, 0) + line([(30, 98), (72, 98)], P, 11) + head(82, 96, 8)
    s3 += f'<path d="M100,50 Q70,20 40,40 Q60,44 64,50 Z" fill="{FOAM}" stroke="{SEA_D}" stroke-width="1.5"/>'
    return panels([(["Rame vite", "vers la mousse"], s1), (["Bras tendus : enfonce", "le nose, puis le tail"], s2), (["Colle-toi à la planche,", "la vague passe"], s3)])


ILLUS["surf-duck-dive"] = duck()

ILLUS["surf-rame"] = panels([(
    ["Au centre, pieds joints, nose 2-3 cm hors de l'eau,", "bras profonds le long du rail"],
    f'<g transform="translate(-60,0) scale(1.4)">{water(70)}<rect x="6" y="66" width="88" height="8" rx="4" fill="{Y}" transform="rotate(-3 50 70)"/>'
    + line([(26, 60), (66, 56)], P, 11) + line([(26, 60), (8, 62)]) + head(76, 50, 8) + line([(64, 58), (60, 86)]) + "</g>"
    + arrow(110, 40, 150, 40, O),
)])


# ---------- swell, tide, breathing ----------

sw = f'<path d="M14,120 Q40,60 66,120 Q92,180 118,120 Q144,60 170,120 Q196,180 222,120 Q248,60 274,120 Q300,180 326,120" fill="none" stroke="{SEA_D}" stroke-width="3"/>'
sw += line([(40, 90), (40, 150)], O, 2) + text(46, 126, "hauteur", 10, BOLD, O, "start")
sw += line([(144, 80), (248, 80)], P, 2) + line([(144, 74), (144, 86)], P, 2) + line([(248, 74), (248, 86)], P, 2)
sw += text(196, 72, "période (s) : d'une crête à l'autre", 10, BOLD, P)
sw += arrow(240, 40, 310, 40, D) + text(250, 32, "direction", 10, SEMI, D, "start")
ILLUS["surf-houle"] = card(212, text(16, 24, "Lire la houle", 13, BOLD, D, "start") + sw
                           + text(16, 190, "Période > 10 s : houle puissante et organisée.", 11, SEMI, D, "start")
                           + text(16, 204, "Note hauteur, période, direction et vent.", 11, SEMI, D, "start"))

tide = f'<path d="M20,140 Q80,140 110,90 Q140,40 170,40 Q200,40 230,90 Q260,140 320,140" fill="none" stroke="{SEA_D}" stroke-width="3"/>'
tide += f'<rect x="96" y="40" width="50" height="104" fill="{Y}" opacity="0.25"/>' + text(121, 158, "montante", 10, BOLD, D)
tide += text(26, 132, "basse", 10, SEMI, P, "start") + text(170, 32, "haute", 10, SEMI, P) + text(314, 132, "basse", 10, SEMI, P, "end")
ILLUS["surf-maree"] = card(206, text(16, 24, "Le spot change avec la marée", 13, BOLD, D, "start") + tide
                           + text(16, 182, "Le pic se déplace et la forme des vagues change.", 11, SEMI, D, "start")
                           + text(16, 198, "Note heure et coefficient de tes meilleures sessions.", 11, SEMI, D, "start"))


def breath(name, title, blocks, foot):
    """blocks: [(minutes, 'apnee'|'respire', label)]"""
    x0, x1 = 16, 324
    tot = sum(b[0] for b in blocks)
    k = (x1 - x0) / tot
    s = text(16, 24, title, 13, BOLD, D, "start")
    x = x0
    for m, kind, lab in blocks:
        w = m * k
        h, c = (60, P) if kind == "apnee" else (26, "#DDD6FE")
        s += f'<rect x="{x + 1:.1f}" y="{110 - h}" width="{max(w - 2, 2):.1f}" height="{h}" rx="3" fill="{c}"/>'
        if lab:
            s += text(x + w / 2, 128, lab, 10, SEMI, D)
        x += w
    s += line([(x0, 110), (x1, 110)], D, 1.5)
    s += f'<rect x="16" y="142" width="12" height="12" rx="3" fill="{P}"/>' + text(34, 152, "apnée confortable, au sec", 11, SEMI, D, "start")
    s += f'<rect x="190" y="142" width="12" height="12" rx="3" fill="#DDD6FE"/>' + text(208, 152, "respiration calme", 11, SEMI, D, "start")
    s += text(16, 176, foot, 11, SEMI, D, "start")
    ILLUS[name] = card(190, s)


breath("surf-apnee", "Respiration et apnée au sec",
       [(2, "respire", "2′")] + rep(4, (1, "apnee", ""), (2, "respire", "2′")),
       "Toujours allongé au sol, jamais dans l'eau seul.")
breath("surf-table-co2", "Table CO2 au sec",
       [x for i, r in enumerate((2, 1.8, 1.6, 1.4, 1.2, 1)) for x in ((1, "apnee", ""), (r, "respire", f"{r:g}′".replace(".", ",")))] + [(3, "respire", "3′ calme")],
       "Même durée d'apnée, récupérations de 2′ à 1′.")

ILLUS["surf-fractionne-rame"] = profile(
    [("Échauf.", [(10, 2)]), ("10 × 20″ à fond / 40″", rep(10, (1 / 3, 5.5), (2 / 3, 1))), ("4 × 1′ / 1′", rep(4, (1, 4), (1, 1)))],
    title="Fractionné de rame")
ILLUS["surf-endurance-rame"] = profile(
    [("Échauf. 10′", [(10, 2)]), ("6 × 200 m crawl / 30″", rep(6, (4, 3), (0.5, 1)))], title="Endurance de rame (piscine)")
ILLUS["surf-recup-respiratoire"] = profile(
    [("8 × (30″ burpees / 1′30 respiration 3 s - 6 s)", rep(8, (0.5, 5), (1.5, 1)))], title="Récupération respiratoire")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for n, svg in ILLUS.items():
        open(os.path.join(here, n + ".svg"), "w").write(svg)
    print(len(ILLUS), "surf illustrations")
