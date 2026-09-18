"""Série S5 — Discriminant et signe du trinôme. Fil rouge E : le festival (clôture)."""

import math
import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S5 | Discriminant", page_icon="🔺", layout="wide")

x, p_ = sp.symbols("x p")

st.title("🔺 S5 — Discriminant et signe du trinôme")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer un **discriminant**, en déduire le nombre de racines, les calculer, et
établir le **signe du trinôme** — donc résoudre une inéquation du second degré.

### 🧠 Ce que le discriminant apporte
En séance 4, les racines se lisaient sur une forme déjà factorisée. Mais la plupart
des expressions arrivent développées, et il faut alors un outil pour savoir **s'il
existe** des racines avant de les chercher. C'est exactement ce que fait $\\Delta$ :
il répond d'abord à la question d'existence, ensuite seulement à celle des valeurs.

### 🎪 Fil rouge E — Le festival (clôture)
Le profit du festival s'écrit $\\pi(p) = -60p^2 + 9\\,000p - 250\\,000$.
Pour quels prix le festival est-il bénéficiaire ?
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 5")
    st.latex(r"\Delta = b^2 - 4ac")
    st.markdown("**Les trois cas**")
    st.markdown(
        "$\\Delta > 0$ : **deux** racines distinctes\n\n"
        "$\\Delta = 0$ : **une** racine double\n\n"
        "$\\Delta < 0$ : **aucune** racine réelle"
    )
    st.markdown("**Les racines**")
    st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{\Delta}}{2a}")
    st.markdown("**Signe du trinôme**")
    st.info(
        "Le trinôme est **du signe de $a$** partout, **sauf entre les racines** "
        "où il est du signe contraire.\n\n"
        "Si $\\Delta < 0$, il garde le signe de $a$ sur tout l'axe."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Calculer le discriminant --------------------------------------------


def gen_discriminant() -> Exercice:
    cas = random.choice(["deux", "deux", "double", "aucune"])
    a = random.choice([-3, -2, -1, 1, 2, 3])

    if cas == "double":
        r = random.choice([-3, -1, 2, 4])
        b = -2 * a * r
        c = a * r**2
    elif cas == "aucune":
        b = random.choice([-6, -2, 4, 8])
        # Delta = b^2 - 4ac < 0  =>  4ac > b^2
        c = a * random.choice([3, 5, 8])
        while b**2 - 4 * a * c >= 0:
            c = c + a * 2
    else:
        r1 = random.choice([-5, -2, 1, 3])
        r2 = r1 + random.choice([2, 4, 6])
        b = -a * (r1 + r2)
        c = a * r1 * r2

    f = a * x**2 + b * x + c
    delta = b**2 - 4 * a * c
    reponse = float(delta)

    enonce = f"""
> Soit le trinôme
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez son **discriminant** $\\Delta$.
"""

    nb = "deux racines distinctes" if delta > 0 else \
        "une racine double" if delta == 0 else "aucune racine réelle"

    etapes = [
        Etape(
            "Identifier — repérer $a$, $b$ et $c$ dans l'ordre",
            f"Ici $a = {a}$, $b = {b}$, $c = {c}$. L'erreur la plus fréquente est de "
            "se tromper de coefficient ou d'oublier un signe négatif : écrire les "
            "trois valeurs avant de calculer est une précaution qui se rentabilise.",
        ),
        Etape(
            "Appliquer $\\Delta = b^2 - 4ac$",
            f"Attention au produit de signes : $4 \\times {a} \\times {c} = "
            f"{4*a*c}$, qu'il faut ensuite **retrancher**.",
            rf"\Delta = ({b})^2 - 4 \times ({a}) \times ({c}) = {b**2} - ({4*a*c}) "
            rf"= {delta}",
        ),
        Etape(
            "Vérifier — conclure sur le nombre de racines",
            f"$\\Delta = {delta}$ est "
            f"**{'strictement positif' if delta > 0 else 'nul' if delta == 0 else 'strictement négatif'}** : "
            f"le trinôme admet donc **{nb}**. "
            "C'est la première information à en tirer, avant même de calculer quoi "
            "que ce soit.",
        ),
        Etape(
            "Interpréter — ce que $\\Delta$ dit graphiquement",
            f"$\\Delta$ mesure si la parabole **coupe** l'axe horizontal. "
            + ("Deux points d'intersection ici."
               if delta > 0 else
               "Un seul point : la parabole est tangente à l'axe."
               if delta == 0 else
               "Aucun : la parabole est entièrement d'un seul côté de l'axe. "
               "Concrètement, cela signifie que la grandeur modélisée ne s'annule "
               "jamais — un profit toujours négatif, par exemple."),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Δ =",
        tolerance=1e-6,
        indice="$\\Delta = b^2 - 4ac$. Notez d'abord les trois coefficients avec "
        "leurs signes.",
        pieges=[
            (float(b**2 + 4 * a * c),
             "Erreur de signe : la formule **retranche** $4ac$."),
            (float(b**2 - 4 * a - c),
             "$4ac$ est un produit des trois facteurs $4$, $a$ et $c$."),
        ],
    )


# --- 2. Calculer les racines ------------------------------------------------


def gen_racines_formule() -> Exercice:
    a = random.choice([-2, -1, 1, 2, 3])
    r1 = random.choice([-6, -3, -1, 2, 4])
    r2 = r1 + random.choice([1, 2, 3, 5])
    b = -a * (r1 + r2)
    c = a * r1 * r2
    f = a * x**2 + b * x + c
    delta = b**2 - 4 * a * c
    reponse = float(max(r1, r2))

    enonce = f"""
> Soit le trinôme
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez ses racines et donnez la **plus grande**.
"""

    etapes = [
        Etape(
            "Identifier — vérifier d'abord l'existence",
            f"$\\Delta = ({b})^2 - 4 \\times ({a}) \\times ({c}) = {delta}$, "
            "strictement positif : il y a bien deux racines distinctes. "
            "Se lancer dans la formule sans avoir vérifié $\\Delta$ mène à une racine "
            "carrée impossible.",
        ),
        Etape(
            "Appliquer la formule",
            f"$\\sqrt{{{delta}}} = {math.isqrt(delta) if math.isqrt(delta)**2 == delta else round(math.sqrt(delta), 4)}$.",
            rf"x_{{1,2}} = \frac{{-({b}) \pm \sqrt{{{delta}}}}}{{2 \times ({a})}}",
        ),
        Etape(
            "Calculer les deux valeurs",
            "",
            rf"x_1 = {min(r1, r2)} \qquad x_2 = {max(r1, r2)}",
        ),
        Etape(
            "Vérifier — par la forme factorisée",
            f"Si les racines sont ${r1}$ et ${r2}$, alors "
            f"$f(x) = {a}(x - ({r1}))(x - ({r2}))$. En développant, on retrouve bien "
            f"${sp.latex(f)}$. ✓ C'est la vérification la plus sûre, et elle prend "
            "trente secondes.",
        ),
        Etape(
            "Interpréter",
            "Le discriminant et la forme factorisée disent la même chose de deux "
            "manières : l'une part du développé, l'autre du factorisé. Savoir passer "
            "de l'une à l'autre est ce qui permet de choisir le chemin le plus court "
            "selon la forme sous laquelle l'énoncé arrive.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Plus grande racine",
        tolerance=1e-6,
        indice="Calculez $\\Delta$ d'abord, puis appliquez la formule.",
        pieges=[
            (float(min(r1, r2)),
             "C'est la **plus petite** racine."),
            (float((b + math.sqrt(delta)) / (2 * a)),
             "Erreur de signe : la formule commence par $-b$, pas par $+b$."),
        ],
    )


# --- 3. Signe du trinôme (QCM) ---------------------------------------------


def gen_signe() -> Exercice:
    a = random.choice([-3, -2, -1, 1, 2, 3])
    r1 = random.choice([-5, -2, 1, 3])
    r2 = r1 + random.choice([2, 4, 6])
    b = -a * (r1 + r2)
    c = a * r1 * r2
    f = a * x**2 + b * x + c

    signe_ext = "positif" if a > 0 else "négatif"
    signe_int = "négatif" if a > 0 else "positif"

    bonne = (
        f"f est {signe_int} entre {r1} et {r2}, et {signe_ext} à l'extérieur"
    )
    options = [
        bonne,
        f"f est {signe_ext} entre {r1} et {r2}, et {signe_int} à l'extérieur",
        f"f est {signe_ext} sur tout l'axe",
        f"f est du signe de x sur tout l'axe",
    ]
    random.shuffle(options)

    enonce = f"""
> Soit le trinôme
>
> $$ f(x) = {sp.latex(f)} $$
>
> dont les racines sont ${r1}$ et ${r2}$.
>
> Quel est son **signe** selon les valeurs de $x$ ?
"""

    milieu = (r1 + r2) / 2

    etapes = [
        Etape(
            "Identifier — la règle tient en une phrase",
            f"Un trinôme est **du signe de $a$** partout, **sauf entre les racines** "
            f"où il prend le signe contraire. Ici $a = {a}$, donc "
            f"{signe_ext} à l'extérieur et {signe_int} entre les racines.",
        ),
        Etape(
            "Appliquer",
            f"Les racines sont ${r1}$ et ${r2}$. Elles découpent l'axe en trois zones, "
            "et le signe alterne en les traversant.",
        ),
        Etape(
            "Vérifier — un test par zone",
            f"$f({r1 - 1}) = {float(f.subs(x, r1-1)):.0f}$ · "
            f"$f({milieu:g}) = {float(f.subs(x, milieu)):.0f}$ · "
            f"$f({r2 + 1}) = {float(f.subs(x, r2+1)):.0f}$. ✓ "
            "En cas de doute sur la règle, ces trois calculs la remplacent "
            "intégralement.",
        ),
        Etape(
            "Interpréter — pourquoi le signe plutôt que les variations",
            "Une question du type « pour quels prix le festival est-il bénéficiaire ? » "
            "porte sur le **signe** du profit, pas sur ses variations. "
            "Le trinôme est positif sur un intervalle, pas à partir d'un seuil : "
            "il y a deux bornes, et les oublier revient à ne répondre qu'à la moitié "
            "de la question.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Signe du trinôme",
        indice=f"Quel est le signe de $a$ ? Le trinôme prend ce signe hors des racines.",
        pieges=[
            (f"f est {signe_ext} entre {r1} et {r2}, et {signe_int} à l'extérieur",
             f"C'est l'inverse : le trinôme est du signe de $a$ (donc {signe_ext}) "
             "**à l'extérieur** des racines."),
            (f"f est {signe_ext} sur tout l'axe",
             "Ce ne serait vrai que si $\\Delta < 0$. Ici il y a deux racines, donc "
             "un changement de signe."),
            (f"f est du signe de x sur tout l'axe",
             "Le signe du trinôme dépend de la position de $x$ par rapport aux "
             "racines, pas du signe de $x$."),
        ],
    )


# --- 4. Fil rouge : pour quels prix le festival est-il bénéficiaire ? ------


def gen_festival() -> Exercice:
    # On retire tant que le profit ne peut pas être positif : sans deux racines,
    # la question « pour quels prix est-il bénéficiaire ? » n'a pas de réponse.
    a = -60
    while True:
        b = random.choice([9_000, 8_400, 9_600])
        cout = random.choice([250_000, 300_000, 240_000])
        delta = b**2 - 4 * a * (-cout)
        if delta > 0:
            break
    racine = math.sqrt(delta)
    p1 = (-b + racine) / (2 * a)
    p2 = (-b - racine) / (2 * a)
    bas, haut = min(p1, p2), max(p1, p2)
    reponse = float(bas)

    enonce = f"""
> **Le festival (clôture de l'arc).** Le profit du festival s'écrit
>
> $$ \\pi(p) = {a}p^2 + {b:,}\\,p - {cout:,} $$
>
> Pour quels prix le festival est-il **bénéficiaire** ?
> Donnez la **borne basse** de l'intervalle, arrondie au centime.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — une inéquation du second degré",
            "« Bénéficiaire » signifie $\\pi(p) > 0$. On ne cherche pas un prix mais "
            "un **intervalle** de prix. La méthode est en trois temps : racines, "
            "puis signe, puis conclusion.",
        ),
        Etape(
            "Calculer le discriminant et les racines",
            f"$\\Delta = {b}^2 - 4 \\times ({a}) \\times ({-cout}) = {delta:,}$, "
            f"positif : deux racines.".replace(",", "\u202f"),
            rf"p_{{1,2}} = \frac{{-{b} \pm \sqrt{{{delta}}}}}{{2 \times ({a})}} "
            rf"\quad\Rightarrow\quad p_1 \approx {bas:.2f} \ ,\ "
            rf"p_2 \approx {haut:.2f}",
        ),
        Etape(
            "Appliquer la règle de signe",
            f"Ici $a = {a}$ est **négatif** : le trinôme est négatif à l'extérieur "
            "des racines et **positif entre elles**. Le festival est donc "
            "bénéficiaire pour les prix compris entre les deux racines.",
            rf"\pi(p) > 0 \iff p \in \left]{bas:.2f}\,;\,{haut:.2f}\right[",
        ),
        Etape(
            "Vérifier",
            f"$\\pi({(bas + haut)/2:.0f}) = "
            f"{a*((bas+haut)/2)**2 + b*((bas+haut)/2) - cout:,.0f}$ € — positif ✓, "
            f"et $\\pi({bas - 10:.0f}) = "
            f"{a*(bas-10)**2 + b*(bas-10) - cout:,.0f}$ € — négatif ✓."
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — deux bornes, et c'est le point",
            f"En dessous de {bas:.2f} €, la billetterie ne couvre pas les "
            f"{cout:,} € de coûts. Au-dessus de {haut:.2f} €, trop peu de spectateurs "
            "viennent. La rentabilité est bornée **des deux côtés** : répondre « à "
            "partir de tel prix » serait une réponse fausse, et c'est l'erreur que "
            "cette question cherche à révéler.".replace(",", "\u202f"),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Borne basse",
        unite="€",
        tolerance=0.002,
        indice="Calculez les deux racines, puis appliquez la règle de signe en "
        "regardant le signe de $a$.",
        pieges=[
            (float(haut),
             "C'est la borne **haute** de l'intervalle. L'énoncé demande la borne "
             "basse."),
            (float(b / (2 * 60)),
             "C'est le prix qui **maximise** le profit (le sommet), pas une borne de "
             "rentabilité."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Calculer Δ",
        "2️⃣ Calculer les racines",
        "3️⃣ Signe du trinôme",
        "4️⃣ Festival : quels prix ?",
    ]
)

with onglets[0]:
    st.subheader("Le discriminant et ce qu'il annonce")
    executer("s5_delta", gen_discriminant)

with onglets[1]:
    st.subheader("La formule des racines")
    executer("s5_racines", gen_racines_formule)

with onglets[2]:
    st.subheader("Du signe de a, sauf entre les racines")
    executer("s5_signe", gen_signe)

with onglets[3]:
    st.subheader("Clôture de l'arc festival")
    executer("s5_festival", gen_festival)

st.markdown("---")
st.caption(
    "Semestre — séance n°5 : Discriminant et signe du trinôme · "
    "Fil rouge E : le festival de Villeneuve · Sciences Po."
)
