"""Série S7 — Le logarithme népérien. Fil rouge F : la dette (clôture).

Variation sur trois axes (cf. `contextes.py`) : le contexte, la notation et
la **forme** de la donnée — taux en pourcentage, coefficient multiplicateur,
écriture continue, ou indice base 100. La méthode, elle, ne change pas : dès
que l'inconnue est en exposant, c'est le logarithme qui la fait descendre.
"""

import math
import random

import streamlit as st

import contextes as cx
from contextes import latex_nombre as L
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


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


def _facteur(valeur) -> str:
    """« 3 » plutôt que « 3,0 », « 1,5 » quand la décimale existe."""
    return _fr(valeur, 0 if float(valeur).is_integer() else 1)


# --- 1. Propriétés du logarithme --------------------------------------------


def gen_proprietes() -> Exercice:
    modele = random.choice(
        ["produit", "quotient", "puissance", "inverse", "combinee"]
    )
    a = random.choice([2, 3, 5, 7])
    b = random.choice([facteur for facteur in (2, 3, 4, 6) if facteur != a])
    n = random.choice([2, 3, 4, 5])

    if modele == "inverse":
        expression = rf"\ln\!\left(\frac{{1}}{{{a}}}\right)"
        reponse = -math.log(a)
        regle = r"\ln\!\left(\frac{1}{a}\right) = -\ln a"
        detail = (
            f"$\\ln 1 - \\ln {a} = 0 - {L(round(math.log(a), 4))}$ : c'est le cas "
            f"particulier du quotient, avec $\\ln 1 = 0$."
        )
        piege = (
            1 / math.log(a),
            "Vous avez pris l'**inverse du logarithme**. C'est le logarithme de "
            "l'inverse qui est demandé, et il vaut l'**opposé** : $-\\ln a$.",
        )
    elif modele == "combinee":
        expression = rf"\ln({a}^{{{n}}} \times {b})"
        reponse = n * math.log(a) + math.log(b)
        regle = r"\ln(a^{n} b) = n \ln a + \ln b"
        detail = (
            f"Deux règles s'enchaînent : le produit devient une somme, puis "
            f"l'exposant descend en facteur. "
            f"${n} \\times \\ln {a} + \\ln {b} \\approx "
            f"{_fr(n * math.log(a), 4)} + {_fr(math.log(b), 4)}$"
        )
        piege = (
            n * math.log(a) * math.log(b),
            "Vous avez multiplié les deux logarithmes. Un **produit** à l'intérieur "
            "devient une **somme** à l'extérieur.",
        )
    elif modele == "produit":
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
    ctx = cx.tirer(cx.MONETAIRES + cx.EFFECTIFS)
    depart = random.choice(
        [85, 120, 640] if ctx.monetaire else [12_400, 9_500, 6_800]
    )
    taux = random.choice([3, 4, 5, 8])
    cible_facteur = random.choice([1.5, 2, 2.5, 3])
    cm = 1 + taux / 100
    cible = depart * cible_facteur
    reponse = math.log(cible_facteur) / math.log(cm)
    presentation = random.choice(["taux", "coefficient", "cible_relative"])
    unite = ctx.unite

    if presentation == "taux":
        description = cx.phrase_taux(taux)
        objectif = f"atteindre **{_fr(cible, 0)} {unite}**"
    elif presentation == "coefficient":
        description = cx.phrase_coefficient(cm, periode="chaque année")
        objectif = f"atteindre **{_fr(cible, 0)} {unite}**"
    else:
        description = cx.phrase_taux(taux)
        objectif = (
            f"avoir été **multiplié par {_facteur(cible_facteur)}** par rapport à "
            "aujourd'hui"
        )

    enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant s'élève aujourd'hui à **{_fr(depart, 0)}
