"""Génère les médias du cahier de révisions : GIF en pixel art (chats, blocs
façon Minecraft) et petits sons de jeu. Tout est dessiné ici, sans fichier
externe.

    python3 outils/generer_medias.py
"""
import math
import random
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

RACINE = Path(__file__).resolve().parent.parent / "medias"
ECHELLE = 6          # 32 px dessinés -> 192 px
TAILLE = 32

# Palette
NOIR = (30, 26, 34)
BLANC = (250, 250, 245)
ROSE = (240, 130, 160)
ORANGE = (240, 150, 50)
ORANGE_F = (200, 105, 30)
CREME = (255, 220, 170)
GRIS = (150, 155, 165)
GRIS_F = (105, 110, 122)
GRIS_C = (205, 208, 215)
BLEU_L = (120, 190, 255)
OR = (255, 205, 40)
OR_F = (205, 145, 20)
CYAN = (90, 230, 230)
CYAN_F = (30, 160, 170)
BOIS = (160, 105, 55)
BOIS_F = (110, 70, 35)
ROUGE = (225, 50, 50)
ROUGE_F = (150, 25, 30)
CIEL = (170, 215, 255)
NUIT = (40, 45, 70)
VERT = (90, 190, 80)
VIOLET = (180, 140, 255)


def toile(fond):
    im = Image.new("RGB", (TAILLE, TAILLE), fond)
    return im, ImageDraw.Draw(im)


def r(d, x0, y0, x1, y1, c):
    """Rectangle plein, bornes incluses."""
    d.rectangle([x0, y0, x1, y1], fill=c)


def p(d, x, y, c):
    d.point((x, y), fill=c)


def note(d, x, y, c=NOIR):
    r(d, x, y + 3, x + 1, y + 4, c)
    r(d, x + 2, y, x + 2, y + 4, c)
    r(d, x + 3, y, x + 4, y, c)


def etincelle(d, x, y, c=BLANC):
    p(d, x, y, c)
    p(d, x - 1, y, c); p(d, x + 1, y, c); p(d, x, y - 1, c); p(d, x, y + 1, c)


def chat(d, dx=0, dy=0, poil=ORANGE, fonce=ORANGE_F, ventre=CREME, oreilles="hautes", queue=0, yeux="ouverts"):
    """Chat assis vu de face, coin haut gauche décalé de (dx, dy)."""
    X = lambda x: x + dx
    Y = lambda y: y + dy
    # queue
    if queue == 0:
        r(d, X(22), Y(24), X(25), Y(26), poil); r(d, X(24), Y(19), X(26), Y(24), poil); p(d, X(25), Y(18), fonce)
    else:
        r(d, X(22), Y(25), X(27), Y(27), poil); r(d, X(27), Y(21), X(28), Y(26), poil); p(d, X(28), Y(20), fonce)
    # corps
    r(d, X(10), Y(18), X(21), Y(28), poil)
    r(d, X(13), Y(20), X(18), Y(27), ventre)
    r(d, X(10), Y(29), X(13), Y(29), poil); r(d, X(18), Y(29), X(21), Y(29), poil)
    # oreilles
    if oreilles == "hautes":
        for i in range(3):
            r(d, X(8), Y(3 + i), X(8 + i), Y(3 + i), poil)
            r(d, X(23 - i), Y(3 + i), X(23), Y(3 + i), poil)
        p(d, X(9), Y(5), ROSE); p(d, X(22), Y(5), ROSE)
    else:  # oreilles basses (triste)
        r(d, X(5), Y(7), X(8), Y(8), poil); r(d, X(23), Y(7), X(26), Y(8), poil)
    # tête
    r(d, X(8), Y(6), X(23), Y(17), poil)
    r(d, X(12), Y(6), X(12), Y(8), fonce); r(d, X(15), Y(6), X(16), Y(8), fonce); r(d, X(19), Y(6), X(19), Y(8), fonce)
    # yeux
    if yeux == "ouverts":
        r(d, X(11), Y(10), X(12), Y(11), NOIR); r(d, X(19), Y(10), X(20), Y(11), NOIR)
        p(d, X(11), Y(10), BLANC); p(d, X(19), Y(10), BLANC)
    elif yeux == "contents":
        r(d, X(11), Y(11), X(12), Y(11), NOIR); p(d, X(10), Y(12), NOIR); p(d, X(13), Y(12), NOIR)
        r(d, X(19), Y(11), X(20), Y(11), NOIR); p(d, X(18), Y(12), NOIR); p(d, X(21), Y(12), NOIR)
    else:  # tristes
        r(d, X(11), Y(11), X(12), Y(12), NOIR); r(d, X(19), Y(11), X(20), Y(12), NOIR)
        p(d, X(10), Y(10), NOIR); p(d, X(21), Y(10), NOIR)
    # museau
    r(d, X(15), Y(13), X(16), Y(13), ROSE)
    if yeux == "tristes":
        p(d, X(14), Y(15), NOIR); p(d, X(17), Y(15), NOIR); r(d, X(15), Y(14), X(16), Y(14), NOIR)
    else:
        p(d, X(14), Y(14), NOIR); p(d, X(17), Y(14), NOIR); r(d, X(15), Y(15), X(16), Y(15), NOIR)
    # moustaches
    r(d, X(5), Y(13), X(8), Y(13), BLANC); r(d, X(23), Y(13), X(26), Y(13), BLANC)


