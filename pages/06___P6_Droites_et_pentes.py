"""Série P6 — Droites, pentes et fonctions affines."""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P6 | Droites et pentes", page_icon="📐", layout="wide")

x = sp.Symbol("x")

st.title("📐 P6 — Droites et pentes")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer la **pente** d'une droite à partir de deux points, retrouver son ordonnée à
l'origine, l'utiliser pour prévoir une valeur, et trouver l'intersection de deux
droites — c'est-à-dire un seuil.

### 🧠 Ce que la pente veut dire
La pente n'est pas une propriété géométrique abstraite : c'est **de combien $y$ varie
quand $x$ augmente d'une unité**. Cette lecture, avec son unité et son signe, est la
seule chose à retenir — et c'est elle qui deviendra la dérivée au semestre.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 6")
    st.markdown("**Fonction affine**")
    st.latex(r"y = ax + b")
    st.markdown("$a$ : pente (coefficient directeur) · $b$ : ordonnée à l'origine")
    st.markdown("**Pente entre deux points**")
    st.latex(r"a = \frac{y_B - y_A}{x_B - x_A}")
    st.markdown("**Ordonnée à l'origine**")
    st.latex(r"b = y_A - a\,x_A")
    st.info(
        "**La lecture qui compte**\n\n"
        "Quand $x$ augmente de 1, $y$ varie de $a$.\n\n"
        "$a > 0$ : croissante · $a < 0$ : décroissante · $a = 0$ : constante"
    )