> {unite}** et {description}.
>
> Au bout de combien d'années doit-on s'attendre à {objectif} ?
> Donnez le nombre d'années (non entier) à $0{{,}}01$ près.
"""

    etapes = [
        Etape(
            "Identifier — l'inconnue est en exposant",
            "Aucune opération algébrique ordinaire — addition, division, "
            "factorisation — ne peut atteindre une inconnue placée en exposant. "
            "C'est exactement la situation qui appelle le logarithme.",
            rf"{L(depart)} \times ({L(cm)})^n = {L(cible, 0)}",
        ),
        Etape(
            "Isoler la puissance",
            "Première étape indispensable : le logarithme ne pourra rien tant que le "
            "facteur multiplicatif est là.",
            rf"({L(cm)})^n = \frac{{{L(cible, 0)}}}{{{L(depart)}}} = {L(cible_facteur)}",
        ),
        Etape(
            "Appliquer le logarithme pour faire descendre l'exposant",
            "C'est la propriété $\\ln(a^n) = n \\ln a$ qui fait tout le travail : "
            "l'exposant devient un simple facteur, et l'équation redevient du "
            "premier degré.",
            rf"n \ln({L(cm)}) = \ln({L(cible_facteur)}) \iff "
            rf"n = \frac{{\ln({L(cible_facteur)})}}{{\ln({L(cm)})}} "
            rf"= \frac{{{L(round(math.log(cible_facteur), 4))}}}"
            rf"{{{L(round(math.log(cm), 4))}}} \approx {L(round(reponse, 2))}",
        ),
        Etape(
            "Vérifier",
            f"${L(depart)} \\times ({L(cm)})^{{{L(round(reponse, 2))}}} \\approx "
            f"{L(depart * cm**reponse, 0)}$ {unite}. ✓ On retrouve bien la cible.",
        ),
        Etape(
            "Interpréter — le résultat ne dépend pas du niveau de départ",
            f"Le montant initial a disparu du calcul final : seuls comptent le taux "
            f"et le **facteur** visé. Multiplier par {_facteur(cible_facteur)} prend "
            f"{_fr(reponse, 1)} ans à ce rythme, quel que soit le niveau de "
            "départ. C'est ce qui donne un sens à la notion de temps de doublement.",
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
    ctx = cx.tirer(cx.MONETAIRES)
    notation = random.choice(["D", "V", "f"])
    var = random.choice(["t", "x"])
    depart = random.choice([85, 100, 112, 64])
    presentation = random.choice(["continue", "taux", "coefficient"])

    if presentation == "continue":
        k = random.choice([0.0296, 0.0392, 0.0488, 0.0583])
        coef = math.exp(k)
        taux_equivalent = (coef - 1) * 100
        enonce = f"""
> **{_maj(ctx.sujet)}.** Son évolution s'écrit en continu
>
> $$ {notation}({var}) = {L(depart)}\\,e^{{{L(k)}\\,{var}}} $$
>
> En combien de temps ce montant **double-t-il** ?
> Donnez le nombre d'années à $0{{,}}01$ près.
"""
        origine_k = (
            f"Le coefficient ${L(k)}$ est directement lisible dans l'exposant : "
            "l'énoncé fait la moitié du travail."
        )
    elif presentation == "taux":
        taux_equivalent = random.choice([3, 4, 5, 6])
        coef = 1 + taux_equivalent / 100
        k = math.log(coef)
        enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant s'élève à **{_fr(depart, 0)} {ctx.unite}** et
> {cx.phrase_taux(taux_equivalent)}.
>
> En combien de temps **double-t-il** ? Donnez le nombre d'années à $0{{,}}01$ près.
"""
        origine_k = (
            f"Le taux n'est pas le coefficient de l'exposant : il faut d'abord écrire "
            f"l'évolution en continu, avec $k = \\ln({L(coef)}) \\approx "
            f"{L(round(k, 4))}$. On peut aussi rester en écriture multiplicative et "
            f"résoudre $({L(coef)})^n = 2$ — les deux chemins donnent le même nombre."
        )
    else:
        taux_equivalent = random.choice([3, 4, 5, 6])
        coef = 1 + taux_equivalent / 100
        k = math.log(coef)
        enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant s'élève à **{_fr(depart, 0)} {ctx.unite}** et est