def sauver_gif(nom, images, durees):
    grandes = [im.resize((TAILLE * ECHELLE, TAILLE * ECHELLE), Image.NEAREST) for im in images]
    if isinstance(durees, int):
        durees = [durees] * len(grandes)
    grandes[0].save(RACINE / "images" / nom, save_all=True, append_images=grandes[1:], duration=durees, loop=0, optimize=True)


# ---------------------------------------------------------------------------
# GIF
# ---------------------------------------------------------------------------
def gif_chat_danse():
    images = []
    pas = [(-2, 0, 0), (0, -1, 1), (2, 0, 0), (0, -1, 1)]
    for i, (dx, dy, q) in enumerate(pas * 2):
        im, d = toile(CIEL)
        r(d, 0, 30, 31, 31, VERT)
        chat(d, dx, dy, queue=q, yeux="contents" if i % 2 else "ouverts")
        note(d, 2 if i % 2 else 3, 4 + (i % 2), VIOLET)
        note(d, 26, 6 - (i % 2), VIOLET)
        images.append(im)
    sauver_gif("chat_danse.gif", images, 140)


def gif_chat_lunettes():
    images = []
    for i in range(10):
        im, d = toile((255, 230, 120))
        chat(d, 0, 1)
        y = min(-4 + i * 2, 10)
        r(d, 9, y, 22, y, NOIR)
        r(d, 10, y + 1, 14, y + 2, NOIR); r(d, 17, y + 1, 21, y + 2, NOIR)
        p(d, 11, y + 1, BLANC); p(d, 18, y + 1, BLANC)
        if i >= 7:
            etincelle(d, 4, 5); etincelle(d, 27, 4 if i % 2 else 6)
        images.append(im)
    sauver_gif("chat_lunettes.gif", images, [110] * 9 + [900])


def gif_chat_trophee():
    images = []
    for i in range(8):
        im, d = toile(NUIT)
        dy = -1 if i % 2 else 0
        chat(d, 0, 2, yeux="contents")
        # coupe tenue au-dessus de la tête
        r(d, 12, 0 + dy, 19, 0 + dy, OR_F)
        r(d, 12, 1 + dy, 19, 3 + dy, OR); r(d, 10, 1 + dy, 11, 2 + dy, OR); r(d, 20, 1 + dy, 21, 2 + dy, OR)
        r(d, 15, 4 + dy, 16, 5 + dy, OR_F)
        p(d, 13, 1 + dy, BLANC)
        for k, (x, y) in enumerate([(4, 4), (27, 3), (3, 20), (28, 18), (6, 12), (26, 11)]):
            if (i + k) % 3 == 0:
                etincelle(d, x, y, OR)
        images.append(im)
    sauver_gif("chat_trophee.gif", images, 150)


def gif_chat_triste():
    images = []
    for i in range(8):
        im, d = toile((190, 200, 220))
        chat(d, 0, 1, poil=GRIS, fonce=GRIS_F, ventre=GRIS_C, oreilles="basses", yeux="tristes")
        y = 14 + i
        if y < 22:
            r(d, 12, y, 12, y + 1, BLEU_L)
        # nuage de pluie
        r(d, 3, 2, 10, 4, GRIS_C); r(d, 5, 1, 8, 1, GRIS_C)
        p(d, 4 + (i % 3) * 2, 6 + (i % 2), BLEU_L)
        images.append(im)
    sauver_gif("chat_triste.gif", images, 160)


def bloc_pierre(d, x0, y0, taille=16, minerai=None, graine=1):
    alea = random.Random(graine)
    for y in range(taille):
        for x in range(taille):
            v = alea.choice([GRIS, GRIS, GRIS_F, GRIS_C])
            p(d, x0 + x, y0 + y, v)
    if minerai:
        for (x, y) in [(3, 3), (10, 4), (5, 10), (11, 11), (8, 7)]:
            r(d, x0 + x, y0 + y, x0 + x + 1, y0 + y + 1, minerai[0])
            p(d, x0 + x, y0 + y, minerai[1])


