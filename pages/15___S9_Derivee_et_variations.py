"""Série S9 — La fonction dérivée et les variations. Fil rouge G : l'atelier."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S9 | Dérivée et variations", page_icon="↗️", layout="wide")

x, q = sp.symbols("x q")

st.title("↗️ S9 — La fonction dérivée et les variations")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **fonction dérivée** avec les règles de combinaison, en étudier le
**signe**, dresser un **tableau de variations**, et trouver un extremum.

### 🧠 Le théorème central du chapitre
Le **signe** de $f'$ donne les **variations** de $f$. On ne regarde plus la valeur de
la dérivée mais seulement son signe : étudier une fonction revient donc à étudier le
signe d'une autre, souvent beaucoup plus simple — un trinôme, par exemple, dont on
sait tout depuis la séance 5.

### 🔧 Fil rouge G — L'atelier municipal
L'atelier facture **100 €** la réparation. Son résultat s'écrit
$\\pi(q) = 100q - \\left(40\\,000 + 35q + 0{,}02\\,q^2\\right)
= -0{,}02\\,q^2 + 65q - 40\\,000$.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 9")
    st.markdown("**Dérivées usuelles**")
    st.latex(r"(x^n)' = n x^{n-1} \qquad (k)' = 0")
    st.latex(r"(e^x)' = e^x \qquad (\ln x)' = \frac{1}{x}")
    st.markdown("**Règles de combinaison**")
    st.latex(r"(u+v)' = u' + v' \qquad (ku)' = k u'")
    st.latex(r"(uv)' = u'v + uv'")
    st.markdown("**Le théorème central**")
    st.latex(r"f' > 0 \Rightarrow f \nearrow \qquad f' < 0 \Rightarrow f \searrow")
    st.error(
        "**Dérivée nulle et extremum : attention**\n\n"
        "$f'(a) = 0$ ne suffit pas. Il faut que $f'$ **change de signe** en $a$."
    )
    st.info(
        "**La méthode en quatre étapes**\n\n"
        "1. Dériver · 2. Résoudre $f'(x) = 0$ · 3. Étudier le signe de $f'$ · "
        "4. Conclure sur $f$"
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Dériver un polynôme -------------------------------------------------


def gen_derivee() -> Exercice:
    a = random.choice([1, 2, 3, 4, -2])
    b = random.choice([-6, -4, -2, 3, 5])
    c = random.choice([-8, -3, 2, 7])
    d = random.choice([-5, 0, 4, 9])
    degre3 = random.random() < 0.5

    f = (a * x**3 if degre3 else 0) + b * x**2 + c * x + d
    reponse = sp.expand(sp.diff(f, x))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez la **fonction dérivée** $f'(x)$.
"""

    etapes = [
        Etape(
            "Identifier — une somme se dérive terme à terme",
            "La dérivée d'une somme est la somme des dérivées, et un coefficient "
            "constant se conserve. Ces deux règles suffisent pour tout polynôme — "
            "elles ne valent ni pour un produit ni pour un quotient.",
        ),
        Etape(
            "Appliquer $(x^n)' = n\\,x^{n-1}$",
            f"L'exposant descend en facteur puis diminue de 1. Le terme constant "
            f"(${d}$) disparaît : une grandeur qui ne varie pas n'a pas de pente.",
            rf"f'(x) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — le degré a baissé d'une unité",
            f"$f$ est de degré ${sp.degree(f, x)}$, $f'$ de degré "
            f"${sp.degree(reponse, x) if reponse.free_symbols else 0}$. ✓ "
            "Ce contrôle détecte immédiatement un exposant oublié.",
        ),
        Etape(
            "Interpréter — $f'$ est une fonction, pas un nombre",
            "C'est le changement de statut décisif de cette séance : en séance 8, on "
            "calculait un nombre dérivé en un point. Ici on obtient une **fonction** "
            "qui donne la pente partout — donc un objet qu'on peut à son tour "
            "étudier, notamment en signe.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="f'(x) =",
        symboles=["x"],
        indice="Dérivez chaque terme séparément. Que devient la constante ?",
        pieges=[
            (sp.expand(sp.diff(f, x) + d) if d != 0 else sp.expand(sp.diff(f, x) + 1),
             "Vous avez conservé le terme constant : sa dérivée est **nulle**."),
        ],
    )


# --- 2. Règle du produit ----------------------------------------------------


def gen_produit() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-4, -2, 3, 5])
    c = random.choice([1, 2])
    d = random.choice([-6, -1, 4])
    u = a * x + b
    v = c * x**2 + d
    reponse = sp.expand(sp.diff(u * v, x))
    up, vp = sp.diff(u, x), sp.diff(v, x)

    enonce = f"""
> Soit la fonction définie par le **produit**
>
> $$ f(x) = ({sp.latex(u)})({sp.latex(v)}) $$
>
> Calculez $f'(x)$.
"""

    etapes = [
        Etape(
            "Identifier — reconnaître la structure avant de calculer",
            "C'est un produit de deux fonctions : la règle $(uv)' = u'v + uv'$ "
            "s'applique. Et $(uv)'$ n'est **jamais** $u'v'$ — c'est la même erreur de "
            "structure que $(a+b)^2 \\neq a^2 + b^2$.",
        ),
        Etape(
            "Poser $u$, $v$, $u'$ et $v'$",
            "Écrire ces quatre éléments séparément avant d'assembler évite la "
            "quasi-totalité des fautes.",
            rf"u = {sp.latex(u)},\ u' = {sp.latex(up)} \qquad "
            rf"v = {sp.latex(v)},\ v' = {sp.latex(vp)}",
        ),
        Etape(
            "Assembler",
            "",
            rf"f'(x) = ({sp.latex(up)})({sp.latex(v)}) + ({sp.latex(u)})"
            rf"({sp.latex(vp)}) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — par le développement",
            f"En développant d'abord, $f(x) = {sp.latex(sp.expand(u*v))}$, dont la "
            f"dérivée terme à terme donne ${sp.latex(reponse)}$. ✓ "
            "Ici les deux chemins étaient possibles ; avec un logarithme ou une "
            "exponentielle, seule la règle du produit fonctionnera.",
        ),
        Etape(
            "Interpréter",
            "La règle dit qu'un produit varie pour **deux** raisons : parce que le "
            "premier facteur bouge, et parce que le second bouge. D'où les deux "
            "termes. Cette lecture — un effet total est la somme de plusieurs "
            "canaux — se retrouvera partout.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="f'(x) =",
        symboles=["x"],
        indice="Posez $u$, $v$, $u'$ et $v'$ avant d'assembler.",
        pieges=[
            (sp.expand(up * vp),
             "Vous avez calculé $u'v'$. La dérivée d'un produit n'est **jamais** le "
             "produit des dérivées : il faut deux termes."),
            (sp.expand(up * v),
             "Il manque le second terme $uv'$ : le facteur $v$ varie lui aussi."),
        ],
    )


# --- 3. Tableau de variations : le point critique --------------------------


def gen_variations() -> Exercice:
    a = random.choice([1, 2, 3, -1, -2])
    sol = random.choice([-4, -2, 1, 3, 5, 6])
    b = -2 * a * sol
    c = random.choice([-6, 0, 4, 10])
    f = a * x**2 + b * x + c
    fp = sp.diff(f, x)

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> En quelle valeur de $x$ sa dérivée s'annule-t-elle ?
"""

    etapes = [
        Etape(
            "Identifier — pourquoi chercher où $f'$ s'annule",
            "Ce sont les seuls points où $f$ peut changer de sens de variation. "
            "Ailleurs, $f'$ garde un signe constant et $f$ varie de façon monotone. "
            "Les points critiques découpent donc l'axe en zones homogènes.",
        ),
        Etape("Dériver", "", rf"f'(x) = {sp.latex(fp)}"),
        Etape(
            "Résoudre $f'(x) = 0$",
            "C'est une équation du premier degré — la pré-rentrée 3, appliquée telle "
            "quelle.",
            rf"{sp.latex(fp)} = 0 \iff x = \frac{{{-b}}}{{{2*a}}} = {sol}",
        ),
        Etape(
            "Vérifier — dresser le tableau de signe",
            f"$f'({sol - 1}) = {float(fp.subs(x, sol-1)):.0f}$ et "
            f"$f'({sol + 1}) = {float(fp.subs(x, sol+1)):.0f}$ : la dérivée passe "
            f"du {'négatif au positif' if a > 0 else 'positif au négatif'}. "
            f"C'est donc un **{'minimum' if a > 0 else 'maximum'}**. ✓ "
            "S'annuler ne suffisait pas : il fallait ce changement de signe.",
        ),
        Etape(
            "Interpréter — on retrouve le sommet de la parabole",
            f"La valeur ${sol}$ est exactement l'abscisse du sommet, que la séance 4 "
            "donnait par $-\\frac{b}{2a}$. La dérivation ne fait donc que "
            "généraliser : ce qui n'était vrai que pour les paraboles devient une "
            "méthode applicable à toute fonction dérivable.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="x =",
        tolerance=1e-6,
        indice="Dérivez, puis résolvez $f'(x) = 0$.",
        pieges=[
            (float(-c / b) if b != 0 else 0.0,
             "Vous avez annulé $f$ plutôt que $f'$. C'est bien la **dérivée** qu'il "
             "faut annuler."),
            (float(b),
             "Vous avez donné un coefficient, pas la solution de l'équation."),
        ],
    )


# --- 4. Fil rouge : le résultat de l'atelier -------------------------------


def gen_atelier() -> Exercice:
    prix = 100
    fixe = random.choice([30_000, 40_000, 50_000])
    lineaire = random.choice([25, 35, 40])
    quad = random.choice([0.01, 0.02, 0.025])
    # pi(q) = -quad q^2 + (prix - lineaire) q - fixe
    marge = prix - lineaire
    q_star = marge / (2 * quad)
    reponse = float(q_star)
    pi_max = -quad * q_star**2 + marge * q_star - fixe

    enonce = f"""
> **L'atelier municipal.** Son coût total est
> $C(q) = {fixe:,} + {lineaire}q + {str(quad).replace('.', ',')}\\,q^2$
> et chaque réparation est facturée **{prix} €**.
>
> Le résultat s'écrit donc
> $\\pi(q) = -{str(quad).replace('.', ',')}\\,q^2 + {marge}q - {fixe:,}$.
>
> Combien de réparations maximisent le résultat ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — appliquer la méthode en quatre étapes",
            "La fonction objectif est déjà écrite. Il reste à dériver, annuler, "
            "étudier le signe, conclure. C'est exactement la séquence de la séance, "
            "sans raccourci.",
        ),
        Etape(
            "Dériver et annuler",
            f"$\\pi'(q) = -{2*quad}q + {marge}$. Annuler cette expression revient à "
            f"égaliser la **recette marginale** ({prix} €) et le **coût marginal** "
            f"($C'(q) = {lineaire} + {2*quad}q$) — c'est la même équation, lue "
            "autrement.",
            rf"-{2*quad}q + {marge} = 0 \iff q = \frac{{{marge}}}{{{2*quad}}} "
            rf"= {reponse:.0f}",
        ),
        Etape(
            "Étudier le signe de la dérivée",
            f"$\\pi'$ est affine de pente $-{2*quad}$, donc **décroissante** : elle "
            f"est positive avant {reponse:.0f} et négative après. Le résultat croît "
            "puis décroît : c'est bien un **maximum**, et il est global.",
        ),
        Etape(
            "Vérifier",
            f"$\\pi({reponse - 200:.0f}) = "
            f"{-quad*(q_star-200)**2 + marge*(q_star-200) - fixe:,.0f}$ € et "
            f"$\\pi({reponse + 200:.0f}) = "
            f"{-quad*(q_star+200)**2 + marge*(q_star+200) - fixe:,.0f}$ €, tous deux "
            f"inférieurs à $\\pi({reponse:.0f}) = {pi_max:,.0f}$ €. ✓"
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — la règle de décision",
            f"Au-delà de {reponse:.0f} réparations, chaque réparation supplémentaire "
            f"coûte plus de {prix} € à produire : elle détruit du résultat, alors même "
            "que le chiffre d'affaires continue d'augmenter. C'est pourquoi la "
            "décision se lit sur la **marge**, jamais sur le total. "
            f"Le résultat maximal vaut ici {pi_max:,.0f} €."
            .replace(",", "\u202f"),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Nombre de réparations",
        tolerance=0.002,
        indice="Dérivez le résultat, annulez la dérivée, vérifiez le signe.",
        pieges=[
            (float(marge / quad),
             "Vous avez oublié le facteur 2 : la dérivée de $q^2$ est $2q$, pas $q$."),
            (float(pi_max),
             "C'est le **montant** du résultat maximal, pas la quantité qui le "
             "réalise. L'énoncé demande un nombre de réparations."),
            (float(fixe / marge),
             "Vous avez calculé un seuil de rentabilité, pas un optimum. "
             "Couvrir ses coûts et maximiser le résultat sont deux questions "
             "différentes."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dériver un polynôme",
        "2️⃣ Règle du produit",
        "3️⃣ Tableau de variations",
        "4️⃣ Le résultat de l'atelier",
    ]
)

with onglets[0]:
    st.subheader("La fonction dérivée")
    executer("s9_derivee", gen_derivee)

with onglets[1]:
    st.subheader("Dériver un produit")
    executer("s9_produit", gen_produit)

with onglets[2]:
    st.subheader("Du signe de f' aux variations de f")
    executer("s9_variations", gen_variations)

with onglets[3]:
    st.subheader("Maximiser le résultat de l'atelier")
    executer("s9_atelier", gen_atelier)

st.markdown("---")
st.caption(
    "Semestre — séance n°9 : La fonction dérivée et les variations · "
    "Fil rouge G : l'atelier municipal · Sciences Po."
)
