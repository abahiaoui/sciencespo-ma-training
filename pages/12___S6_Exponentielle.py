"""Série S6 — La fonction exponentielle. Fil rouge F : la dette de Villeneuve.

Variation sur trois axes (cf. `contextes.py`) : le contexte (dette, dotation,
loyer, chiffre d'affaires), la notation (nom de fonction et variable) et la
**forme** de la question — propriété directe ou combinée, taux donné en
pourcentage, coefficient multiplicateur, ou écriture continue déjà posée.
"""

import math
import random

import streamlit as st

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S6 | Exponentielle", page_icon="📈", layout="wide")

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

### ⚠️ Trois façons de vous donner la même croissance
Un taux (« $+4$ % par an »), un coefficient multiplicateur (« $\\times 1{,}04$ »)
ou une écriture continue (« $e^{0{,}0392\\,t}$ ») décrivent **la même** évolution.
Savoir passer de l'une à l'autre est l'objet central de la séance.
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
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


NOTATIONS = [
    cx.NotationFonction("D", "t"),
    cx.NotationFonction("f", "t"),
    cx.NotationFonction("V", "t"),
    cx.NotationFonction("g", "x"),
]


# --- 1. Propriétés de l'exponentielle --------------------------------------


def gen_proprietes() -> Exercice:
    modele = random.choice(
        ["produit", "quotient", "puissance", "inverse", "combinee"]
    )
    a = random.choice([0.5, 1, 1.5, 2])
    b = random.choice([0.5, 1, 2, 3])
    n = random.choice([2, 3, 4])

    if modele == "produit":
        expression = rf"e^{{{L(a)}}} \times e^{{{L(b)}}}"
        exposant = a + b
        regle = r"e^{a} \times e^{b} = e^{a+b}"
        detail = (
            f"$e^{{{L(a)}}} \\times e^{{{L(b)}}} = e^{{{L(a)} + {L(b)}}} "
            f"= e^{{{L(exposant)}}}$"
        )
        piege = (
            math.exp(a) + math.exp(b),
            "Vous avez **additionné** les exponentielles. La règle dit l'inverse : "
            "le produit d'exponentielles devient l'exponentielle d'une somme.",
        )
    elif modele == "quotient":
        expression = rf"\frac{{e^{{{L(a + b)}}}}}{{e^{{{L(b)}}}}}"
        exposant = a
        regle = r"\frac{e^{a}}{e^{b}} = e^{a-b}"
        detail = (
            f"$\\frac{{e^{{{L(a + b)}}}}}{{e^{{{L(b)}}}}} = "
            f"e^{{{L(a + b)} - {L(b)}}} = e^{{{L(a)}}}$"
        )
        piege = (
            math.exp(a + b) / b if b else 0.0,
            "Vous avez divisé par l'exposant. Ce sont les **exposants** qui se "
            "soustraient, pas les valeurs.",
        )
    elif modele == "puissance":
        expression = rf"\left(e^{{{L(a)}}}\right)^{{{n}}}"
        exposant = a * n
        regle = r"(e^{a})^{n} = e^{an}"
        detail = (
            f"$(e^{{{L(a)}}})^{{{n}}} = e^{{{L(a)} \\times {n}}} "
            f"= e^{{{L(exposant)}}}$"
        )
        piege = (
            math.exp(a + n),
            "Pour une puissance de puissance, les exposants se **multiplient**, "
            "ils ne s'additionnent pas.",
        )
    elif modele == "inverse":
        expression = rf"\frac{{1}}{{e^{{{L(a)}}}}}"
        exposant = -a
        regle = r"\frac{1}{e^{a}} = e^{-a}"
        detail = (
            f"$\\frac{{1}}{{e^{{{L(a)}}}}} = e^{{-{L(a)}}}$ : passer au dénominateur "
            "revient à changer le signe de l'exposant."
        )
        piege = (
            -math.exp(a),
            "Un exposant négatif ne rend pas l'exponentielle négative : "
            "$e^{-a}$ est l'**inverse** de $e^{a}$, donc un nombre entre $0$ et $1$.",
        )
    else:
        expression = (
            rf"\frac{{e^{{{L(a)}}} \times e^{{{L(b)}}}}}{{e^{{{L(b)}}}}}"
        )
        exposant = a
        regle = r"e^{a} \times e^{b} = e^{a+b} \qquad \frac{e^{a}}{e^{b}} = e^{a-b}"
        detail = (
            f"Au numérateur, $e^{{{L(a)}}} \\times e^{{{L(b)}}} = "
            f"e^{{{L(a + b)}}}$. Puis le quotient retranche : "
            f"$e^{{{L(a + b)} - {L(b)}}} = e^{{{L(a)}}}$. Les deux règles "
            "s'enchaînent sans qu'aucun calcul numérique soit nécessaire avant la fin."
        )
        piege = (
            math.exp(a + b),
            "Vous avez appliqué la première règle mais oublié le dénominateur : "
            f"il reste à retrancher ${L(b)}$ à l'exposant.",
        )

    reponse = math.exp(exposant)

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
            "exposants, un quotient les soustraire, une puissance les multiplier, "
            "un passage au dénominateur les changer de signe.",
        ),
        Etape("Appliquer la règle", "", regle),
        Etape(
            "Calculer",
            detail,
            rf"\approx {L(round(reponse, 4))}",
        ),
        Etape(
            "Vérifier — le résultat est-il strictement positif ?",
            f"${L(round(reponse, 4))} > 0$. ✓ Une exponentielle est **toujours** "
            "strictement positive, quel que soit son exposant. Un résultat négatif ou "
            "nul signalerait une erreur, sans avoir besoin de refaire le calcul.",
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
    n = random.choice([2, 3])
    if a * n == a + n:  # sinon deux options du QCM seraient identiques
        a += 1
    question = random.choice(["somme", "difference", "puissance", "oppose"])

    if question == "somme":
        enonce_math = f"e^{{{a} + {b}}}"
        bonne = f"e^{a} × e^{b}"
        fausses = [f"e^{a} + e^{b}", f"e^{a * b}", f"{a + b} × e"]
        regle = r"e^{a+b} = e^{a} \times e^{b}"
        lecture = (
            "Une **somme** en exposant devient un **produit** de valeurs. C'est la "
            "propriété fondamentale, et le sens de la transformation est exactement "
            "inverse de celui du logarithme."
        )
        messages = {
            f"e^{a} + e^{b}": (
                f"C'est **l'erreur interdite** de la séance. Test : "
                f"$e^{{{a + b}}} \\approx {L(round(math.exp(a + b), 2))}$ alors que "
                f"$e^{{{a}}} + e^{{{b}}} \\approx "
                f"{_fr(math.exp(a) + math.exp(b))}$."
            ),
            f"e^{a * b}": (
                "Les exposants ne se multiplient que pour une **puissance de "
                "puissance**, $(e^a)^n$. Ici il s'agit d'une somme."
            ),
            f"{a + b} × e": (
                "L'exposant n'est pas un facteur : $e^3$ vaut environ 20, pas 3 fois "
                "2,72."
            ),
        }
    elif question == "difference":
        enonce_math = f"e^{{{a + b} - {b}}}"
        bonne = f"e^{a + b} / e^{b}"
        fausses = [f"e^{a + b} - e^{b}", f"e^{a + b} × e^{b}", f"e^{a} - {b}"]
        regle = r"e^{a-b} = \frac{e^{a}}{e^{b}}"
        lecture = (
            "Une **différence** en exposant devient un **quotient**. C'est la même "
            "règle que pour le produit, lue à l'envers."
        )
        messages = {
            f"e^{a + b} - e^{b}": (
                "Même erreur de structure que pour la somme : une différence "
                "d'exposants donne un **quotient**, jamais une différence de valeurs."
            ),
            f"e^{a + b} × e^{b}": (
                "Multiplier reviendrait à **ajouter** les exposants. Ici l'exposant "
                "est une soustraction."
            ),
            f"e^{a} - {b}": (
                "L'exposant ne se coupe pas en deux morceaux dont l'un sortirait de "
                "l'exponentielle."
            ),
        }
    elif question == "puissance":
        enonce_math = f"\\left(e^{{{a}}}\\right)^{{{n}}}"
        bonne = f"e^{a * n}"
        fausses = [f"e^{a + n}", f"{n} × e^{a}", f"e^{a} + {n}"]
        regle = r"(e^{a})^{n} = e^{a \times n}"
        lecture = (
            "Une **puissance de puissance** multiplie les exposants : élever au cube, "
            "c'est multiplier trois fois par lui-même, donc ajouter trois fois "
            "l'exposant."
        )
        messages = {
            f"e^{a + n}": (
                "Les exposants s'additionnent pour un **produit** d'exponentielles, "
                "pas pour une puissance."
            ),
            f"{n} × e^{a}": (
                f"Élever à la puissance {n}, ce n'est pas multiplier par {n} : "
                f"$(e^{{{a}}})^{{{n}}} \\approx {L(round(math.exp(a * n), 2))}$ contre "
                f"{_fr(n * math.exp(a))}."
            ),
            f"e^{a} + {n}": "L'exposant ne se répercute pas en une addition "
            "extérieure : élever à une puissance agit **dans** l'exposant.",
        }
    else:
        enonce_math = f"e^{{-{a}}}"
        bonne = f"1 / e^{a}"
        fausses = [f"-e^{a}", f"e^{a} - 1", "0"]
        regle = r"e^{-a} = \frac{1}{e^{a}}"
        lecture = (
            "Un exposant **négatif** donne l'**inverse**, jamais un nombre négatif : "
            "l'exponentielle reste strictement positive en toute circonstance."
        )
        messages = {
            f"-e^{a}": (
                f"$e^{{-{a}}} \\approx {L(round(math.exp(-a), 4))}$ : c'est un nombre "
                "**positif**, compris entre $0$ et $1$. Le signe de l'exposant ne "
                "passe pas devant l'exponentielle."
            ),
            f"e^{a} - 1": "L'exposant négatif n'est pas une soustraction.",
            "0": (
                "Une exponentielle ne s'annule jamais, aussi négatif que soit "
                "l'exposant : elle s'approche de $0$ sans l'atteindre."
            ),
        }

    options = [bonne] + fausses
    random.shuffle(options)

    enonce = f"""
> À quoi ${enonce_math}$ est-il **égal** ?
"""

    etapes = [
        Etape(
            "Identifier — quelle règle est en jeu",
            lecture,
            regle,
        ),
        Etape(
            "Vérifier numériquement",
            "Un seul test numérique suffit à écarter les mauvaises réponses : "
            f"$e^{{1}} \\approx {L(round(math.e, 4))}$, $e^{{2}} \\approx "
            f"{L(round(math.exp(2), 4))}$, $e^{{3}} \\approx "
            f"{L(round(math.exp(3), 4))}$. "
            "Calculer les deux membres sur ces valeurs tranche immédiatement.",
        ),
        Etape(
            "Vérifier — pourquoi l'intuition se trompe",
            "L'opération lue dans l'exposant (somme, différence, puissance) ressemble "
            "à ce qu'on attend en sortie. Mais l'exposant compte des "
            "**multiplications** : ajouter 1 à l'exposant, c'est multiplier une fois "
            "de plus par $e$. C'est la même structure d'erreur que "
            "$(a+b)^2 \\neq a^2 + b^2$.",
        ),
        Etape(
            "Interpréter",
            "Ces propriétés sont la raison pour laquelle l'exponentielle décrit si "
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
        indice="Que devient l'opération lue dans l'exposant, une fois sortie de "
        "l'exponentielle ?",
        pieges=[(fausse, messages[fausse]) for fausse in fausses],
    )


# --- 3. Écrire un taux annuel en exponentielle -----------------------------


def gen_taux_continu() -> Exercice:
    ctx = cx.tirer(cx.MONETAIRES)
    notation = random.choice(NOTATIONS)
    var = notation.var
    depart = random.choice([85, 72, 95, 110, 64])
    taux = random.choice([3, 4, 5, 6])
    coef = 1 + taux / 100
    k = math.log(coef)
    horizon = random.choice([3, 5, 8, 10])
    reponse = depart * math.exp(k * horizon)
    discret = depart * coef**horizon
    presentation = random.choice(["continue", "coefficient", "taux"])

    if presentation == "continue":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant s'élève aujourd'hui à **{_fr(depart, 0)}
> {ctx.unite}**, et son évolution s'écrit sous forme continue
>
> $$ {notation.de()} = {L(depart)}\\,e^{{{L(round(k, 4))}\\,{var}}} $$
>
> où ${var}$ est le nombre d'années écoulées.
>
> Que vaudra-t-il dans **{horizon} ans** ? Arrondissez au centième.
"""
        origine_k = (
            f"Le coefficient ${L(round(k, 4))}$ n'est pas le taux de {taux} % : c'est "
            f"le nombre qui vérifie $e^{{{L(round(k, 4))}}} = {L(coef)}$. L'écriture "
            "continue et le coefficient multiplicateur décrivent la même évolution, "
            "avec deux paramétrages différents."
        )
    elif presentation == "coefficient":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant s'élève aujourd'hui à **{_fr(depart, 0)}
> {ctx.unite}** et est **multiplié par ${L(coef)}$ chaque année**. On souhaite l'écrire sous la forme
> continue ${notation.de()} = {L(depart)}\\,e^{{k\\,{var}}}$.
>
> Que vaudra-t-il dans **{horizon} ans** ? Arrondissez au centième.
"""
        origine_k = (
            f"Le coefficient $k$ de l'exposant est défini par $e^{{k}} = {L(coef)}$, "
            f"soit $k \\approx {L(round(k, 4))}$. Ce n'est pas ${L(coef)}$ lui-même, "
            "et ce n'est pas non plus le taux : c'est le troisième paramétrage de la "
            "même croissance."
        )
    else:
        enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant s'élève aujourd'hui à **{_fr(depart, 0)}
> {ctx.unite}** et {cx.phrase_taux(taux)}.
>
> En écrivant son évolution sous forme continue
> ${notation.de()} = {L(depart)}\\,e^{{k\\,{var}}}$, que vaudra-t-elle dans
> **{horizon} ans** ? Arrondissez au centième.
"""
        origine_k = (
            f"Un taux de {taux} % correspond au coefficient ${L(coef)}$, donc à "
            f"$k$ tel que $e^{{k}} = {L(coef)}$, soit $k \\approx "
            f"{L(round(k, 4))}$. C'est la seule difficulté de l'exercice : le taux "
            "ne se recopie pas tel quel dans l'exposant."
        )

    etapes = [
        Etape(
            "Identifier — d'où vient le coefficient dans l'exposant",
            origine_k,
        ),
        Etape(
            "Substituer",
            "",
            rf"{notation.de(str(horizon))} = {L(depart)} \times "
            rf"e^{{{L(round(k, 4))} \times {horizon}}} = {L(depart)} \times "
            rf"e^{{{L(round(k * horizon, 4))}}} \approx {L(round(reponse, 2))}"
            rf"\ \text{{{ctx.unite}}}",
        ),
        Etape(
            "Vérifier — les deux écritures coïncident",
            f"Par le coefficient multiplicateur : ${L(depart)} \\times "
            f"({L(coef)})^{{{horizon}}} = {L(round(discret, 2))}$ {ctx.unite}. "
            f"Par l'exponentielle : ${L(round(reponse, 2))}$ {ctx.unite}. "
            "Identiques. ✓ Ce contrôle est le meilleur moyen de confirmer qu'on n'a "
            "pas confondu le taux et le coefficient de l'exposant.",
        ),
        Etape(
            "Interpréter — ce que le continu apporte",
            "L'écriture exponentielle permet de calculer la valeur à **n'importe quel "
            "instant**, y compris au bout de 3,5 ans — ce qu'une suite géométrique ne "
            "permet pas. C'est ce qui la rend indispensable dès qu'on veut répondre à "
            "« quand ? » plutôt qu'à « combien la n-ième année ? ».",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur dans {horizon} ans",
        unite=ctx.unite,
        tolerance=0.002,
        indice="Le temps se place **dans** l'exposant, jamais en facteur devant.",
        pieges=[
            (
                float(depart * math.exp(k) * horizon),
                "Vous avez multiplié par le nombre d'années **en dehors** de "
                "l'exponentielle. Le temps est dans l'exposant.",
            ),
            (
                float(depart * (1 + horizon * taux / 100)),
                f"Vous avez raisonné en évolution **linéaire** : {taux} % du montant "
                "initial, répétés. Or le taux porte chaque année sur la valeur "
                "courante.",
            ),
            (
                float(depart * math.exp(coef * horizon)),
                f"Vous avez placé le coefficient ${L(coef)}$ dans l'exposant. "
                f"L'exposant contient $k \\approx {L(round(k, 4))}$, défini par "
                f"$e^{{k}} = {L(coef)}$.",
            ),
        ],
    )


# --- 4. Pourquoi notre intuition échoue ------------------------------------


def gen_intuition() -> Exercice:
    ctx = cx.tirer(cx.MONETAIRES)
    depart = random.choice([85, 100, 120, 64])
    taux = random.choice([3, 4, 5])
    horizon = random.choice([20, 25, 30, 40])
    coef = 1 + taux / 100
    reponse = depart * coef**horizon
    lineaire = depart * (1 + horizon * taux / 100)
    presentation = random.choice(["taux", "coefficient"])

    if presentation == "taux":
        description = cx.phrase_taux(taux)
    else:
        description = cx.phrase_coefficient(coef, periode="chaque année")

    enonce = f"""
> **{_maj(ctx.sujet)}.** Ce montant s'élève aujourd'hui à **{_fr(depart, 0)}
> {ctx.unite}** et {description}.
>
> Que vaudra-t-il dans **{horizon} ans** ? Arrondissez au dixième.
"""

    etapes = [
        Etape(
            "Identifier — chaque année multiplie, elle n'ajoute pas",
            f"Le piège de cette question est l'horizon long : sur {horizon} ans, "
            "l'intuition linéaire devient franchement fausse, alors qu'elle restait "
            "acceptable sur trois ou quatre ans."
            + (
                f" Le taux de {taux} % correspond au coefficient ${L(coef)}$."
                if presentation == "taux"
                else f" Le coefficient ${L(coef)}$ correspond à une hausse de "
                f"{taux} % par an."
            ),
        ),
        Etape(
            "Calculer",
            "",
            rf"{L(depart)} \times ({L(coef)})^{{{horizon}}} \approx {L(depart)} "
            rf"\times {L(round(coef**horizon, 4))} \approx {L(round(reponse, 1))}"
            rf"\ \text{{{ctx.unite}}}",
        ),
        Etape(
            "Vérifier — comparer à l'intuition linéaire",
            f"Un raisonnement linéaire donnerait ${L(depart)} \\times (1 + {horizon} "
            f"\\times {L(taux / 100)}) = {L(round(lineaire, 1))}$ {ctx.unite}, soit un "
            f"écart de **{_fr(reponse - lineaire, 1)} {ctx.unite}** avec le résultat "
            f"correct. Sur {horizon} ans, l'erreur atteint "
            f"{_fr(100 * (reponse - lineaire) / lineaire, 0)} % du montant.",
        ),
        Etape(
            "Interpréter — pourquoi l'exponentielle surprend toujours",
            "Sur les premières années, l'écart entre les deux raisonnements est "
            "négligeable et la croissance paraît maîtrisable. C'est ce qui rend ce "
            "mécanisme si difficile à traiter politiquement : au moment où l'écart "
            "devient visible, il est déjà considérable. "
            "La séance 7 permettra de répondre à la question complémentaire — "
            "**quand** la valeur aura-t-elle doublé ?",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur dans {horizon} ans",
        unite=ctx.unite,
        tolerance=0.002,
        indice="Le coefficient s'applique une fois par an, sur le montant de l'année "
        "précédente.",
        pieges=[
            (
                float(lineaire),
                f"Vous avez ajouté {horizon} fois {taux} % du montant **initial**. "
                "Chaque année, le taux porte sur la valeur de l'année précédente, qui "
                "a déjà augmenté.",
            ),
            (
                float(depart * coef),
                "Vous n'avez appliqué le coefficient qu'une seule fois.",
            ),
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
    st.subheader("Une grandeur à horizon long")
    executer("s6_intuition", gen_intuition)

st.markdown("---")
st.caption(
    "Semestre — séance n°6 : La fonction exponentielle · "
    "Fil rouge F : la dette de Villeneuve · Sciences Po."
)
