"""Série P6 — Fonctions et fonctions affines. Fil rouge C : le logement étudiant."""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P6 | Fonctions affines", page_icon="📐", layout="wide")

x, p_ = sp.symbols("x p")

st.title("📐 P6 — Fonctions et fonctions affines")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Distinguer **image** et **antécédent**, calculer et interpréter une **pente**,
trouver un **équilibre** entre offre et demande, et lire le **signe d'un produit de
fonctions affines**.

### 🧠 La lecture qui compte
Une pente n'est pas un objet géométrique abstrait : c'est **de combien $y$ varie
quand $x$ augmente d'une unité**, avec ses unités. Cette phrase deviendra la dérivée
au semestre.

### 🏠 Fil rouge C — Le marché du logement étudiant
Au loyer $p$ (en euros), les étudiants demandent $D(p) = 4\\,000 - 4p$ logements et
les propriétaires en offrent $O(p) = 200 + 2p$.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 6")
    st.markdown("**Fonction affine**")
    st.latex(r"f(x) = ax + b")
    st.markdown("$a$ : pente · $b$ : ordonnée à l'origine")
    st.markdown("**Pente à partir de deux points**")
    st.latex(r"a = \frac{f(x_B) - f(x_A)}{x_B - x_A}")
    st.markdown("**Image et antécédent**")
    st.markdown(
        "**Image** de $x$ : on remplace, c'est direct.\n\n"
        "**Antécédent** de $y$ : on résout une équation."
    )
    st.info(
        "**Interpréter la pente — toujours avec ses unités**\n\n"
        "« Si le loyer augmente de 1 €, 4 logements de moins sont demandés. »"
    )
    st.error(
        "**Signe et variations : deux lectures différentes**\n\n"
        "Le **signe** dit si $f(x)$ est au-dessus ou en dessous de zéro.\n\n"
        "Les **variations** disent si $f$ monte ou descend."
    )