> **multiplié par ${L(coef)}$ chaque année**.
>
> En combien de temps **double-t-il** ? Donnez le nombre d'années à $0{{,}}01$ près.
"""
        origine_k = (
            f"Avec un coefficient multiplicateur, l'équation du doublement s'écrit "
            f"$({L(coef)})^n = 2$. En passant au logarithme, "
            f"$n = \\dfrac{{\\ln 2}}{{\\ln({L(coef)})}}$, et $\\ln({L(coef)}) "
            f"\\approx {L(round(k, 4))}$ est exactement le $k$ de l'écriture continue."
        )

    reponse = math.log(2) / k

    etapes = [
        Etape(
            "Identifier — doubler, c'est atteindre le double",
            f"On cherche la durée au bout de laquelle le montant vaut "
            f"$2 \\times {L(depart)} = {L(2 * depart)}$. {origine_k}",
        ),
        Etape(
            "Simplifier : le niveau de départ s'en va",
            "Le montant initial se simplifie des deux côtés — c'est lui qui fera "
            "disparaître toute dépendance au niveau de départ.",
            rf"e^{{{L(round(k, 4))}\,n}} = 2 \iff {L(round(k, 4))}\,n = \ln 2 "
            rf"\approx {L(round(math.log(2), 4))}",
        ),
        Etape(
            "Résoudre",
            "",
            rf"n = \frac{{\ln 2}}{{{L(round(k, 4))}}} \approx "
            rf"\frac{{{L(round(math.log(2), 4))}}}{{{L(round(k, 4))}}} \approx "
            rf"{L(round(reponse, 2))}\ \text{{ans}}",
        ),
        Etape(
            "Vérifier",
            f"${L(depart)} \\times ({L(coef)})^{{{L(round(reponse, 2))}}} \\approx "
            f"{L(depart * coef**reponse, 1)}$ {ctx.unite}, soit bien le double de "
            f"{_fr(depart, 0)}. ✓",
        ),
        Etape(
            "Interpréter — une durée caractéristique du taux",
            f"Le montant initial a disparu : le temps de doublement ne dépend **que** "
            f"du taux. À ce rythme — environ {_fr(taux_equivalent, 1)} % par an — "
            f"toute grandeur double en {_fr(reponse, 1)} ans. C'est ce qui permet de "
            "comparer d'un seul chiffre des dynamiques portant sur des grandeurs sans "
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
        indice="Écrivez l'équation du doublement, puis simplifiez par le montant "
        "initial : il disparaît toujours.",
        pieges=[
            (
                float(2 / k),
                "Vous avez divisé 2 par le coefficient. C'est $\\ln 2$ qu'il faut "
                "diviser, pas 2.",
            ),
            (
                float(math.log(2 * depart) / k),
                "Le montant initial se **simplifie** des deux côtés avant "
                "l'application du logarithme : il ne doit pas rester dedans.",
            ),
            (
                float(100 / taux_equivalent),
                "Vous avez utilisé la règle approchée « 70 divisé par le taux » (ou "
                "une variante). Ici le calcul exact est demandé.",
            ),
        ],
    )


# --- 4. Taux de croissance annuel moyen ------------------------------------


def gen_taux_moyen() -> Exercice:
    ctx = cx.tirer(cx.MONETAIRES)
    depart = random.choice([85, 120, 200, 450])
    facteur = random.choice([1.25, 1.32, 1.45, 1.6])
    arrivee = round(depart * facteur)
    annees = random.choice([4, 5, 6, 8])
    rapport = arrivee / depart
    reponse = (rapport ** (1 / annees) - 1) * 100
    naif = 100 * (arrivee - depart) / depart / annees
    presentation = random.choice(["valeurs", "indice", "croissance_totale"])

    if presentation == "valeurs":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant est passé de **{_fr(depart, 0)} {ctx.unite}** à
> **{_fr(arrivee, 0)} {ctx.unite}** en **{annees} ans**.
>
> Quel **taux annuel moyen** cela représente-t-il ? Donnez le taux en pourcentage,
> à $0{{,}}01$ près.
"""
        lecture = (
            f"Le rapport entre les deux valeurs vaut "
            f"$\\dfrac{{{L(arrivee)}}}{{{L(depart)}}} = {L(round(rapport, 4))}$ : "
            "c'est l'évolution **globale** sur toute la période."
        )
    elif presentation == "indice":
        indice = round(100 * rapport, 1)
        enonce = f"""
> **{_maj(ctx.sujet)}.** En base 100 l'année de référence, l'indice de ce montant
> atteint **{_fr(indice, 1)}** au bout de **{annees} ans**.
>
> Quel **taux annuel moyen** cela représente-t-il ? Donnez le taux en pourcentage,
> à $0{{,}}01$ près.
"""
        lecture = (
            f"Un indice de {_fr(indice, 1)} en base 100 signifie que le montant a été "
            f"multiplié par $\\dfrac{{{L(round(indice, 1))}}}{{100}} = "
            f"{L(round(rapport, 4))}$ sur l'ensemble de la période. L'indice n'est "
            "qu'une autre écriture du coefficient multiplicateur."
        )
    else:
        hausse = 100 * (rapport - 1)
        enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant a augmenté de **{_fr(hausse, 1)} % en