SITUATIONS = [
    ("le coût de fonctionnement d'un équipement", "usagers", "€"),
    ("la dépense de chauffage d'un bâtiment", "m²", "€"),
    ("le temps de traitement d'un dossier", "pièces jointes", "minutes"),
    ("la consommation d'eau d'un service", "agents", "litres"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Pente entre deux points --------------------------------------------


def gen_pente() -> Exercice:
    xa = random.choice([0, 1, 2, 3, 4, 5])
    xb = xa + random.choice([2, 3, 4, 5, 8])
    a = random.choice([Fraction(-3), Fraction(-2), Fraction(-1, 2), Fraction(1, 2),
                       Fraction(3, 2), Fraction(2), Fraction(3), Fraction(5, 2)])
    b = random.choice([-6, -2, 0, 3, 5, 8])
    ya = a * xa + b
    yb = a * xb + b
    reponse = float(a)

    enonce = f"""
> Une droite passe par les deux points suivants :
>
> $$ A\\,({xa}\\;;\\;{sp.latex(sp.Rational(ya))}) \\qquad
>    B\\,({xb}\\;;\\;{sp.latex(sp.Rational(yb))}) $$
>
> Calculez sa **pente** (coefficient directeur).
"""

    etapes = [
        Etape(
            "Identifier — la pente est un rapport de variations",
            "La pente compare la variation verticale à la variation horizontale entre "
            "deux points. L'ordre des points n'a pas d'importance, **à condition de "
            "garder le même ordre** au numérateur et au dénominateur.",
        ),
        Etape(
            "Calculer les deux variations",
            f"Variation verticale : ${sp.latex(sp.Rational(yb))} - "
            f"{sp.latex(sp.Rational(ya))} = {sp.latex(sp.Rational(yb - ya))}$. "
            f"Variation horizontale : ${xb} - {xa} = {xb - xa}$.",
            rf"a = \frac{{y_B - y_A}}{{x_B - x_A}} = "
            rf"\frac{{{sp.latex(sp.Rational(yb - ya))}}}{{{xb - xa}}} "
            rf"= {sp.latex(sp.Rational(a))}",
        ),
        Etape(
            "Vérifier — le signe correspond-il au dessin ?",
            f"En passant de $A$ à $B$, $x$ augmente et $y$ "
            f"{'augmente' if yb > ya else 'diminue' if yb < ya else 'ne bouge pas'}. "
            f"La pente doit donc être "
            f"{'positive' if a > 0 else 'négative' if a < 0 else 'nulle'} : "
            f"c'est bien le cas (${sp.latex(sp.Rational(a))}$). ✓",
        ),
        Etape(
            "Interpréter",
            f"Concrètement : chaque fois que $x$ augmente de 1, $y$ "
            f"{'augmente' if a > 0 else 'diminue'} de "
            f"${sp.latex(sp.Rational(abs(a)))}$. C'est cette phrase — pas la formule — "
            "qu'il faut savoir produire, et c'est exactement ce que dira la dérivée "
            "au semestre, pour des courbes qui ne sont plus des droites.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Pente a",
        tolerance=1e-6,
        indice="Variation de $y$ divisée par variation de $x$, dans le même ordre.",
        pieges=[
            (float(xb - xa) / float(yb - ya) if yb != ya else 0.0,
             "Vous avez inversé le rapport : la variation de $y$ va au **numérateur**."),
            (float(yb - ya),
             "C'est la variation verticale seule. Il reste à la rapporter à la "
             "variation horizontale."),
            (-reponse,
             "Erreur de signe : vérifiez que vous avez soustrait dans le même ordre "
             "en haut et en bas."),
        ],
    )


# --- 2. Ordonnée à l'origine ------------------------------------------------


def gen_ordonnee() -> Exercice:
    a = random.choice([-4, -3, -2, 2, 3, 4, 5])
    b = random.choice([-10, -6, -3, 4, 7, 12])
    xa = random.choice([2, 3, 4, 5, 6])
    ya = a * xa + b
    reponse = float(b)

    enonce = f"""
> Une droite a pour pente **$a = {a}$** et passe par le point
> $A\\,({xa}\\;;\\;{ya})$.
>
> Quelle est son **ordonnée à l'origine** $b$ ?
"""

    etapes = [
        Etape(
            "Identifier — écrire ce qu'on sait",
            "Toute droite non verticale s'écrit $y = ax + b$. La pente est connue, "
            "et le point $A$ appartient à la droite : ses coordonnées vérifient donc "
            "l'équation.",
            rf"{ya} = {a} \times {xa} + b",
        ),
        Etape(
            "Calculer — isoler $b$",
            f"${a} \\times {xa} = {a*xa}$, qu'il reste à retrancher des deux côtés.",
            rf"b = {ya} - ({a*xa}) = {b}",
        ),
        Etape(
            "Vérifier — l'équation complète redonne-t-elle le point ?",
            f"La droite est $y = {sp.latex(a*x + b)}$. Pour $x = {xa}$ : "
            f"${a} \\times {xa} + ({b}) = {ya}$. ✓ On retombe bien sur $A$.",
        ),
        Etape(
            "Interpréter",
            f"L'ordonnée à l'origine est la valeur de $y$ **quand $x$ vaut 0**. "
            "Dans un modèle de coût, c'est le coût fixe : ce qu'on paie avant même "
            "de produire quoi que ce soit. Les deux paramètres d'une droite ont donc "
            "chacun une signification concrète — la pente, un coût unitaire ; "
            "l'ordonnée, un coût fixe.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Ordonnée à l'origine b",
        tolerance=1e-6,
        indice="Le point appartient à la droite : ses coordonnées vérifient "
        "$y = ax + b$.",
        pieges=[
            (float(ya + a * xa),
             "Erreur de signe : il faut **retrancher** $a x_A$, pas l'ajouter."),
            (float(ya),
             "Vous avez donné l'ordonnée du point $A$, pas celle de l'origine. "
             "Elles ne coïncident que si $x_A = 0$."),
        ],
    )


# --- 3. Prévoir une valeur --------------------------------------------------


def gen_prevision() -> Exercice:
    situation, unite_x, unite_y = random.choice(SITUATIONS)
    a = random.choice([2, 3, 4, 5, 8, 12])
    b = random.choice([50, 80, 120, 200, 350])
    x0 = random.choice([15, 20, 25, 30, 40, 50])
    reponse = a * x0 + b

    enonce = f"""
> On modélise {situation} par la relation
>
> $$ y = {sp.latex(a*x + b)} $$
>
> où $x$ est le nombre de {unite_x} et $y$ la valeur en {unite_y}.
>
> Que vaut $y$ pour **{x0} {unite_x}** ?
"""

    etapes = [
        Etape(
            "Identifier — lire le modèle avant de calculer",
            f"Le modèle contient deux informations : une partie fixe de **{b} "
            f"{unite_y}**, présente même sans aucun {unite_x[:-1]}, et une partie "
            f"variable de **{a} {unite_y} par {unite_x[:-1]}**.",
        ),
        Etape(
            "Calculer — substituer",
            "",
            rf"y = {a} \times {x0} + {b} = {a*x0} + {b} = {reponse}",
        ),
        Etape(
            "Vérifier — l'encadrement par la partie fixe",
            f"Le résultat doit être supérieur à {b} (la partie fixe) et cohérent avec "
            f"la pente : passer de 0 à {x0} {unite_x} ajoute "
            f"${a} \\times {x0} = {a*x0}$ {unite_y}. ✓",
        ),
        Etape(
            "Interpréter",
            f"Attention à la portée du modèle : il est linéaire, donc il suppose que "
            f"chaque {unite_x[:-1]} supplémentaire coûte toujours exactement {a} "
            f"{unite_y}. C'est une **hypothèse**, rarement vraie aux extrêmes. "
            "Le semestre servira précisément à traiter les cas où elle tombe.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(reponse),
        etapes=etapes,
        libelle=f"Valeur de y ({unite_y})",
        tolerance=1e-6,
        indice="Remplacez $x$ par sa valeur, sans oublier la partie fixe.",
        pieges=[
            (float(a * x0),
             "Vous avez oublié la partie fixe : le modèle vaut déjà "
             f"{b} {unite_y} pour $x = 0$."),
            (float((a + b) * x0),
             "Vous avez multiplié toute l'expression par $x$. Seul le terme en $a$ "
             "dépend de $x$ ; $b$ est une constante."),
        ],
    )


# --- 4. Intersection de deux droites ---------------------------------------


def gen_intersection() -> Exercice:
    sol = random.choice([2, 3, 4, 5, 6, 8, 10])
    a1 = random.choice([2, 3, 4, 6])
    a2 = a1 + random.choice([1, 2, 3, 4])
    b2 = random.choice([0, 5, 10])
    b1 = (a2 - a1) * sol + b2

    enonce = f"""
> Deux droites ont pour équations :
>
> $$ y_1 = {sp.latex(a1*x + b1)} \\qquad\\qquad y_2 = {sp.latex(a2*x + b2)} $$
>
> Pour quelle valeur de $x$ se **coupent-elles** ?
"""

    etapes = [
        Etape(
            "Identifier — se couper, c'est avoir la même valeur",
            "Au point d'intersection, les deux droites donnent le même $y$ pour le "
            "même $x$. Chercher l'intersection revient donc à résoudre une équation.",
            rf"{sp.latex(a1*x + b1)} = {sp.latex(a2*x + b2)}",
        ),
        Etape(
            "Résoudre",
            f"On rassemble les $x$ d'un côté : ${a2}x - {a1}x = {a2 - a1}x$.",
            rf"{b1 - b2} = {a2 - a1}x \iff x = \frac{{{b1 - b2}}}{{{a2 - a1}}} = {sol}",
        ),
        Etape(
            "Vérifier — les deux droites donnent-elles le même $y$ ?",
            f"$y_1({sol}) = {a1} \\times {sol} + {b1} = {a1*sol + b1}$ et "
            f"$y_2({sol}) = {a2} \\times {sol} + {b2} = {a2*sol + b2}$. "
            "Identiques. ✓ Sans cette vérification, une erreur de signe passe "
            "inaperçue.",
        ),
        Etape(
            "Interpréter — le point de bascule",
            f"Avant $x = {sol}$, la droite de plus faible pente (celle de coefficient "
            f"${a1}$) est au-dessus ; après, c'est l'autre qui la dépasse. "
            "Ce croisement est la forme géométrique du seuil de bascule entre deux "
            "dispositifs — la même question qu'en séance 4, vue autrement.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="Abscisse du point d'intersection",
        tolerance=1e-6,
        indice="Deux droites se coupent là où leurs équations donnent le même $y$.",
        pieges=[
            (float(b1 + b2) / (a1 + a2),
             "Vous avez additionné au lieu de soustraire. On cherche l'**égalité** "
             "des deux expressions, donc l'annulation de leur différence."),
            (float(b1 - b2) / (a1 + a2),
             "Le dénominateur est l'**écart** entre les deux pentes, pas leur somme."),
        ],
    )


# --- 5. Interpréter une pente (QCM) ----------------------------------------


def gen_interpretation() -> Exercice:
    situation, unite_x, unite_y = random.choice(SITUATIONS)
    a = random.choice([-8, -5, -3, 2, 4, 7])
    b = random.choice([60, 100, 180, 250])
    sens = "augmente" if a > 0 else "diminue"

    bonne = (
        f"Chaque {unite_x[:-1]} supplémentaire fait {sens} y de {abs(a)} {unite_y}."
    )
    options = [
        bonne,
        f"y vaut {abs(a)} {unite_y} en moyenne par {unite_x[:-1]}.",
        f"Quand y augmente de 1 {unite_y}, x {sens} de {abs(a)} {unite_x}.",
        f"y vaut {b} {unite_y} quand x augmente de 1 {unite_x[:-1]}.",
    ]
    random.shuffle(options)

    enonce = f"""
> On modélise {situation} par
>
> $$ y = {sp.latex(a*x + b)} $$
>
> où $x$ est le nombre de {unite_x} et $y$ la valeur en {unite_y}.
>
> Quelle est la bonne **interprétation de la pente** ?
"""

    etapes = [
        Etape(
            "Identifier — la pente répond à une question précise",
            "« De combien $y$ varie-t-il quand $x$ augmente d'une unité ? » "
            "Ni une moyenne, ni une valeur de $y$ : une **variation**, avec une "
            "unité composée.",
        ),
        Etape(
            "Calculer — vérifier sur deux valeurs",
            f"Pour $x = 10$ : $y = {a*10 + b}$. Pour $x = 11$ : $y = {a*11 + b}$. "
            f"L'écart vaut exactement ${a}$, quel que soit le point de départ choisi. "
            "C'est ce qui caractérise une droite.",
        ),
        Etape(
            "Vérifier — l'unité de la pente",
            f"La pente s'exprime en **{unite_y} par {unite_x[:-1]}**. "
            "Une interprétation qui ne mentionne pas les deux unités est "
            "nécessairement incomplète, et souvent fausse.",
        ),
        Etape(
            "Interpréter — ne pas confondre niveau et variation",
            f"L'ordonnée à l'origine ({b} {unite_y}) est un **niveau** ; la pente "
            f"({a}) est une **variation**. Confondre les deux est l'erreur "
            "d'interprétation la plus coûteuse de tout le cours — elle reviendra "
            "à l'identique avec la dérivée.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation",
        indice="La pente décrit une variation, pas un niveau. Et elle porte deux unités.",
        pieges=[
            (f"y vaut {abs(a)} {unite_y} en moyenne par {unite_x[:-1]}.",
             "Vous confondez la pente avec une moyenne. La pente est une **variation**, "
             "pas un niveau moyen."),
            (f"y vaut {b} {unite_y} quand x augmente de 1 {unite_x[:-1]}.",
             f"{b} est l'ordonnée à l'origine : la valeur de $y$ quand $x = 0$. "
             "Ce n'est pas la pente."),
            (f"Quand y augmente de 1 {unite_y}, x {sens} de {abs(a)} {unite_x}.",
             "Vous avez inversé les rôles de $x$ et de $y$. La pente se lit toujours "
             "« variation de $y$ pour une unité de $x$ »."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Calculer une pente",
        "2️⃣ Ordonnée à l'origine",
        "3️⃣ Prévoir une valeur",
        "4️⃣ Intersection",
        "5️⃣ Interpréter la pente",
    ]
)

with onglets[0]:
    st.subheader("La pente à partir de deux points")
    executer("p6_pente", gen_pente)

with onglets[1]:
    st.subheader("Retrouver l'ordonnée à l'origine")
    executer("p6_ordonnee", gen_ordonnee)

with onglets[2]:
    st.subheader("Utiliser le modèle pour prévoir")
    executer("p6_prevision", gen_prevision)

with onglets[3]:
    st.subheader("Où deux droites se croisent-elles ?")
    executer("p6_intersection", gen_intersection)

with onglets[4]:
    st.subheader("Que dit la pente, exactement ?")
    executer("p6_interpretation", gen_interpretation)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°6 — Droites et pentes · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