SITUATIONS = [
    ("le coût de fonctionnement d'un équipement", "usagers", "€"),
    ("la dépense de chauffage d'un bâtiment", "m²", "€"),
    ("le temps de traitement d'un dossier", "pièces jointes", "minutes"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Image et antécédent -------------------------------------------------


def gen_image_antecedent() -> Exercice:
    a = random.choice([-5, -3, -2, 2, 3, 4, 6])
    b = random.choice([-12, -7, 5, 10, 18])
    f = a * x + b
    demande_image = random.choice([True, False])

    if demande_image:
        x0 = random.choice([-3, -2, 2, 3, 5, 7])
        reponse = float(f.subs(x, x0))
        question = f"Calculez l'**image** de ${x0}$ par $f$, c'est-à-dire $f({x0})$."
        libelle = f"f({x0}) ="
        calcul = rf"f({x0}) = {a} \times ({x0}) + ({b}) = {reponse:.0f}"
        commentaire = (
            "Calculer une image est une **substitution** : on remplace $x$ par la "
            "valeur donnée, sans rien résoudre."
        )
        pieges = [
            (float(Fraction(x0 - b, a)),
             "Vous avez cherché un **antécédent** : vous avez résolu une équation là "
             "où une simple substitution suffisait."),
        ]
        interpretation = (
            f"$f({x0}) = {reponse:.0f}$ signifie que le point "
            f"$({x0}\\,;\\,{reponse:.0f})$ appartient à la droite. Image et point de "
            "la courbe sont deux façons de dire la même chose."
        )
    else:
        sol = random.choice([-3, -1, 2, 4, 6])
        k = a * sol + b
        reponse = float(sol)
        question = (
            f"Quel est l'**antécédent** de ${k}$ par $f$ ? Autrement dit, pour quelle "
            f"valeur de $x$ a-t-on $f(x) = {k}$ ?"
        )
        libelle = "x ="
        calcul = (
            rf"{a}x + ({b}) = {k} \iff {a}x = {k - b} \iff "
            rf"x = \frac{{{k - b}}}{{{a}}} = {sol}"
        )
        commentaire = (
            "Chercher un antécédent, c'est **résoudre une équation** — le chemin "
            "inverse de l'image. C'est exactement la séance 3."
        )
        pieges = [
            (float(f.subs(x, k)),
             "Vous avez calculé l'**image** de la valeur donnée. Image et antécédent "
             "vont en sens inverse."),
            (float(k + b) / a,
             "Erreur de signe : on retranche $b$ des deux membres."),
        ]
        interpretation = (
            f"L'antécédent est unique ici parce que la fonction est affine et que sa "
            f"pente ${a}$ n'est pas nulle. Au semestre, avec une parabole, une même "
            "image pourra avoir deux antécédents — ou aucun."
        )

    enonce = f"""
> Soit la fonction affine $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> {question}
"""

    etapes = [
        Etape(
            "Identifier — image ou antécédent ?",
            "C'est la distinction à faire **avant** tout calcul. Une image se calcule, "
            "un antécédent se cherche. Les confondre revient à résoudre le problème "
            "inverse de celui qui est posé.",
        ),
        Etape("Calculer", commentaire, calcul),
        Etape(
            "Vérifier",
            "Dans les deux cas, le contrôle est le même : le couple obtenu "
            "doit satisfaire l'équation de la droite. Dix secondes, et la question "
            "est close.",
        ),
        Etape("Interpréter", interpretation),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=libelle,
        tolerance=1e-6,
        indice="Image : on remplace. Antécédent : on résout.",
        pieges=pieges,
    )


# --- 2. Pente et interprétation --------------------------------------------


def gen_pente() -> Exercice:
    situation, unite_x, unite_y = random.choice(SITUATIONS)
    xa = random.choice([0, 5, 10, 20])
    xb = xa + random.choice([5, 10, 15, 20])
    a = random.choice([-4, -3, -2, 2, 3, 5, 8])
    b = random.choice([40, 80, 150, 300])
    ya = a * xa + b
    yb = a * xb + b
    reponse = float(a)

    enonce = f"""
> On modélise {situation} par une fonction affine. On dispose de deux relevés :
>
> - pour **{xa} {unite_x}** : **{ya} {unite_y}**
> - pour **{xb} {unite_x}** : **{yb} {unite_y}**
>
> Calculez la **pente** de cette fonction.
"""

    etapes = [
        Etape(
            "Identifier — la pente est un rapport de variations",
            "Elle compare la variation verticale à la variation horizontale. "
            "L'ordre des deux points est libre, **à condition** de garder le même "
            "ordre en haut et en bas.",
        ),
        Etape(
            "Calculer",
            f"Variation verticale : ${yb} - {ya} = {yb - ya}$ {unite_y}. "
            f"Variation horizontale : ${xb} - {xa} = {xb - xa}$ {unite_x}.",
            rf"a = \frac{{{yb} - {ya}}}{{{xb} - {xa}}} = "
            rf"\frac{{{yb - ya}}}{{{xb - xa}}} = {reponse:.4g}",
        ),
        Etape(
            "Vérifier — le signe correspond-il aux données ?",
            f"Quand $x$ augmente, $y$ "
            f"{'augmente' if yb > ya else 'diminue'} : la pente doit donc être "
            f"{'positive' if a > 0 else 'négative'}. ✓",
        ),
        Etape(
            "Interpréter — toujours avec les unités",
            f"Chaque {unite_x[:-1]} supplémentaire fait "
            f"{'augmenter' if a > 0 else 'diminuer'} {situation} de "
            f"${abs(reponse):.4g}$ {unite_y}. C'est **cette phrase** — et non le "
            "nombre seul — qui constitue la réponse attendue à l'examen. "
            "Une pente sans unités n'est pas interprétable.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Pente",
        tolerance=1e-6,
        indice="Variation de $y$ divisée par variation de $x$, dans le même ordre.",
        pieges=[
            (float(xb - xa) / (yb - ya) if yb != ya else 0.0,
             "Vous avez inversé le rapport : la variation de $y$ va au **numérateur**."),
            (float(yb - ya),
             "C'est la variation verticale seule : il reste à la rapporter à la "
             "variation horizontale."),
            (-reponse,
             "Erreur de signe : vérifiez que vous avez soustrait dans le même ordre "
             "en haut et en bas."),
        ],
    )


# --- 3. Équilibre offre / demande (fil rouge) ------------------------------


def gen_equilibre() -> Exercice:
    # D(p) = d0 - d1 p ; O(p) = o0 + o1 p, choisis pour un équilibre entier
    d1 = random.choice([3, 4, 5, 6])
    o1 = random.choice([1, 2, 3])
    p_eq = random.choice([300, 400, 500, 600, 625])
    o0 = random.choice([100, 200, 300])
    d0 = o0 + (d1 + o1) * p_eq
    reponse = float(p_eq)

    enonce = f"""
> **Logement étudiant.** Au loyer $p$ (en euros) :
>
> - les étudiants demandent $D(p) = {d0:,} - {d1}p$ logements ;
> - les propriétaires en offrent $O(p) = {o0} + {o1}p$.
>
> Quel est le **loyer d'équilibre**, celui pour lequel offre et demande coïncident ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — l'équilibre est une égalité",
            "Le marché est à l'équilibre quand la quantité demandée égale la quantité "
            "offerte. Chercher l'équilibre revient donc à résoudre une équation du "
            "premier degré — exactement la séance 3.",
            rf"D(p) = O(p) \iff {d0} - {d1}p = {o0} + {o1}p",
        ),
        Etape(
            "Résoudre",
            f"On rassemble les termes en $p$ d'un côté : "
            f"${d1}p + {o1}p = {d1 + o1}p$.",
            rf"{d0} - {o0} = {d1 + o1}p \iff p = \frac{{{d0 - o0}}}{{{d1 + o1}}} "
            rf"= {p_eq}\ \text{{€}}",
        ),
        Etape(
            "Vérifier — les deux quantités coïncident-elles ?",
            f"$D({p_eq}) = {d0} - {d1} \\times {p_eq} = {d0 - d1*p_eq}$ logements et "
            f"$O({p_eq}) = {o0} + {o1} \\times {p_eq} = {o0 + o1*p_eq}$ logements. "
            "Identiques. ✓ Vérifier une seule des deux ne prouverait rien.",
        ),
        Etape(
            "Interpréter — lire les deux pentes",
            f"La pente de la demande est $-{d1}$ : si le loyer augmente de 1 €, "
            f"{d1} logements de moins sont demandés. Celle de l'offre est $+{o1}$ : "
            f"{o1} logements de plus sont mis sur le marché. "
            f"Au loyer de {p_eq} €, {d0 - d1*p_eq} logements changent de mains — "
            "au-dessus, des logements restent vacants ; en dessous, des étudiants "
            "ne trouvent rien.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Loyer d'équilibre",
        unite="€",
        tolerance=1e-6,
        indice="Offre égale demande : une équation du premier degré.",
        pieges=[
            (float(d0 - o0) / (d1 - o1) if d1 != o1 else 0.0,
             "Les deux pentes se **soustraient** dans l'équation, donc leurs valeurs "
             f"absolues s'**additionnent** : ${d1} + {o1} = {d1 + o1}$ au "
             "dénominateur."),
            (float(d0 - d1 * p_eq),
             "C'est la **quantité** échangée à l'équilibre, pas le loyer. "
             "L'énoncé demande un prix, en euros."),
            (float(d0 + o0) / (d1 + o1),
             "Les deux constantes se soustraient, elles ne s'additionnent pas."),
        ],
    )


# --- 4. Signe d'un produit de fonctions affines (QCM) ----------------------


def gen_signe_produit() -> Exercice:
    a1 = random.choice([1, 2, 3])
    r1 = random.choice([-4, -2, 1, 3])
    a2 = random.choice([-1, -2, -3])
    r2 = r1 + random.choice([2, 3, 5])
    # f(x) = a1(x - r1) * a2(x - r2)
    f = sp.expand(a1 * (x - r1) * a2 * (x - r2))

    # a1 > 0 et a2 < 0 : produit négatif à l'extérieur, positif entre les racines
    bonne = f"f(x) > 0 sur ]{r1} ; {r2}[ et f(x) < 0 à l'extérieur"
    options = [
        bonne,
        f"f(x) < 0 sur ]{r1} ; {r2}[ et f(x) > 0 à l'extérieur",
        f"f(x) > 0 pour tout x sauf en {r1} et {r2}",
        f"f(x) a le même signe que x sur tout l'axe",
    ]
    random.shuffle(options)

    enonce = f"""
> Soit la fonction produit
>
> $$ f(x) = {a1}(x - ({r1})) \\times {a2}(x - ({r2})) $$
>
> Quel est le **signe** de $f(x)$ selon les valeurs de $x$ ?
"""

    test_gauche = float(f.subs(x, r1 - 1))
    test_milieu = float(f.subs(x, (r1 + r2) / 2))
    test_droite = float(f.subs(x, r2 + 1))

    etapes = [
        Etape(
            "Identifier — surtout ne pas développer",
            "La forme factorisée donne les **racines** immédiatement : "
            f"$x = {r1}$ et $x = {r2}$. Ce sont les seuls points où $f$ peut changer "
            "de signe, car un produit ne change de signe que si l'un de ses facteurs "
            "en change.",
        ),
        Etape(
            "Étudier le signe de chaque facteur",
            f"Le premier facteur, de pente ${a1}$ (positive), est négatif avant "
            f"${r1}$ et positif après. Le second, de pente ${a2}$ (négative), fait "
            f"l'inverse autour de ${r2}$. Le signe du produit suit la règle des signes.",
        ),
        Etape(
            "Vérifier — un test dans chaque zone",
            f"$f({r1 - 1}) = {test_gauche:.0f}$ (négatif) · "
            f"$f({(r1 + r2)/2:g}) = {test_milieu:.0f}$ (positif) · "
            f"$f({r2 + 1}) = {test_droite:.0f}$ (négatif). ✓ "
            "Trois calculs suffisent à confirmer tout le tableau de signe.",
        ),
        Etape(
            "Interpréter — signe et variations ne sont pas la même chose",
            "Le tableau de **signe** dit où la courbe est au-dessus de l'axe ; le "
            "tableau de **variations** dirait où elle monte. Ici $f$ est positive "
            f"entre {r1} et {r2}, mais elle n'y est pas croissante partout. "
            "Confondre les deux lectures est l'erreur classique du chapitre — et une "
            "question de profit positif porte bien sur le **signe**.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Signe de f",
        indice="Les racines se lisent sur la forme factorisée. Testez une valeur "
        "dans chaque zone.",
        pieges=[
            (f"f(x) < 0 sur ]{r1} ; {r2}[ et f(x) > 0 à l'extérieur",
             f"Vérifiez avec un test : $f({(r1 + r2)/2:g}) = {test_milieu:.0f}$, "
             "donc positif entre les racines."),
            (f"f(x) > 0 pour tout x sauf en {r1} et {r2}",
             "Un produit de deux facteurs affines de pentes de signes contraires "
             "change bien de signe en traversant chaque racine."),
            (f"f(x) a le même signe que x sur tout l'axe",
             "Le signe de $f$ ne dépend pas de celui de $x$ mais de la position de "
             f"$x$ par rapport aux racines {r1} et {r2}."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Image ou antécédent",
        "2️⃣ Calculer et lire une pente",
        "3️⃣ Équilibre offre-demande",
        "4️⃣ Signe d'un produit",
    ]
)

with onglets[0]:
    st.subheader("Les deux sens de lecture d'une fonction")
    executer("p6_image", gen_image_antecedent)

with onglets[1]:
    st.subheader("La pente, avec ses unités")
    executer("p6_pente", gen_pente)

with onglets[2]:
    st.subheader("Deux droites qui se croisent")
    executer("p6_equilibre", gen_equilibre)

with onglets[3]:
    st.subheader("Tableau de signe d'un produit")
    executer("p6_signe", gen_signe_produit)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°6 — Fonctions et fonctions affines · "
    "Fil rouge C : le logement étudiant · Sciences Po."
)
