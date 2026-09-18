"""Série S7 — Le logarithme népérien. Fil rouge F : la dette (clôture)."""

import math
import random

import streamlit as st

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S7 | Logarithme népérien", page_icon="🔓", layout="wide")

st.title("🔓 S7 — Le logarithme népérien")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Utiliser les propriétés du logarithme, **résoudre une équation dont l'inconnue est
en exposant**, calculer un **temps de doublement** et un **taux de croissance annuel
moyen**.

### 🧠 Trois fois, nous avons buté sur le même obstacle
Le seuil de Mélodia, le franchissement d'un cap, le doublement de la dette : à chaque
fois, l'inconnue était **en exposant** et aucune manipulation algébrique ne pouvait
l'atteindre. Le logarithme est l'outil qui défait l'exponentielle — et c'est sa seule
raison d'être.

### 💰 Fil rouge F — La dette (clôture)
La dette est passée de **85 M€** (2020) à **112 M€** (2025). Écrite en continu :
$D(t) = 85\\,e^{0{,}0392\\,t}$.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 7")
    st.markdown("**Définition**")
    st.latex(r"\ln(e^{a}) = a \qquad e^{\ln a} = a \quad (a > 0)")
    st.markdown("**L'équation fonctionnelle**")
    st.latex(r"\ln(ab) = \ln a + \ln b")
    st.markdown("**Les propriétés qui en découlent**")
    st.latex(r"\ln\!\left(\frac{a}{b}\right) = \ln a - \ln b \qquad "
             r"\ln(a^{n}) = n \ln a")
    st.latex(r"\ln 1 = 0 \qquad \ln e = 1")
    st.error(
        "**L'erreur interdite**\n\n"
        r"$\ln(a+b) \neq \ln a + \ln b$"
        "\n\nCe sont les **produits** qui deviennent des sommes."
    )
    st.info("**Valeurs utiles**\n\n$\\ln 2 \\approx 0{,}693$ · "
            "$\\ln 10 \\approx 2{,}303$")

