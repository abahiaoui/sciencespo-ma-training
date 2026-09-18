"""Série S11 — Fonctions à deux variables, dérivées partielles et Lagrangien.

Chapitre non exigible à l'examen final : il ouvre sur la suite du cursus.
"""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S11 | Deux variables", page_icon="🧭", layout="wide")

x, y, K, L = sp.symbols("x y K L")

st.title("🧭 S11 — Fonctions à deux variables et Lagrangien")

st.warning(
    "**Chapitre non exigible à l'examen final.** Cette séance ouvre sur la suite du "
    "cursus : elle montre que tout ce qui précède se transpose quand une décision "
    "dépend de plusieurs leviers. Travaillez-la par curiosité, sans pression."
)

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **dérivée partielle**, l'interpréter comme un effet « toutes choses
égales par ailleurs », et résoudre un problème d'optimisation **sous contrainte** par
la méthode du Lagrangien.

### 🧠 Le déplacement conceptuel
Jusqu'ici, une décision portait sur un seul levier. Ici il y en a deux, et surtout
un **budget** qui les relie : dépenser davantage sur l'un impose de dépenser moins sur
l'autre. C'est la structure de tout arbitrage réel, et c'est ce que le Lagrangien
formalise.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 11")
    st.markdown("**Dérivée partielle**")
    st.latex(r"\frac{\partial f}{\partial x}")
    st.markdown("On dérive par rapport à $x$ en traitant $y$ comme une **constante**.")
    st.markdown("**Optimisation sous contrainte**")
    st.latex(r"\mathcal{L}(x,y,\lambda) = f(x,y) - \lambda\,\big(g(x,y) - c\big)")
    st.markdown("**Conditions du premier ordre**")
    st.latex(r"\frac{\partial \mathcal{L}}{\partial x} = 0 \qquad "
             r"\frac{\partial \mathcal{L}}{\partial y} = 0 \qquad "
             r"\frac{\partial \mathcal{L}}{\partial \lambda} = 0")
    st.info(
        "**Cas Cobb-Douglas**\n\n"
        r"Pour $f = x^{\alpha} y^{\beta}$ sous $p x + q y = R$, l'optimum dépense "
        r"une part $\frac{\alpha}{\alpha+\beta}$ du budget sur $x$."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Dérivée partielle ---------------------------------------------------


def gen_derivee_partielle() -> Exercice:
    a = random.choice([2, 3, 4])
    b = random.choice([1, 2, 5])
    c = random.choice([1, 2, 3])
    variable = random.choice(["x", "y"])
    f = a * x**2 * y + b * x * y**2 + c * y

    reponse = sp.expand(sp.diff(f, x if variable == "x" else y))

    enonce = f"""
> Soit la fonction de deux variables
>
> $$ f(x, y) = {sp.latex(f)} $$
>
> Calculez la dérivée partielle
> $\\dfrac{{\\partial f}}{{\\partial {variable}}}$.
"""

    autre = "y" if variable == "x" else "x"

    etapes = [
        Etape(
            "Identifier — l'autre variable devient une constante",
            f"Dériver par rapport à ${variable}$, c'est dériver **comme si ${autre}$ "
            "était un nombre fixe. Aucune règle nouvelle n'est nécessaire : ce sont "
            "les dérivées de la séance 3, appliquées à une seule lettre à la fois.",
        ),
        Etape(
            "Traiter terme par terme",
            f"Dans chaque terme, tout ce qui ne contient pas ${variable}$ est un "
            f"simple coefficient. Un terme sans ${variable}$ du tout disparaît, comme "
            "une constante ordinaire.",
            rf"\frac{{\partial f}}{{\partial {variable}}} = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — un test numérique",
            f"En $(x, y) = (1, 1)$, la dérivée partielle vaut "
            f"${float(reponse.subs({x: 1, y: 1})):.0f}$. On peut le confirmer en "
            f"faisant varier ${variable}$ de $0{{,}}001$ à partir de ce point, "
            f"l'autre variable restant fixée. ✓",
        ),
        Etape(
            "Interpréter — « toutes choses égales par ailleurs »",
            f"La dérivée partielle mesure l'effet d'une variation de ${variable}$ "
            f"**en maintenant ${autre}$ constant**. C'est exactement la clause *ceteris "
            "paribus* omniprésente en sciences sociales — et c'est aussi sa limite : "
            "dans la réalité, les deux variables bougent souvent ensemble.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle=f"∂f/∂{variable} =",
        symboles=["x", "y"],
        indice=f"Traitez ${autre}$ comme un nombre, puis dérivez normalement.",
        pieges=[
            (sp.expand(sp.diff(f, x) + sp.diff(f, y)),
             "Vous avez dérivé par rapport aux **deux** variables et additionné. "
             "Une dérivée partielle ne porte que sur une variable à la fois."),
            (sp.expand(sp.diff(f, y if variable == "x" else x)),
             f"Vous avez dérivé par rapport à ${autre}$ au lieu de ${variable}$."),
        ],
    )


# --- 2. Évaluer une dérivée partielle --------------------------------------


def gen_valeur_partielle() -> Exercice:
    alpha = random.choice([2, 3])
    beta = random.choice([1, 2])
    k = random.choice([1, 2, 5])
    k0 = random.choice([2, 3, 4])
    l0 = random.choice([2, 3, 5])
    f = k * K**alpha * L**beta
    fp = sp.diff(f, K)
    reponse = float(fp.subs({K: k0, L: l0}))

    enonce = f"""
> Une fonction de production s'écrit
>
> $$ Y(K, L) = {sp.latex(f)} $$
>
> où $K$ est le capital et $L$ le travail.
>
> Calculez la **productivité marginale du capital** en $K = {k0}$, $L = {l0}$,
> c'est-à-dire $\\dfrac{{\\partial Y}}{{\\partial K}}({k0}, {l0})$.
"""

    etapes = [
        Etape(
            "Identifier — la productivité marginale est une dérivée partielle",
            "Elle répond à : « que rapporte une unité de capital supplémentaire, à "
            "travail inchangé ? ». C'est bien un effet toutes choses égales par "
            "ailleurs, donc une dérivée partielle.",
        ),
        Etape(
            "Dériver par rapport à $K$",
            f"$L^{{{beta}}}$ joue le rôle d'un coefficient constant.",
            rf"\frac{{\partial Y}}{{\partial K}} = {sp.latex(sp.expand(fp))}",
        ),
        Etape(
            "Substituer",
            "",
            rf"\frac{{\partial Y}}{{\partial K}}({k0}, {l0}) = {reponse:.0f}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur",
            f"La production elle-même vaut $Y({k0}, {l0}) = "
            f"{float(f.subs({K: k0, L: l0})):.0f}$. La productivité marginale "
            f"({reponse:.0f}) est du même ordre : c'est cohérent, une dérivée n'ayant "
            "aucune raison d'être d'une échelle radicalement différente ici.",
        ),
        Etape(
            "Interpréter",
            f"Une unité de capital supplémentaire apporterait environ "
            f"**{reponse:.0f} unités** de production, à travail inchangé. "
            "C'est ce nombre — et son équivalent pour le travail — qu'on compare aux "
            "prix respectifs des deux facteurs pour décider où investir. "
            "L'onglet suivant formalise cette comparaison.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Productivité marginale du capital",
        tolerance=1e-6,
        indice="Dérivez par rapport à $K$ en traitant $L$ comme une constante, "
        "puis remplacez.",
        pieges=[
            (float(f.subs({K: k0, L: l0})),
             "Vous avez calculé la **production**, pas sa dérivée partielle."),
            (float(sp.diff(f, L).subs({K: k0, L: l0})),
             "Vous avez dérivé par rapport au **travail**. La question porte sur le "
             "capital."),
        ],
    )


# --- 3. Optimisation sous contrainte : la part du budget -------------------


def gen_lagrangien_part() -> Exercice:
    alpha = random.choice([1, 2, 3])
    beta = random.choice([1, 2, 3])
    budget = random.choice([120, 240, 300, 600])
    prix = random.choice([2, 3, 4, 5])
    part = sp.Rational(alpha, alpha + beta)
    reponse = float(part * budget / prix)

    enonce = f"""
> Une collectivité répartit un budget de **{budget} milliers d'euros** entre deux
> actions, $x$ et $y$. Le bénéfice social est modélisé par
>
> $$ U(x, y) = x^{{{alpha}}}\\,y^{{{beta}}} $$
>
> Le coût unitaire de l'action $x$ est de **{prix}** milliers d'euros, celui de
> l'action $y$ de **1** millier d'euros. La contrainte budgétaire s'écrit donc
> $\\;{prix}x + y = {budget}$.
>
> Quelle quantité $x$ faut-il retenir à l'optimum ?
"""

    etapes = [
        Etape(
            "Identifier — maximiser sous contrainte, pas librement",
            "Sans contrainte, on augmenterait indéfiniment $x$ et $y$. C'est le budget "
            "qui rend le problème intéressant : toute unité de $x$ en plus se paie "
            "en unités de $y$ en moins. Le Lagrangien sert précisément à intégrer "
            "cette contrainte au calcul.",
            rf"\mathcal{{L}} = x^{{{alpha}}}y^{{{beta}}} - \lambda({prix}x + y - {budget})",
        ),
        Etape(
            "Écrire les conditions du premier ordre",
            "On annule les trois dérivées partielles. Les deux premières, mises en "
            "rapport, éliminent $\\lambda$ et donnent la règle d'arbitrage.",
            rf"\frac{{{alpha}\,x^{{{alpha}-1}}y^{{{beta}}}}}"
            rf"{{{beta}\,x^{{{alpha}}}y^{{{beta}-1}}}} = \frac{{{prix}}}{{1}}"
            rf" \iff \frac{{{alpha}\,y}}{{{beta}\,x}} = {prix}",
        ),
        Etape(
            "Résoudre avec la contrainte",
            f"En reportant $y = \\frac{{{beta}}}{{{alpha}}} \\times {prix}x$ dans la "
            "contrainte, on obtient la part du budget consacrée à $x$ :",
            rf"{prix}x = \frac{{{alpha}}}{{{alpha}+{beta}}} \times {budget} "
            rf"= {float(part*budget):.1f} \iff x = {reponse:.2f}",
        ),
        Etape(
            "Vérifier — la contrainte est-elle saturée ?",
            f"Avec $x = {reponse:.2f}$, la dépense sur $x$ vaut "
            f"${prix} \\times {reponse:.2f} = {prix*reponse:.1f}$, et il reste "
            f"${budget - prix*reponse:.1f}$ pour $y$. Le budget est intégralement "
            "utilisé. ✓ À l'optimum, la contrainte est toujours saturée : laisser "
            "de l'argent inutilisé ne peut pas être optimal.",
        ),
        Etape(
            "Interpréter — la règle des parts constantes",
            f"Le résultat remarquable est que la **part du budget** consacrée à $x$ "
            f"vaut $\\frac{{{alpha}}}{{{alpha}+{beta}}}$, indépendamment du budget "
            "total et des prix. C'est la propriété caractéristique des fonctions "
            "Cobb-Douglas, et la raison de leur succès en modélisation : elle rend "
            "les arbitrages prévisibles.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Quantité x optimale",
        tolerance=0.005,
        indice="À l'optimum, le rapport des dérivées partielles égale le rapport "
        "des prix.",
        pieges=[
            (float(part * budget),
             "Vous avez donné la **dépense** consacrée à $x$, pas la quantité. "
             f"Il reste à diviser par le prix unitaire ({prix})."),
            (float(budget) / prix,
             "Vous avez consacré **tout** le budget à $x$. La contrainte impose de "
             "partager entre les deux actions."),
            (float(budget) / (2 * prix),
             "Vous avez partagé le budget en deux parts égales. Ce n'est correct que "
             "si les deux exposants sont identiques, ce qui n'est pas le cas ici."),
        ],
    )


# --- 4. Le sens du multiplicateur (QCM) ------------------------------------


def gen_multiplicateur() -> Exercice:
    lam = random.choice([0.4, 1.5, 2.8, 6.0])
    budget = random.choice([200, 500, 1000])

    bonne = (
        f"Un millier d'euros de budget supplémentaire augmenterait le bénéfice "
        f"social d'environ {lam} unité(s)."
    )
    options = [
        bonne,
        f"Le bénéfice social optimal vaut {lam} unités.",
        f"Il faut consacrer {lam} milliers d'euros à la première action.",
        f"La contrainte budgétaire est dépassée de {lam} milliers d'euros.",
    ]
    random.shuffle(options)

    enonce = f"""
> Un problème d'optimisation sous contrainte budgétaire de **{budget} milliers
> d'euros** a été résolu. Le multiplicateur de Lagrange à l'optimum vaut
>
> $$ \\lambda = {lam} $$
>
> Que signifie ce nombre ?
"""

    etapes = [
        Etape(
            "Identifier — $\\lambda$ n'est pas une quantité",
            "Le multiplicateur n'est ni une des variables de décision ni la valeur de "
            "l'objectif. Il apparaît comme un intermédiaire de calcul, mais il a une "
            "interprétation propre, et elle est économique.",
        ),
        Etape(
            "Lire $\\lambda$ comme une dérivée",
            "$\\lambda$ mesure la variation de l'objectif optimal quand on **relâche "
            "la contrainte d'une unité**. C'est la dérivée de la valeur optimale par "
            "rapport au budget.",
            r"\lambda = \frac{\partial U^{*}}{\partial R}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur est plausible",
            f"Avec $\\lambda = {lam}$, passer de {budget} à {budget + 1} milliers "
            f"d'euros ferait gagner environ {lam} unité(s) de bénéfice social. "
            "Comme toute lecture marginale, l'approximation ne vaut que pour une "
            "petite variation du budget.",
        ),
        Etape(
            "Interpréter — le prix implicite de la contrainte",
            "On appelle $\\lambda$ le **prix fictif** de la contrainte : c'est ce "
            "qu'il vaudrait la peine de payer pour desserrer le budget d'une unité. "
            "En évaluation de politique publique, c'est l'argument chiffré en faveur "
            "d'une rallonge budgétaire — et s'il est faible, l'argument tombe.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation de λ",
        indice="$\\lambda$ répond à la question : que gagnerait-on si la contrainte "
        "était un peu moins serrée ?",
        pieges=[
            (f"Le bénéfice social optimal vaut {lam} unités.",
             "$\\lambda$ n'est pas la **valeur** de l'objectif, mais sa **sensibilité** "
             "à un relâchement de la contrainte."),
            (f"Il faut consacrer {lam} milliers d'euros à la première action.",
             "$\\lambda$ n'est pas une variable de décision : les quantités optimales "
             "sont $x$ et $y$."),
            (f"La contrainte budgétaire est dépassée de {lam} milliers d'euros.",
             "À l'optimum, la contrainte est exactement saturée, jamais dépassée."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dérivée partielle",
        "2️⃣ Productivité marginale",
        "3️⃣ Optimiser sous contrainte",
        "4️⃣ Le multiplicateur λ",
    ]
)

with onglets[0]:
    st.subheader("Dériver une variable à la fois")
    executer("s11_partielle", gen_derivee_partielle)

with onglets[1]:
    st.subheader("Toutes choses égales par ailleurs")
    executer("s11_valeur", gen_valeur_partielle)

with onglets[2]:
    st.subheader("Le Lagrangien en pratique")
    executer("s11_lagrangien", gen_lagrangien_part)

with onglets[3]:
    st.subheader("Que vaut une contrainte desserrée ?")
    executer("s11_multiplicateur", gen_multiplicateur)

st.markdown("---")
st.caption(
    "Semestre — séance n°11 : Fonctions à deux variables et Lagrangien "
    "(non exigible à l'examen final) · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