> {annees} ans**.
>
> Quel **taux annuel moyen** cela représente-t-il ? Donnez le taux en pourcentage,
> à $0{{,}}01$ près.
"""
        lecture = (
            f"Une hausse de {_fr(hausse, 1)} % correspond au coefficient global "
            f"${L(round(rapport, 4))}$. Attention : ce pourcentage porte sur la "
            "**période entière**, pas sur une année."
        )

    etapes = [
        Etape(
            "Identifier — ce n'est pas une moyenne arithmétique",
            f"{lecture} La tentation est de diviser cette hausse globale par "
            f"{annees}. C'est faux, pour la raison vue en pré-rentrée 5 : les taux ne "
            "s'additionnent pas, les coefficients se multiplient.",
        ),
        Etape(
            "Poser l'équation du taux moyen",
            f"Le taux moyen $\\bar t$ est celui qui, appliqué {annees} fois de suite, "
            "produirait la même évolution globale.",
            rf"(1 + \bar t)^{{{annees}}} = {L(round(rapport, 4))}",
        ),
        Etape(
            "Résoudre — l'inconnue est dans la base, pas en exposant",
            f"C'est la différence avec l'exercice précédent : ici on prend la racine "
            f"${annees}$-ième, ce qui revient à élever à la puissance "
            f"$\\frac{{1}}{{{annees}}}$. Le logarithme n'est pas nécessaire.",
            rf"1 + \bar t = ({L(round(rapport, 4))})^{{1/{annees}}} \approx "
            rf"{L(round(rapport ** (1 / annees), 5))} \quad\Rightarrow\quad "
            rf"\bar t \approx {L(round(reponse, 2))}\,\%",
        ),
        Etape(
            "Vérifier",
            f"${L(depart)} \\times (1 + {L(round(reponse / 100, 4))})^{{{annees}}} "
            f"\\approx {L(depart * (1 + reponse / 100) ** annees, 1)}$ "
            f"{ctx.unite}. ✓ On retrouve bien le niveau d'arrivée.",
        ),
        Etape(
            "Interpréter — l'écart avec la moyenne naïve",
            f"La moyenne arithmétique donnerait {_fr(naif, 2)} % par an, contre "
            f"{_fr(reponse, 2)} % pour le taux réel. Elle **surestime** toujours, "
            "parce qu'elle ignore que les hausses des dernières années portent sur "
            "une base déjà accrue. Sur une série longue, l'écart devient substantiel.",
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
            (
                float(naif),
                "Vous avez divisé la hausse totale par le nombre d'années : c'est une "
                "moyenne **arithmétique**, qui surestime systématiquement le taux "
                "réel.",
            ),
            (
                float(100 * (rapport - 1)),
                "C'est l'évolution **totale** sur la période, pas le taux annuel.",
            ),
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