GRANDEURS = [
    ("la dette de Villeneuve", "M€"),
    ("les abonnés de Mélodia", "abonnés"),
    ("le stock de logements vacants", "logements"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Propriétés du logarithme --------------------------------------------


def gen_proprietes() -> Exercice:
    modele = random.choice(["produit", "quotient", "puissance"])
    a = random.choice([2, 3, 5, 7])
    b = random.choice([2, 3, 4, 6])
    n = random.choice([2, 3, 4, 5])

    if modele == "produit":
        expression = rf"\ln({a} \times {b})"
        reponse = math.log(a * b)
        regle = r"\ln(ab) = \ln a + \ln b"
        detail = (f"$\\ln {a} + \\ln {b} \\approx {math.log(a):.4f} + "
                  f"{math.log(b):.4f}$")
        piege = (math.log(a) * math.log(b),
                 "Vous avez **multiplié** les logarithmes. La règle transforme le "
                 "produit en **somme**.")
    elif modele == "quotient":
        expression = rf"\ln\!\left(\frac{{{a*b}}}{{{b}}}\right)"
        reponse = math.log(a)
        regle = r"\ln\!\left(\frac{a}{b}\right) = \ln a - \ln b"
        detail = (f"$\\ln {a*b} - \\ln {b} \\approx {math.log(a*b):.4f} - "
                  f"{math.log(b):.4f}$")
        piege = (math.log(a * b) / math.log(b),
                 "Vous avez **divisé** les logarithmes. Le quotient devient une "
                 "**différence**.")
    else:
        expression = rf"\ln({a}^{{{n}}})"
        reponse = n * math.log(a)
        regle = r"\ln(a^{n}) = n \ln a"
        detail = f"${n} \\times \\ln {a} \\approx {n} \\times {math.log(a):.4f}$"
        piege = (math.log(a) ** n,
                 "Vous avez élevé le logarithme à la puissance. L'exposant "
                 "**descend en facteur** — et c'est précisément cette propriété qui "
                 "rend le logarithme utile.")

    enonce = f"""
> Calculez, à l'aide des propriétés du logarithme :
>
> $$ {expression} $$
>
> Donnez une valeur approchée à $0{{,}}01$ près.
"""

    etapes = [
        Etape(
            "Identifier — le logarithme descend d'un cran",
            "Une puissance devient un produit, un produit devient une somme, un "
            "quotient devient une différence. Toutes ces règles découlent d'une "
            "seule, l'équation fonctionnelle $\\ln(ab) = \\ln a + \\ln b$.",
        ),
        Etape("Appliquer la règle", "", regle),
        Etape("Calculer", detail, rf"\approx {reponse:.4f}"),
        Etape(
            "Vérifier — le calcul direct",
            "La propriété n'a pas changé le résultat, elle a changé la **forme**. "
            "Et c'est cette forme — une somme ou un produit plutôt qu'une puissance — "
            "qui rend soluble une équation qui ne l'était pas.",
        ),
        Etape(
            "Interpréter",
            "C'est aussi la raison pour laquelle les sciences sociales passent "
            "souvent leurs séries en logarithme : une croissance multiplicative "
            "devient additive, donc linéaire, donc lisible sur un graphique et "
            "estimable par une droite.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur",
        tolerance=0.01,
        indice="Repérez l'opération de départ : produit, quotient ou puissance.",
        pieges=[piege],
    )


# --- 2. Résoudre avec l'inconnue en exposant -------------------------------


def gen_inconnue_exposant() -> Exercice:
    grandeur, unite = random.choice(GRANDEURS)
    depart = random.choice([85, 120, 12_400, 9_500])
    taux = random.choice([3, 4, 5, 8])
    cible_facteur = random.choice([1.5, 2, 2.5, 3])
    cm = 1 + taux / 100
    cible = depart * cible_facteur
    reponse = math.log(cible_facteur) / math.log(cm)

    enonce = f"""
> {grandeur.capitalize()} vaut aujourd'hui **{depart:,} {unite}** et progresse de
> **{taux} % par an**.
>
> Au bout de combien d'années atteindra-t-elle **{cible:,.0f} {unite}** ?
> Donnez le nombre d'années (non entier) à $0{{,}}01$ près.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — l'inconnue est en exposant",
            "Aucune opération algébrique ordinaire — addition, division, "
            "factorisation — ne peut atteindre une inconnue placée en exposant. "
            "C'est exactement la situation qui appelle le logarithme.",
            rf"{depart} \times ({cm})^n = {cible:.0f}",
        ),
        Etape(
            "Isoler la puissance",
            "Première étape indispensable : le logarithme ne pourra rien tant que le "
            "facteur multiplicatif est là.",
            rf"({cm})^n = \frac{{{cible:.0f}}}{{{depart}}} = {cible_facteur}",
        ),
        Etape(
            "Appliquer le logarithme pour faire descendre l'exposant",
            "C'est la propriété $\\ln(a^n) = n \\ln a$ qui fait tout le travail : "
            "l'exposant devient un simple facteur, et l'équation redevient du "
            "premier degré.",
            rf"n \ln({cm}) = \ln({cible_facteur}) \iff "
            rf"n = \frac{{\ln({cible_facteur})}}{{\ln({cm})}} "
            rf"= \frac{{{math.log(cible_facteur):.4f}}}{{{math.log(cm):.4f}}} "
            rf"\approx {reponse:.2f}",
        ),
        Etape(
            "Vérifier",
            f"${depart} \\times ({cm})^{{{reponse:.2f}}} \\approx "
            f"{depart * cm**reponse:,.0f}$ {unite}. ✓ On retrouve bien la cible."
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — le résultat ne dépend pas du niveau de départ",
            f"Le montant initial a disparu du calcul final : seuls comptent le taux "
            f"et le **facteur** visé. Multiplier par {cible_facteur} prend "
            f"{reponse:.1f} ans à ce rythme, que l'on parte de 85 M€ ou de 12 400 "
            "abonnés. C'est ce qui donne un sens à la notion de temps de doublement.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Nombre d'années",
        unite="ans",
        tolerance=0.005,
        indice="Isolez la puissance, puis appliquez le logarithme aux deux membres.",
        pieges=[
            (math.log(cible) / math.log(depart),
             "Vous avez appliqué le logarithme sans avoir isolé la puissance. "
             "Divisez d'abord par la valeur de départ."),
            (float(cible_facteur - 1) * 100 / taux,
             "Vous avez raisonné en évolution **linéaire**. Le taux porte chaque "
             "année sur la valeur courante, d'où le passage par le logarithme."),
        ],
    )


# --- 3. Temps de doublement -------------------------------------------------


def gen_doublement() -> Exercice:
    dette0 = random.choice([85, 100, 112])
    k = random.choice([0.0296, 0.0392, 0.0488, 0.0583])
    taux_equivalent = (math.exp(k) - 1) * 100
    reponse = math.log(2) / k

    enonce = f"""
> **La dette de Villeneuve** s'écrit en continu
>
> $$ D(t) = {dette0}\\,e^{{{str(k).replace('.', ',')}\\,t}} $$
>
> En combien de temps la dette **double-t-elle** ?
> Donnez le nombre d'années à $0{{,}}01$ près.
"""

    etapes = [
        Etape(
            "Identifier — doubler, c'est atteindre le double",
            f"On cherche $t$ tel que $D(t) = 2 \\times {dette0} = {2*dette0}$. "
            "L'écriture en exponentielle rend l'équation particulièrement simple, "
            "parce que le logarithme est exactement sa fonction inverse.",
            rf"{dette0}\,e^{{{k}t}} = {2*dette0}",
        ),
        Etape(
            "Simplifier puis appliquer le logarithme",
            f"Le montant initial se simplifie des deux côtés — c'est lui qui fera "
            "disparaître toute dépendance au niveau de départ.",
            rf"e^{{{k}t}} = 2 \iff {k}t = \ln 2 \approx {math.log(2):.4f}",
        ),
        Etape(
            "Résoudre",
            "",
            rf"t = \frac{{\ln 2}}{{{k}}} \approx \frac{{{math.log(2):.4f}}}{{{k}}} "
            rf"\approx {reponse:.2f}\ \text{{ans}}",
        ),
        Etape(
            "Vérifier",
            f"$D({reponse:.2f}) = {dette0} \\times e^{{{k} \\times {reponse:.2f}}} "
            f"\\approx {dette0 * math.exp(k*reponse):.1f}$ M€, soit bien le double de "
            f"{dette0}. ✓",
        ),
        Etape(
            "Interpréter — une durée caractéristique du taux",
            f"Le montant initial a disparu : le temps de doublement ne dépend **que** "
            f"du taux. À ce rythme — environ {taux_equivalent:.1f} % par an — toute "
            f"grandeur double en {reponse:.1f} ans. C'est ce qui permet de comparer "
            "d'un seul chiffre des dynamiques portant sur des grandeurs sans "
            "commune mesure.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Temps de doublement",
        unite="ans",
        tolerance=0.005,
        indice="Écrivez l'équation du doublement, simplifiez par le montant initial.",
        pieges=[
            (float(2 / k),
             "Vous avez divisé 2 par le coefficient. C'est $\\ln 2$ qu'il faut "
             "diviser, pas 2."),
            (float(math.log(2 * dette0) / k),
             "Le montant initial se **simplifie** des deux côtés avant l'application "
             "du logarithme : il ne doit pas rester dedans."),
            (float(100 / taux_equivalent),
             "Vous avez utilisé une règle approchée. Ici le calcul exact est "
             "demandé."),
        ],
    )


# --- 4. Taux de croissance annuel moyen ------------------------------------


def gen_taux_moyen() -> Exercice:
    depart = random.choice([85, 120, 200, 450])
    facteur = random.choice([1.25, 1.32, 1.45, 1.6])
    arrivee = round(depart * facteur)
    annees = random.choice([4, 5, 6, 8])
    reponse = ((arrivee / depart) ** (1 / annees) - 1) * 100

    enonce = f"""
> **La dette de Villeneuve** est passée de **{depart} M€** à **{arrivee} M€** en
> **{annees} ans**.
>
> Quel **taux annuel moyen** cela représente-t-il ? Donnez le taux en pourcentage,
> à $0{{,}}01$ près.
"""

    naif = 100 * (arrivee - depart) / depart / annees

    etapes = [
        Etape(
            "Identifier — ce n'est pas une moyenne arithmétique",
            f"La tentation est de calculer la hausse totale "
            f"({100*(arrivee-depart)/depart:.1f} %) et de la diviser par {annees}. "
            "C'est faux, pour la raison vue en pré-rentrée 5 : les taux ne "
            "s'additionnent pas, les coefficients se multiplient.",
        ),
        Etape(
            "Poser l'équation du taux moyen",
            f"Le taux moyen $\\bar t$ est celui qui, appliqué {annees} fois de suite, "
            "produirait la même évolution globale.",
            rf"(1 + \bar t)^{{{annees}}} = \frac{{{arrivee}}}{{{depart}}} "
            rf"= {arrivee/depart:.4f}",
        ),
        Etape(
            "Résoudre — l'inconnue est dans la base, pas en exposant",
            f"Ici on prend la racine ${annees}$-ième, ce qui revient à élever à la "
            f"puissance $\\frac{{1}}{{{annees}}}$.",
            rf"1 + \bar t = ({arrivee/depart:.4f})^{{1/{annees}}} "
            rf"\approx {(arrivee/depart)**(1/annees):.5f} "
            rf"\quad\Rightarrow\quad \bar t \approx {reponse:.2f}\,\%",
        ),
        Etape(
            "Vérifier",
            f"${depart} \\times (1 + {reponse/100:.4f})^{{{annees}}} \\approx "
            f"{depart * (1 + reponse/100)**annees:.1f}$ M€. ✓ "
            f"On retrouve bien {arrivee} M€.",
        ),
        Etape(
            "Interpréter — l'écart avec la moyenne naïve",
            f"La moyenne arithmétique donnerait {naif:.2f} % par an, contre "
            f"{reponse:.2f} % pour le taux réel. Elle **surestime** toujours, parce "
            "qu'elle ignore que les hausses des dernières années portent sur une base "
            "déjà accrue. Sur une série longue, l'écart devient substantiel.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux annuel moyen",
        unite="%",
        tolerance=0.005,
        indice="Cherchez le taux qui, répété, donne la même évolution globale.",
        pieges=[
            (float(naif),
             "Vous avez divisé la hausse totale par le nombre d'années : c'est une "
             "moyenne **arithmétique**, qui surestime systématiquement le taux réel."),
            (float(100 * (arrivee - depart) / depart),
             "C'est l'évolution **totale** sur la période, pas le taux annuel."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Propriétés du logarithme",
        "2️⃣ L'inconnue en exposant",
        "3️⃣ Temps de doublement",
        "4️⃣ Taux annuel moyen",
    ]
)

with onglets[0]:
    st.subheader("Produits en sommes, puissances en produits")
    executer("s7_proprietes", gen_proprietes)

with onglets[1]:
    st.subheader("Débloquer une équation qui résistait")
    executer("s7_exposant", gen_inconnue_exposant)

with onglets[2]:
    st.subheader("En combien de temps la dette double-t-elle ?")
    executer("s7_doublement", gen_doublement)

with onglets[3]:
    st.subheader("Ce n'est pas une moyenne arithmétique")
    executer("s7_taux_moyen", gen_taux_moyen)

st.markdown("---")
st.caption(
    "Semestre — séance n°7 : Le logarithme népérien · "
    "Fil rouge F : la dette de Villeneuve · Sciences Po."
)