def pioche(d, x, y, angle):
    """Pioche en pixels ; angle 0 = levée, 1 = frappe."""
    if angle == 0:
        for k in range(8):
            p(d, x + k, y + 8 - k, BOIS); p(d, x + k + 1, y + 8 - k, BOIS_F)
        r(d, x + 4, y - 2, x + 11, y - 1, GRIS_C); r(d, x + 3, y - 1, x + 4, y + 1, GRIS_C); r(d, x + 11, y, x + 12, y + 1, GRIS_C)
    else:
        r(d, x, y + 4, x + 9, y + 5, BOIS); r(d, x, y + 6, x + 9, y + 6, BOIS_F)
        r(d, x + 9, y - 1, x + 10, y + 10, GRIS_C); p(d, x + 8, y - 1, GRIS_C); p(d, x + 8, y + 10, GRIS_C)


def diamant(d, x, y):
    r(d, x + 2, y, x + 5, y, CYAN)
    r(d, x + 1, y + 1, x + 6, y + 2, CYAN)
    r(d, x + 2, y + 3, x + 5, y + 3, CYAN_F)
    r(d, x + 3, y + 4, x + 4, y + 4, CYAN_F)
    p(d, x + 2, y + 1, BLANC)


def gif_bloc_diamant():
    images, durees = [], []
    fond = (60, 50, 70)
    for i in range(6):
        im, d = toile(fond)
        bloc_pierre(d, 8, 12, minerai=(CYAN, CYAN_F))
        for k in range(i // 2 + 1 if i else 0):  # fissures
            r(d, 10 + k * 4, 14 + k * 3, 11 + k * 4, 15 + k * 3, NOIR)
        pioche(d, 18, 2, i % 2)
        images.append(im); durees.append(130)
    for i in range(6):
        im, d = toile(fond)
        for k, (x, y) in enumerate([(9, 22), (22, 23), (12, 26), (20, 18)]):
            r(d, x - i // 2 + (k % 2) * i, y + i, x + 1 - i // 2 + (k % 2) * i, y + 1 + i, GRIS)
        diamant(d, 12, 12 - (i % 2))
        etincelle(d, 9, 9 if i % 2 else 11); etincelle(d, 23, 10 if i % 2 else 8)
        images.append(im); durees.append(150)
    sauver_gif("bloc_diamant.gif", images, durees)


def coeur(d, x, y, plein=True, clignote=False):
    c = BLANC if clignote else (ROUGE if plein else NOIR)
    f = ROUGE_F if plein and not clignote else (60, 55, 65)
    r(d, x + 1, y, x + 2, y, c); r(d, x + 4, y, x + 5, y, c)
    r(d, x, y + 1, x + 6, y + 2, c)
    r(d, x + 1, y + 3, x + 5, y + 3, f)
    r(d, x + 2, y + 4, x + 4, y + 4, f)
    p(d, x + 3, y + 5, f)
    if plein and not clignote:
        p(d, x + 1, y + 1, BLANC)


def gif_bloc_coeurs():
    images = []
    for i in range(8):
        im, d = toile((35, 30, 40))
        for k in range(4):
            x = 1 + k * 8
            if k < 3:
                coeur(d, x, 12)
            elif i < 5:
                coeur(d, x, 12, clignote=i % 2 == 1)
            else:
                coeur(d, x, 12, plein=False)
        if i >= 5:  # petite secousse « aïe »
            r(d, 26, 6, 27, 7, ROUGE); r(d, 29, 5, 30, 6, ROUGE)
        images.append(im)
    sauver_gif("bloc_coeurs.gif", images, [160] * 7 + [700])


def gif_bloc_coffre():
    images, durees = [], []
    for i in range(9):
        im, d = toile(NUIT)
        ouvert = min(i, 4)
        # rayons dorés
        if i >= 4:
            for k in range(5):
                x = 7 + k * 4 + (i % 2)
                r(d, x, 3, x, 13 - ouvert, OR)
        # corps du coffre
        r(d, 6, 17, 25, 28, BOIS); r(d, 6, 17, 25, 17, BOIS_F); r(d, 6, 28, 25, 28, BOIS_F)
        r(d, 6, 22, 25, 22, BOIS_F)
        # couvercle qui s'ouvre
        haut = 16 - ouvert * 2
        r(d, 6, haut - 3, 25, haut, BOIS); r(d, 6, haut - 3, 25, haut - 3, BOIS_F)
        r(d, 15, haut - 1, 16, haut + 2, OR)  # loquet
        if i >= 4:
            diamant(d, 9, 14 - (i % 2)); r(d, 17, 14, 22, 16, OR); p(d, 18, 14, BLANC)
            etincelle(d, 4, 6 if i % 2 else 8, OR); etincelle(d, 27, 7 if i % 2 else 5, OR)
        images.append(im); durees.append(140 if i < 8 else 600)
    sauver_gif("bloc_coffre.gif", images, durees)


# ---------------------------------------------------------------------------
# Sons
# ---------------------------------------------------------------------------
TAUX = 22050


def t(duree):
    return np.linspace(0, duree, int(TAUX * duree), endpoint=False)


def enveloppe(n, attaque=0.005, chute=4.0):
    x = np.arange(n) / TAUX
    env = np.exp(-chute * x)
    a = int(attaque * TAUX)
    if a:
        env[:a] *= np.linspace(0, 1, a)
    return env


def ton(freq, duree, forme="sinus", chute=6.0, volume=0.5):
    x = t(duree)
    if callable(freq):
        phase = 2 * np.pi * np.cumsum(freq(x)) / TAUX
    else:
        phase = 2 * np.pi * freq * x
    if forme == "sinus":
        s = np.sin(phase)
    elif forme == "carre":
        s = np.sign(np.sin(phase)) * 0.6
    else:  # dent de scie douce
        s = 2 * ((phase / (2 * np.pi)) % 1) - 1
        s = np.convolve(s, np.ones(6) / 6, mode="same")
    return s * enveloppe(len(x), chute=chute) * volume


def suite(*morceaux, ecart=0.0):
    sortie = []
    for m in morceaux:
        sortie.append(m)
        if ecart:
            sortie.append(np.zeros(int(ecart * TAUX)))
    return np.concatenate(sortie)


def sauver_son(nom, s):
    s = s / max(1e-9, np.max(np.abs(s))) * 0.8
    with wave.open(str(RACINE / "sons" / nom), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(TAUX)
        w.writeframes((s * 32767).astype(np.int16).tobytes())


def sons():
    sauver_son("ding.wav", suite(ton(1318.5, 0.09, chute=12), ton(1760, 0.45, chute=7)) + 0)
    sauver_son("xp.wav", suite(*[ton(f, 0.05, "carre", chute=20, volume=0.35) for f in (880, 1175, 1568, 2093)]))
    sauver_son("pop.wav", ton(lambda x: 300 + 1500 * np.exp(-x * 40), 0.12, chute=25))
    sauver_son("bonk.wav", ton(lambda x: 180 * np.exp(-x * 6) + 60, 0.35, chute=10) + 0.3 * np.random.default_rng(1).normal(0, 1, int(TAUX * 0.35)) * enveloppe(int(TAUX * 0.35), chute=40))
    vib = lambda base: (lambda x: base * (1 - 0.06 * x) + 6 * np.sin(2 * np.pi * 6 * x))
    sauver_son("womp.wav", suite(ton(vib(392), 0.3, "scie", chute=2), ton(vib(370), 0.3, "scie", chute=2), ton(vib(349), 0.75, "scie", chute=1.6), ecart=0.04))
    sauver_son("fanfare.wav", suite(*[ton(f, 0.11, "carre", chute=8, volume=0.4) for f in (523, 659, 784)], ton(1047, 0.6, "carre", chute=3, volume=0.4)))
    sauver_son("niveau.wav", suite(*[ton(f, 0.07, "carre", chute=10, volume=0.35) for f in (523, 659, 784, 1047, 1319, 1568)]))
    # miaou : son harmonique dont la hauteur monte puis descend, filtré « i » -> « ou »
    x = t(0.6)
    hauteur = 500 + 350 * np.sin(np.pi * np.clip(x / 0.6, 0, 1)) ** 1.5
    phase = 2 * np.pi * np.cumsum(hauteur) / TAUX
    s = sum(np.sin(k * phase) / k for k in range(1, 8))
    brillance = np.interp(x, [0, 0.25, 0.6], [1.0, 1.0, 0.25])
    s = s * (0.4 + 0.6 * brillance) + brillance * sum(np.sin(k * phase) / k for k in range(4, 8)) * 0.8
    env = np.interp(x, [0, 0.06, 0.45, 0.6], [0, 1, 0.8, 0])
    sauver_son("miaou.wav", s * env)


if __name__ == "__main__":
    (RACINE / "images").mkdir(parents=True, exist_ok=True)
    (RACINE / "sons").mkdir(parents=True, exist_ok=True)
    gif_chat_danse(); gif_chat_lunettes(); gif_chat_trophee(); gif_chat_triste()
    gif_bloc_diamant(); gif_bloc_coeurs(); gif_bloc_coffre()
    sons()
    print("Médias générés dans", RACINE)
