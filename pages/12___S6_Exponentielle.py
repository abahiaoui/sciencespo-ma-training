"""Série S6 — La fonction exponentielle. Fil rouge F : la dette de Villeneuve."""

import math
import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S6 | Exponentielle", page_icon="📈", layout="wide")

x = sp.Symbol("x")

st.title("📈 S6 — La fonction exponentielle")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Utiliser les propriétés de l'exponentielle, passer d'un **taux annuel** à une écriture
continue, et mesurer l'écart entre une croissance exponentielle et l'intuition
linéaire.

### 🧠 Du discret au continu
Une suite géométrique ne donne de valeur qu'aux rangs entiers. L'exponentielle
prolonge ce mécanisme à **tout instant** : elle permet de parler de la dette au bout
de 3,5 ans, ce qu'une suite ne permet pas. C'est le même phénomène, décrit de façon
continue.

### 💰 Fil rouge F — La dette de Villeneuve
La dette s'élevait à **85 M€** en 2020 et progresse d'environ **4 % par an**.
En 2025, elle atteint **112 M€**.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 6")
    st.markdown("**Propriétés**")
    st.latex(r"e^{a} \times e^{b} = e^{a+b}")
    st.latex(r"\frac{e^{a}}{e^{b}} = e^{a-b} \qquad (e^{a})^{n} = e^{an}")
    st.latex(r"e^{0} = 1 \qquad e^{-a} = \frac{1}{e^{a}}")
    st.markdown("**Écriture continue d'un taux annuel**")
    st.latex(r"(1+t)^{n} = e^{k n} \quad \text{avec} \quad e^{k} = 1+t")
    st.error(
        "**L'erreur à ne pas commettre**\n\n"
        r"$e^{a+b} \neq e^{a} + e^{b}$"
        "\n\nL'exponentielle transforme les **sommes en produits**, pas en sommes."
    )
    st.info(
        "**Toujours strictement positive**\n\n"
        "$e^{x} > 0$ pour tout $x$ : une exponentielle ne s'annule jamais et ne "
        "devient jamais négative."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Propriétés de l'exponentielle --------------------------------------


def gen_proprietes() -> Exercice:
    modele = random.choice(["produit", "quotient", "puissance"])
    a = random.choice([0.5, 1, 1.5, 2])
    b = random.choice([0.5, 1, 2, 3])
    n = random.choice([2, 3, 4])

    if modele == "produit":
        expression = rf"e^{{{a}}} \times e^{{{b}}}"
        reponse = math.exp(a + b)
        regle = r"e^{a} \times e^{b} = e^{a+b}"
        detail = f"$e^{{{a}}} \\times e^{{{b}}} = e^{{{a} + {b}}} = e^{{{a+b}}}$"
        piege = (math.exp(a) + math.exp(b),
                 "Vous avez **additionné** les exponentielles. La règle dit l'inverse : "
                 "le produit d'exponentielles devient l'exponentielle d'une somme.")
    elif modele == "quotient":
        expression = rf"\frac{{e^{{{a+b}}}}}{{e^{{{b}}}}}"
        reponse = math.exp(a)
        regle = r"\frac{e^{a}}{e^{b}} = e^{a-b}"
        detail = f"$\\frac{{e^{{{a+b}}}}}{{e^{{{b}}}}} = e^{{{a+b} - {b}}} = e^{{{a}}}$"
        piege = (math.exp(a + b) / b if b else 0.0,
                 "Vous avez divisé par l'exposant. Ce sont les **exposants** qui se "
                 "soustraient, pas les valeurs.")
    else:
        expression = rf"\left(e^{{{a}}}\right)^{{{n}}}"
        reponse = math.exp(a * n)
        regle = r"(e^{a})^{n} = e^{an}"
        detail = f"$(e^{{{a}}})^{{{n}}} = e^{{{a} \\times {n}}} = e^{{{a*n}}}$"
        piege = (math.exp(a + n),
                 "Pour une puissance de puissance, les exposants se **multiplient**, "
                 "ils ne s'additionnent pas.")

    enonce = f"""
> Calculez, à l'aide des propriétés de l'exponentielle :
>
> $$ {expression} $$
>
> Donnez une valeur approchée à $0{{,}}01$ près.
"""

    etapes = [
        Etape(
            "Identifier — les règles sont celles des puissances",
            "Rien de nouveau : l'exponentielle obéit exactement aux règles des "
            "puissances vues en pré-rentrée 1. Un produit fait additionner les "
            "exposants, un quotient les soustraire, une puissance les multiplier.",
        ),
        Etape("Appliquer la règle", "", regle),
        Etape(
            "Calculer",
            detail,
            rf"\approx {reponse:.4f}",
        ),
        Etape(
            "Vérifier — le résultat est-il strictement positif ?",
            f"${reponse:.4f} > 0$. ✓ Une exponentielle est **toujours** strictement "
            "positive, quel que soit son exposant. Un résultat négatif ou nul "
            "signalerait une erreur, sans avoir besoin de refaire le calcul.",
        ),
        Etape(
            "Interpréter",
            "Ces règles ne sont pas décoratives : ce sont elles qui permettront, "
            "en séance 7, de faire descendre un exposant inconnu à l'aide du "
            "logarithme. Sans elles, la question « au bout de combien d'années ? » "
            "reste sans réponse.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur",
        tolerance=0.005,
        indice="Ce sont les règles des puissances, appliquées aux exposants.",
        pieges=[piege],
    )


# --- 2. L'erreur à ne pas commettre (QCM) ----------------------------------


def gen_erreur() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([1, 2, 4])

    bonne = f"e^{a} × e^{b}"
    options = [
        bonne,
        f"e^{a} + e^{b}",
        f"e^{a*b}",
        f"{a + b} × e",
    ]
    random.shuffle(options)

    enonce = f"""
> À quoi $e^{{{a} + {b}}}$ est-il **égal** ?
"""

    va, vb = math.exp(a), math.exp(b)

    etapes = [
        Etape(
            "Identifier — l'exponentielle transforme les sommes en produits",
            "C'est la propriété fondamentale, et le sens de la transformation est "
            "exactement inverse de celui du logarithme. Une **somme** en exposant "
            "devient un **produit** de valeurs.",
            r"e^{a+b} = e^{a} \times e^{b}",
        ),
        Etape(
            "Vérifier numériquement",
            f"$e^{{{a + b}}} \\approx {math.exp(a+b):.4f}$ · "
            f"$e^{{{a}}} \\times e^{{{b}}} \\approx {va:.4f} \\times {vb:.4f} "
            f"= {va*vb:.4f}$ ✓ · "
            f"mais $e^{{{a}}} + e^{{{b}}} \\approx {va + vb:.4f}$ ✗. "
            "Un seul test numérique suffit à écarter la mauvaise réponse.",
        ),
        Etape(
            "Vérifier — pourquoi l'intuition se trompe",
            "L'addition en exposant ressemble à une addition, donc on l'attend en "
            "sortie. Mais l'exposant compte des **multiplications** : ajouter 1 à "
            "l'exposant, c'est multiplier une fois de plus par $e$. "
            "C'est la même structure d'erreur que $(a+b)^2 \\neq a^2 + b^2$.",
        ),
        Etape(
            "Interpréter",
            "Cette propriété est la raison pour laquelle l'exponentielle décrit si "
            "bien les croissances par taux : ajouter des années dans l'exposant "
            "revient à multiplier les coefficients annuels, ce qui est exactement le "
            "mécanisme de la pré-rentrée 5.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Expression égale",
        indice="Une somme en exposant devient-elle une somme ou un produit ?",
        pieges=[
            (f"e^{a} + e^{b}",
             f"C'est **l'erreur interdite** de la séance. Test : $e^{{{a+b}}} \\approx "
             f"{math.exp(a+b):.2f}$ alors que $e^{{{a}}} + e^{{{b}}} \\approx "
             f"{va + vb:.2f}$."),
            (f"e^{a*b}",
             "Les exposants ne se multiplient que pour une **puissance de puissance**, "
             "$(e^a)^n$. Ici il s'agit d'une somme."),
            (f"{a + b} × e",
             "L'exposant n'est pas un facteur : $e^3$ vaut environ 20, pas 3 fois "
             "2,72."),
        ],
    )


# --- 3. Écrire un taux annuel en exponentielle -----------------------------


def gen_taux_continu() -> Exercice:
    dette0 = random.choice([85, 72, 95, 110])
    taux = random.choice([3, 4, 5, 6])
    k = math.log(1 + taux / 100)
    t = random.choice([3, 5, 8, 10])
    reponse = dette0 * math.exp(k * t)

    enonce = f"""
> **La dette de Villeneuve.** Elle s'élève à **{dette0} M€** aujourd'hui et progresse
> de **{taux} % par an**. On peut écrire son évolution sous forme continue :
>
> $$ D(t) = {dette0}\\,e^{{{k:.4f}\\,t}} $$
>
> où $t$ est le nombre d'années écoulées.
>
> Que vaudra la dette dans **{t} ans** ? Arrondissez au centième de million.
"""

    discret = dette0 * (1 + taux / 100) ** t

    etapes = [
        Etape(
            "Identifier — d'où vient le coefficient dans l'exposant",
            f"Le coefficient ${k:.4f}$ n'est pas le taux de {taux} % : c'est le nombre "
            f"qui vérifie $e^{{{k:.4f}}} = {1 + taux/100}$. Autrement dit, l'écriture "
            "continue et l'écriture par coefficient multiplicateur décrivent la même "
            "évolution, avec deux paramétrages différents.",
        ),
        Etape(
            "Substituer",
            "",
            rf"D({t}) = {dette0} \times e^{{{k:.4f} \times {t}}} "
            rf"= {dette0} \times e^{{{k*t:.4f}}} \approx {reponse:.2f}\ \text{{M€}}",
        ),
        Etape(
            "Vérifier — les deux écritures coïncident",
            f"Par le coefficient multiplicateur : "
            f"${dette0} \\times ({1 + taux/100})^{{{t}}} = {discret:.2f}$ M€. "
            f"Par l'exponentielle : ${reponse:.2f}$ M€. Identiques. ✓ "
            "Ce contrôle est le meilleur moyen de confirmer qu'on n'a pas confondu "
            "le taux et le coefficient de l'exposant.",
        ),
        Etape(
            "Interpréter — ce que le continu apporte",
            f"L'écriture exponentielle permet de calculer la dette à **n'importe quel "
            f"instant**, y compris au bout de 3,5 ans — ce qu'une suite géométrique "
            "ne permet pas. C'est ce qui la rend indispensable dès qu'on veut "
            "répondre à « quand ? » plutôt qu'à « combien la n-ième année ? ».",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Dette dans {t} ans",
        unite="M€",
        tolerance=0.002,
        indice="Remplacez $t$ par sa valeur dans l'exposant, puis calculez.",
        pieges=[
            (float(dette0 * math.exp(k) * t),
             "Vous avez multiplié par $t$ **en dehors** de l'exponentielle. "
             "Le temps est dans l'exposant."),
            (float(dette0 * (1 + t * taux / 100)),
             f"Vous avez raisonné en évolution **linéaire** : {taux} % du montant "
             "initial, répétés. Or le taux porte chaque année sur la dette courante."),
            (float(dette0 + k * t),
             "L'exponentielle multiplie, elle n'ajoute pas."),
        ],
    )


# --- 4. Pourquoi notre intuition échoue ------------------------------------


def gen_intuition() -> Exercice:
    dette0 = random.choice([85, 100, 120])
    taux = random.choice([3, 4, 5])
    horizon = random.choice([20, 25, 30, 40])
    cm = 1 + taux / 100
    reponse = dette0 * cm**horizon
    lineaire = dette0 * (1 + horizon * taux / 100)

    enonce = f"""
> **La dette de Villeneuve.** Elle vaut **{dette0} M€** aujourd'hui et progresse de
> **{taux} % par an**.
>
> Que vaudra-t-elle dans **{horizon} ans** ? Arrondissez au dixième de million.
"""

    etapes = [
        Etape(
            "Identifier — chaque année multiplie, elle n'ajoute pas",
            f"Le piège de cette question est l'horizon long : sur {horizon} ans, "
            "l'intuition linéaire devient franchement fausse, alors qu'elle restait "
            "acceptable sur trois ou quatre ans.",
        ),
        Etape(
            "Calculer",
            "",
            rf"D({horizon}) = {dette0} \times ({cm})^{{{horizon}}} "
            rf"\approx {dette0} \times {cm**horizon:.4f} \approx {reponse:.1f}"
            rf"\ \text{{M€}}",
        ),
        Etape(
            "Vérifier — comparer à l'intuition linéaire",
            f"Un raisonnement linéaire donnerait "
            f"${dette0} \\times (1 + {horizon} \\times {taux/100}) = "
            f"{lineaire:.1f}$ M€, soit un écart de "
            f"**{reponse - lineaire:.1f} M€** avec le résultat correct. "
            f"Sur {horizon} ans, l'erreur atteint "
            f"{100*(reponse - lineaire)/lineaire:.0f} % du montant.",
        ),
        Etape(
            "Interpréter — pourquoi l'exponentielle surprend toujours",
            "Sur les premières années, l'écart entre les deux raisonnements est "
            "négligeable et la croissance paraît maîtrisable. C'est ce qui rend ce "
            "mécanisme si difficile à traiter politiquement : au moment où l'écart "
            "devient visible, il est déjà considérable. "
            "La séance 7 permettra de répondre à la question complémentaire — "
            "**quand** la dette aura-t-elle doublé ?",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Dette dans {horizon} ans",
        unite="M€",
        tolerance=0.002,
        indice="Le coefficient s'applique une fois par an, sur le montant de l'année "
        "précédente.",
        pieges=[
            (float(lineaire),
             f"Vous avez ajouté {horizon} fois {taux} % du montant **initial**. "
             "Chaque année, le taux porte sur la dette de l'année précédente, qui a "
             "déjà augmenté."),
            (float(dette0 * cm),
             "Vous n'avez appliqué le coefficient qu'une seule fois."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Propriétés",
        "2️⃣ L'erreur interdite",
        "3️⃣ Taux annuel en exponentielle",
        "4️⃣ Pourquoi l'intuition échoue",
    ]
)

with onglets[0]:
    st.subheader("Les règles des puissances, appliquées à e")
    executer("s6_proprietes", gen_proprietes)

with onglets[1]:
    st.subheader("Somme en exposant, produit en sortie")
    executer("s6_erreur", gen_erreur)

with onglets[2]:
    st.subheader("Du discret au continu")
    executer("s6_continu", gen_taux_continu)

with onglets[3]:
    st.subheader("La dette à horizon long")
    executer("s6_intuition", gen_intuition)

st.markdown("---")
st.caption(
    "Semestre — séance n°6 : La fonction exponentielle · "
    "Fil rouge F : la dette de Villeneuve · Sciences Po."
)
