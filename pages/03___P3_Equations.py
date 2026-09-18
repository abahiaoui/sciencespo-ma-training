"""Série P3 — Équations à une variable. Fil rouge B : Vélocité."""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P3 | Équations", page_icon="⚖️", layout="wide")

x = sp.Symbol("x")

st.title("⚖️ P3 — Équations à une variable")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Résoudre une équation du premier degré, utiliser l'**équation produit nul**, et
**isoler une variable** dans une formule — la compétence la plus utile de tout le
module.

### 🧠 Le principe unique
Une équation est une balance : tout ce qu'on fait d'un côté, on le fait de l'autre.
Ajouter, retrancher, multiplier ou diviser par un nombre **non nul** ne change pas
l'ensemble des solutions. Tout le reste en découle.

### 🚲 Fil rouge B — Vélocité
Villeneuve lance *Vélocité*, un service de vélos en libre-service : **40 000 €** de
coûts fixes, **350 €** par vélo mis en circulation, et **90 €** de recette par
abonnement vendu.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 3")
    st.markdown("**Ce qu'on a le droit de faire à une égalité**")
    st.latex(r"a = b \iff a + k = b + k")
    st.latex(r"a = b \iff ka = kb \quad (k \neq 0)")
    st.markdown("**Équation du premier degré**")
    st.latex(r"ax + b = cx + d \iff x = \frac{d-b}{a-c}")
    st.markdown("**Équation produit nul**")
    st.latex(r"A \times B = 0 \iff A = 0 \ \text{ou} \ B = 0")
    st.info(
        "**Isoler une variable**\n\n"
        "Même méthode, mais les autres lettres sont traitées comme des nombres. "
        "C'est la compétence la plus utile du module."
    )
    st.error(
        "**Le réflexe obligatoire**\n\n"
        "Toute solution se vérifie en la réinjectant dans l'équation de départ."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Équation du premier degré ------------------------------------------


def gen_premier_degre() -> Exercice:
    a = random.choice([2, 3, 4, 5, 6, 7])
    c = random.choice([-3, -2, -1, 1, 2, 3])
    while a == c:
        c = random.choice([-3, -2, -1, 1, 2, 3])
    sol = random.choice([-4, -3, -2, 2, 3, 4, 5, 6])
    b = random.choice([-8, -5, -2, 1, 4, 7])
    d = (a - c) * sol + b

    enonce = f"""
> Résolvez l'équation suivante :
>
> $$ {sp.latex(a*x + b)} = {sp.latex(c*x + d)} $$
"""

    etapes = [
        Etape(
            "Identifier — rassembler puis isoler",
            "Il y a des $x$ des deux côtés et des constantes des deux côtés. "
            "La stratégie est invariable : les $x$ d'un côté, les nombres de l'autre, "
            "puis une division.",
        ),
        Etape(
            "Calculer — déplacer les termes",
            f"On retranche ${sp.latex(c*x)}$ des deux membres, puis ${b}$ des deux "
            "membres. Chaque opération porte sur les **deux** côtés de la balance.",
            rf"{sp.latex(a*x + b)} = {sp.latex(c*x + d)} \iff "
            rf"{sp.latex((a-c)*x)} = {d - b}",
        ),
        Etape(
            "Isoler l'inconnue",
            f"On divise par ${a - c}$, ce qui est licite car ce nombre n'est pas nul.",
            rf"x = \frac{{{d - b}}}{{{a - c}}} = {sol}",
        ),
        Etape(
            "Vérifier — réinjecter la solution",
            f"À gauche : ${a} \\times {sol} + ({b}) = {a*sol + b}$. "
            f"À droite : ${c} \\times {sol} + {d} = {c*sol + d}$. ✓ "
            "Cette vérification est toujours possible et devrait être systématique.",
        ),
        Etape(
            "Interpréter",
            "Résoudre une équation, c'est répondre à : « pour quelle valeur ces deux "
            "quantités deviennent-elles égales ? ». Appliquée à deux dispositifs, "
            "cette valeur est un **seuil**.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="x =",
        tolerance=1e-6,
        indice="Rassemblez les $x$ à gauche et les nombres à droite avant de diviser.",
        pieges=[
            (float(d + b) / (a - c),
             "Erreur de signe : faire passer $b$ de l'autre côté, c'est le "
             "**retrancher** des deux membres, pas l'ajouter."),
            (float(d - b) / (a + c) if a + c != 0 else 0.0,
             f"Erreur de signe en regroupant les $x$ : le coefficient devient "
             f"$a - c = {a - c}$."),
        ],
    )


# --- 2. Équation produit nul ------------------------------------------------


def gen_produit_nul() -> Exercice:
    a = random.choice([1, 2, 3, 4])
    b = random.choice([-12, -8, -6, 5, 9, 15])
    c = random.choice([1, 2, 5])
    d = random.choice([-20, -10, 4, 14])
    r1 = Fraction(-b, a)
    r2 = Fraction(-d, c)
    reponse = float(max(r1, r2))

    enonce = f"""
> Résolvez l'équation produit nul suivante :
>
> $$ ({sp.latex(a*x + b)})({sp.latex(c*x + d)}) = 0 $$
>
> Donnez la **plus grande** des deux solutions.
"""

    etapes = [
        Etape(
            "Identifier — surtout ne pas développer",
            "Un produit est nul **si et seulement si** l'un de ses facteurs est nul. "
            "La forme factorisée donne donc directement les solutions ; développer "
            "détruirait cette information et ramènerait à une équation plus difficile.",
        ),
        Etape(
            "Séparer en deux équations simples",
            "",
            rf"{sp.latex(a*x + b)} = 0 \quad \text{{ou}} \quad {sp.latex(c*x + d)} = 0",
        ),
        Etape(
            "Résoudre chacune",
            "Deux équations du premier degré, traitées indépendamment.",
            rf"x = {sp.latex(sp.Rational(r1.numerator, r1.denominator))} "
            rf"\quad \text{{ou}} \quad "
            rf"x = {sp.latex(sp.Rational(r2.numerator, r2.denominator))}",
        ),
        Etape(
            "Vérifier",
            f"Pour $x = {sp.latex(sp.Rational(r1.numerator, r1.denominator))}$, le "
            "premier facteur s'annule, donc le produit aussi — quelle que soit la "
            "valeur du second. ✓ C'est exactement ce que dit la règle.",
        ),
        Etape(
            "Interpréter",
            "Cette règle explique pourquoi la factorisation de la séance 2 était utile : "
            "une expression factorisée livre ses zéros immédiatement. Au semestre, "
            "c'est ainsi qu'on trouvera les racines d'une parabole.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Plus grande solution",
        tolerance=1e-6,
        indice="Un produit est nul si l'un des facteurs est nul. Deux équations "
        "simples, donc.",
        pieges=[
            (float(min(r1, r2)),
             "C'est la **plus petite** des deux solutions. L'énoncé demande la plus "
             "grande."),
            (float(b * d) / (a * c),
             "Vous avez développé puis cherché autre chose. La forme factorisée "
             "donnait les solutions sans aucun calcul supplémentaire."),
        ],
    )


# --- 3. Isoler une variable -------------------------------------------------


def gen_isoler() -> Exercice:
    modele = random.choice(["affine", "produit", "moyenne"])

    if modele == "affine":
        a = random.choice([2, 3, 5, 8])
        b = random.choice([10, 25, 40, 60])
        y0 = random.choice([50, 80, 120, 200])
        reponse = float(Fraction(y0 - b, a))
        formule = rf"y = {a}x + {b}"
        question = f"Sachant que $y = {y0}$, que vaut $x$ ?"
        etapes_calcul = (
            rf"{y0} = {a}x + {b} \iff {a}x = {y0 - b} \iff "
            rf"x = \frac{{{y0 - b}}}{{{a}}} = {reponse:.4g}"
        )
        commentaire = (
            "Les autres lettres sont traitées exactement comme des nombres : la "
            "méthode ne change pas d'un iota par rapport à l'onglet 1."
        )
        pieges = [
            (float(y0 + b) / a,
             "Erreur de signe : on **retranche** la constante des deux membres."),
            (float(y0) / a,
             "Vous avez oublié la constante $b$ : elle doit d'abord être déplacée."),
        ]
    elif modele == "produit":
        p = random.choice([12, 15, 20, 25])
        R = random.choice([600, 900, 1200, 1500])
        reponse = float(Fraction(R, p))
        formule = rf"R = p \times q"
        question = (
            f"Une recette totale de $R = {R}$ € est réalisée à un prix unitaire "
            f"de $p = {p}$ €. Combien d'unités $q$ ont été vendues ?"
        )
        etapes_calcul = (
            rf"{R} = {p} \times q \iff q = \frac{{{R}}}{{{p}}} = {reponse:.4g}"
        )
        commentaire = (
            "Isoler $q$ dans un produit demande une seule opération : diviser les deux "
            "membres par $p$, qui n'est pas nul."
        )
        pieges = [
            (float(R * p),
             "Vous avez multiplié au lieu de diviser. Pour défaire une "
             "multiplication, on divise."),
            (float(R - p),
             "Vous avez soustrait. L'opération à défaire ici est une "
             "multiplication, pas une addition."),
        ]
    else:
        n = random.choice([4, 5, 6, 8])
        m = random.choice([12, 15, 20, 25])
        autres = random.choice([40, 55, 70, 90])
        reponse = float(n * m - autres)
        formule = rf"m = \frac{{S}}{{n}}"
        question = (
            f"La moyenne de ${n}$ valeurs vaut ${m}$. La somme des ${n - 1}$ premières "
            f"vaut ${autres}$. Que vaut la dernière ?"
        )
        etapes_calcul = (
            rf"S = n \times m = {n} \times {m} = {n*m} \quad\Rightarrow\quad "
            rf"x = {n*m} - {autres} = {reponse:.0f}"
        )
        commentaire = (
            "On isole d'abord la somme totale dans la formule de la moyenne, "
            "puis on en retranche ce que l'on connaît déjà."
        )
        pieges = [
            (float(m - autres),
             "Vous avez oublié de remonter à la **somme** : la moyenne doit d'abord "
             "être multipliée par l'effectif."),
            (float(n * m),
             "C'est la somme totale, pas la dernière valeur : il reste à retrancher "
             "les autres."),
        ]

    enonce = f"""
> On dispose de la relation
>
> $$ {formule} $$
>
> {question}
"""

    etapes = [
        Etape(
            "Identifier — isoler, c'est défaire les opérations",
            "On regarde ce qui « entoure » l'inconnue, et on défait chaque opération "
            "en remontant : une addition se défait par une soustraction, une "
            "multiplication par une division.",
        ),
        Etape(
            "Calculer",
            commentaire,
            etapes_calcul,
        ),
        Etape(
            "Vérifier — reprendre la formule de départ",
            "On replace la valeur trouvée dans la relation initiale et on contrôle "
            "qu'elle est bien satisfaite. Ce contrôle prend dix secondes.",
        ),
        Etape(
            "Interpréter — pourquoi c'est la compétence la plus utile",
            "Toutes les formules que vous rencontrerez en sciences sociales — taux, "
            "indices, moyennes, élasticités — s'utilisent dans les deux sens. Savoir "
            "retourner une formule vaut mieux que d'en mémoriser plusieurs versions.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur cherchée",
        tolerance=0.005,
        indice="Repérez ce qui entoure l'inconnue, et défaites chaque opération.",
        pieges=pieges,
    )


# --- 4. Fil rouge : le seuil de rentabilité de Vélocité --------------------


def gen_velocite() -> Exercice:
    fixe = 40_000
    par_velo = 350
    recette = 90
    flotte = random.choice([200, 280, 320, 400, 500])
    cout = fixe + par_velo * flotte
    reponse = cout / recette

    enonce = f"""
> **Vélocité.** Le service coûte **{fixe:,} €** de coûts fixes, plus **{par_velo} €**
> par vélo mis en circulation. Chaque abonnement vendu rapporte **{recette} €**.
>
> Villeneuve met **{flotte} vélos** en circulation.
>
> À partir de combien d'abonnements le service couvre-t-il ses coûts ?
> Donnez le nombre d'abonnements à l'équilibre (non entier accepté).
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — traduire avant de calculer",
            f"Le coût ne dépend pas du nombre d'abonnements : avec {flotte} vélos, "
            f"il est **fixé**. La recette, elle, dépend du nombre $q$ d'abonnements "
            "vendus. L'équilibre est atteint quand les deux se rejoignent.",
            rf"C = {fixe} + {par_velo} \times {flotte} = {cout} "
            rf"\qquad R(q) = {recette}q",
        ),
        Etape(
            "Poser l'équation",
            "Couvrir ses coûts signifie recette égale coût.",
            rf"{recette}q = {cout}",
        ),
        Etape(
            "Résoudre",
            "",
            rf"q = \frac{{{cout}}}{{{recette}}} \approx {reponse:.2f}"
            rf"\ \text{{abonnements}}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur est-il crédible ?",
            f"{reponse:.0f} abonnements pour {flotte} vélos, soit environ "
            f"{reponse/flotte:.1f} abonnés par vélo. C'est plausible pour un service "
            "en libre-service. Un résultat de 10 ou de 500 000 aurait signalé une "
            "erreur d'unité.",
        ),
        Etape(
            "Interpréter — ce que le seuil dit à la collectivité",
            f"En dessous de {reponse:.0f} abonnements, le service est déficitaire et "
            "la différence est financée par le budget général. Le seuil ne dit pas "
            "si le service doit exister — un service public peut être délibérément "
            "subventionné — mais il chiffre exactement ce que coûte ce choix.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Nombre d'abonnements",
        tolerance=0.005,
        indice="Calculez d'abord le coût total, qui ne dépend pas de $q$.",
        pieges=[
            (float(fixe) / recette,
             f"Vous avez oublié le coût des {flotte} vélos : seuls les coûts fixes "
             "ont été couverts."),
            (float(par_velo * flotte) / recette,
             "Vous avez oublié les coûts fixes de gestion."),
            (float(cout),
             "C'est le coût total en euros, pas un nombre d'abonnements. "
             "Il reste à diviser par la recette unitaire."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Premier degré",
        "2️⃣ Équation produit nul",
        "3️⃣ Isoler une variable",
        "4️⃣ Vélocité : le seuil",
    ]
)

with onglets[0]:
    st.subheader("Résoudre une équation du premier degré")
    executer("p3_premier", gen_premier_degre)

with onglets[1]:
    st.subheader("Un produit nul livre ses solutions")
    executer("p3_produit", gen_produit_nul)

with onglets[2]:
    st.subheader("Retourner une formule")
    executer("p3_isoler", gen_isoler)

with onglets[3]:
    st.subheader("Le seuil de rentabilité de Vélocité")
    executer("p3_velocite", gen_velocite)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°3 — Équations à une variable · Fil rouge B : Vélocité · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
