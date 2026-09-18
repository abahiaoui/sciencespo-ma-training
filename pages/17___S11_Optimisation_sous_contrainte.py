"""Série S11 — Plusieurs variables et optimisation sous contrainte.

Fil rouge H : l'arbitrage budgétaire. Séance d'ouverture, non exigible à l'examen.
"""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S11 | Deux variables", page_icon="🧭", layout="wide")

x, y = sp.symbols("x y")

st.title("🧭 S11 — Plusieurs variables et optimisation sous contrainte")

st.warning(
    "**Statut de cette séance.** Elle ouvre sur la suite du cursus et n'est pas "
    "exigible à l'examen final. Travaillez-la par curiosité : elle montre que tout "
    "ce qui précède se transpose quand une décision dépend de plusieurs leviers."
)

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **dérivée partielle**, l'interpréter comme un effet « toutes choses
égales par ailleurs », appliquer la **recette du Lagrangien**, et comprendre ce que
mesure le multiplicateur $\\lambda$.

### 🧠 Une idée déjà familière
Optimiser, c'est toujours annuler une dérivée. La nouveauté est qu'il y a désormais
**deux** leviers et un **budget** qui les relie : dépenser plus sur l'un impose de
dépenser moins sur l'autre. C'est la structure de tout arbitrage réel.

### 🏛️ Fil rouge H — L'arbitrage budgétaire
Villeneuve consacre **500 000 €** à sa politique de mobilité, répartis entre $x$ euros
d'infrastructures et $y$ euros de personnel. La qualité du service est estimée par
$Q(x, y) = x^{0{,}6}\\,y^{0{,}4}$.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 11")
    st.markdown("**Dérivée partielle**")
    st.latex(r"\frac{\partial f}{\partial x}")
    st.markdown("On dérive par rapport à $x$ en traitant $y$ comme une **constante**.")
    st.markdown("**La recette du Lagrangien**")
    st.latex(r"\mathcal{L} = f(x,y) - \lambda\,\big(g(x,y) - c\big)")
    st.latex(r"\frac{\partial \mathcal{L}}{\partial x} = 0 \quad "
             r"\frac{\partial \mathcal{L}}{\partial y} = 0 \quad "
             r"\frac{\partial \mathcal{L}}{\partial \lambda} = 0")
    st.info(
        "**Cas Cobb-Douglas**\n\n"
        r"Pour $f = x^{\alpha}y^{\beta}$ sous $x + y = R$, l'optimum consacre "
        r"la part $\frac{\alpha}{\alpha+\beta}$ du budget à $x$ — quel que soit $R$."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Dérivée partielle ---------------------------------------------------


def gen_partielle() -> Exercice:
    a = random.choice([2, 3, 4])
    b = random.choice([1, 2, 5])
    c = random.choice([1, 2, 3])
    variable = random.choice(["x", "y"])
    f = a * x**2 * y + b * x * y**2 + c * y
    reponse = sp.expand(sp.diff(f, x if variable == "x" else y))
    autre = "y" if variable == "x" else "x"

    enonce = f"""
> Soit la fonction de deux variables
>
> $$ f(x, y) = {sp.latex(f)} $$
>
> Calculez la dérivée partielle $\\dfrac{{\\partial f}}{{\\partial {variable}}}$.
"""

    etapes = [
        Etape(
            "Identifier — l'autre variable devient une constante",
            f"Dériver par rapport à ${variable}$, c'est dériver **comme si ${autre}$ "
            "était un nombre fixe. Aucune règle nouvelle : ce sont les dérivées de la "
            "séance 9, appliquées à une seule lettre à la fois.",
        ),
        Etape(
            "Traiter terme par terme",
            f"Dans chaque terme, tout ce qui ne contient pas ${variable}$ n'est qu'un "
            f"coefficient. Un terme sans ${variable}$ du tout disparaît, comme "
            "n'importe quelle constante.",
            rf"\frac{{\partial f}}{{\partial {variable}}} = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — un test numérique",
            f"En $(x, y) = (1, 1)$, la dérivée partielle vaut "
            f"${float(reponse.subs({x: 1, y: 1})):.0f}$. On peut le confirmer en "
            f"faisant varier ${variable}$ de $0{{,}}001$ à partir de ce point, "
            f"${autre}$ restant fixé. ✓",
        ),
        Etape(
            "Interpréter — « toutes choses égales par ailleurs »",
            f"La dérivée partielle mesure l'effet d'une variation de ${variable}$ en "
            f"maintenant ${autre}$ constant. C'est exactement la clause *ceteris "
            "paribus* omniprésente en sciences sociales — et c'en est aussi la "
            "limite : dans la réalité, les deux variables bougent souvent ensemble.",
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
             "Une dérivée partielle ne porte que sur une variable."),
            (sp.expand(sp.diff(f, y if variable == "x" else x)),
             f"Vous avez dérivé par rapport à ${autre}$ au lieu de ${variable}$."),
        ],
    )


# --- 2. Productivité marginale ---------------------------------------------


def gen_marginale() -> Exercice:
    alpha = random.choice([2, 3])
    beta = random.choice([1, 2])
    k = random.choice([1, 2, 5])
    x0 = random.choice([2, 3, 4])
    y0 = random.choice([2, 3, 5])
    f = k * x**alpha * y**beta
    fp = sp.diff(f, x)
    reponse = float(fp.subs({x: x0, y: y0}))

    enonce = f"""
> La qualité d'un service est modélisée par
>
> $$ Q(x, y) = {sp.latex(f)} $$
>
> où $x$ est la dépense d'infrastructure et $y$ la dépense de personnel
> (en centaines de milliers d'euros).
>
> Calculez $\\dfrac{{\\partial Q}}{{\\partial x}}({x0}, {y0})$.
"""

    etapes = [
        Etape(
            "Identifier — c'est un effet marginal",
            "La question revient à : « que gagne-t-on en qualité pour un euro "
            "d'infrastructure de plus, à personnel inchangé ? ». "
            "C'est bien un effet toutes choses égales par ailleurs.",
        ),
        Etape(
            "Dériver par rapport à $x$",
            f"$y^{{{beta}}}$ joue le rôle d'un simple coefficient constant.",
            rf"\frac{{\partial Q}}{{\partial x}} = {sp.latex(sp.expand(fp))}",
        ),
        Etape(
            "Substituer",
            "",
            rf"\frac{{\partial Q}}{{\partial x}}({x0}, {y0}) = {reponse:.0f}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur",
            f"La qualité elle-même vaut $Q({x0}, {y0}) = "
            f"{float(f.subs({x: x0, y: y0})):.0f}$. La dérivée partielle "
            f"({reponse:.0f}) est du même ordre : cohérent. ✓",
        ),
        Etape(
            "Interpréter — le rapport des marginales décide de l'arbitrage",
            "Ce nombre ne dit rien seul. Ce qui compte, c'est sa comparaison avec la "
            "productivité marginale de l'**autre** levier : si un euro rapporte plus "
            "en infrastructure qu'en personnel, il faut redéployer. "
            "L'optimum est atteint quand les deux s'égalisent — c'est exactement ce "
            "que formalise l'onglet suivant.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Productivité marginale",
        tolerance=1e-6,
        indice="Dérivez par rapport à $x$ en traitant $y$ comme une constante, "
        "puis remplacez.",
        pieges=[
            (float(f.subs({x: x0, y: y0})),
             "Vous avez calculé la **qualité**, pas sa dérivée partielle."),
            (float(sp.diff(f, y).subs({x: x0, y: y0})),
             "Vous avez dérivé par rapport à $y$. La question porte sur $x$."),
        ],
    )


# --- 3. Le Lagrangien en pratique ------------------------------------------


def gen_lagrangien() -> Exercice:
    alpha_num = random.choice([1, 2, 3])
    beta_num = random.choice([1, 2, 3])
    budget = random.choice([300_000, 400_000, 500_000, 600_000])
    part = sp.Rational(alpha_num, alpha_num + beta_num)
    reponse = float(part * budget)
    alpha = sp.Rational(alpha_num, alpha_num + beta_num)
    beta = 1 - alpha

    enonce = f"""
> **L'arbitrage budgétaire.** Villeneuve consacre **{budget:,} €** à sa politique de
> mobilité, répartis entre $x$ euros d'**infrastructures** et $y$ euros de
> **personnel**.
>
> La qualité du service est estimée par
>
> $$ Q(x, y) = x^{{{sp.latex(alpha)}}}\\,y^{{{sp.latex(beta)}}}
>    \\qquad \\text{{sous la contrainte}} \\qquad x + y = {budget:,} $$
>
> Quelle somme faut-il consacrer aux **infrastructures** à l'optimum ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — sans contrainte, le problème n'a pas de solution",
            "On augmenterait indéfiniment $x$ et $y$. C'est le budget qui rend la "
            "question intéressante : chaque euro d'infrastructure se paie en un euro "
            "de personnel en moins. Le Lagrangien sert à intégrer cette contrainte "
            "au calcul plutôt qu'à la traiter à part.",
            rf"\mathcal{{L}} = x^{{{sp.latex(alpha)}}}y^{{{sp.latex(beta)}}} "
            rf"- \lambda\,(x + y - {budget})",
        ),
        Etape(
            "Écrire les conditions du premier ordre",
            "On annule les trois dérivées partielles. Les deux premières, mises en "
            "rapport, éliminent $\\lambda$ et laissent la règle d'arbitrage : le "
            "rapport des productivités marginales égale le rapport des prix — ici 1, "
            "puisque les deux dépenses sont en euros.",
            rf"\frac{{\partial \mathcal{{L}}}}{{\partial x}} = 0 \ ,\quad "
            rf"\frac{{\partial \mathcal{{L}}}}{{\partial y}} = 0 "
            rf"\quad\Longrightarrow\quad \frac{{{sp.latex(alpha)}\,y}}"
            rf"{{{sp.latex(beta)}\,x}} = 1",
        ),
        Etape(
            "Résoudre avec la contrainte",
            "La troisième condition redonne simplement la contrainte budgétaire. "
            "En y reportant la relation précédente, on obtient la part consacrée "
            "à $x$.",
            rf"x = {sp.latex(alpha)} \times {budget} = {reponse:.0f}\ \text{{€}}",
        ),
        Etape(
            "Vérifier — la contrainte est-elle saturée ?",
            f"Il reste ${budget - reponse:,.0f}$ € pour le personnel, et la somme "
            f"fait bien {budget:,} €. ✓ À l'optimum, la contrainte est **toujours** "
            "saturée : laisser de l'argent inutilisé ne peut pas être optimal."
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — la règle des parts constantes",
            f"Le résultat remarquable est que la **part** du budget consacrée aux "
            f"infrastructures vaut ${sp.latex(alpha)}$, c'est-à-dire exactement "
            "l'exposant — indépendamment du montant du budget. "
            "C'est la propriété caractéristique des fonctions Cobb-Douglas, et la "
            "raison de leur succès en modélisation : elle rend les arbitrages "
            "prévisibles et transposables d'une collectivité à l'autre.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Dépense d'infrastructures",
        unite="€",
        tolerance=0.002,
        indice="À l'optimum, le rapport des dérivées partielles égale le rapport des "
        "prix.",
        pieges=[
            (float(budget) / 2,
             "Vous avez partagé le budget en deux parts égales. Ce ne serait correct "
             "que si les deux exposants étaient identiques."),
            (float(budget) - reponse,
             "C'est la somme consacrée au **personnel**. L'énoncé demande les "
             "infrastructures."),
            (float(budget),
             "Vous avez tout consacré aux infrastructures : la contrainte impose de "
             "partager."),
        ],
    )


# --- 4. Que représente λ ? (QCM) -------------------------------------------


def gen_lambda() -> Exercice:
    lam = random.choice([0.4, 1.5, 2.8, 6.0])
    budget = random.choice([300_000, 500_000])

    bonne = (
        f"Un euro de budget supplémentaire augmenterait la qualité optimale "
        f"d'environ {lam} unité(s)."
    )
    options = [
        bonne,
        f"La qualité optimale du service vaut {lam}.",
        f"Il faut consacrer {lam} € aux infrastructures.",
        f"Le budget est dépassé de {lam} €.",
    ]
    random.shuffle(options)

    enonce = f"""
> Le problème d'arbitrage sous contrainte budgétaire de **{budget:,} €** a été
> résolu. Le multiplicateur de Lagrange à l'optimum vaut
>
> $$ \\lambda = {lam} $$
>
> Que signifie ce nombre ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — $\\lambda$ n'est ni une quantité ni un objectif",
            "Il apparaît comme un intermédiaire de calcul, introduit pour incorporer "
            "la contrainte. Mais il a une interprétation propre, et elle est "
            "économique.",
        ),
        Etape(
            "Lire $\\lambda$ comme une dérivée",
            "$\\lambda$ mesure la variation de l'objectif optimal quand on **relâche "
            "la contrainte d'une unité** : c'est la dérivée de la valeur optimale par "
            "rapport au budget.",
            r"\lambda = \frac{\partial Q^{*}}{\partial R}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur",
            f"Avec $\\lambda = {lam}$, passer de {budget:,} à {budget + 1:,} € "
            f"ferait gagner environ {lam} unité(s) de qualité. Comme toute lecture "
            "marginale, l'approximation ne vaut que pour une petite variation."
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — le prix implicite de la contrainte",
            "On appelle $\\lambda$ le **prix fictif** de la contrainte : ce qu'il "
            "vaudrait la peine de payer pour desserrer le budget d'un euro. "
            "En évaluation de politique publique, c'est l'argument chiffré en faveur "
            "d'une rallonge budgétaire — et s'il est faible, l'argument tombe de "
            "lui-même.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation de λ",
        indice="Que gagnerait-on si la contrainte était un peu moins serrée ?",
        pieges=[
            (f"La qualité optimale du service vaut {lam}.",
             "$\\lambda$ n'est pas la **valeur** de l'objectif, mais sa "
             "**sensibilité** à un relâchement de la contrainte."),
            (f"Il faut consacrer {lam} € aux infrastructures.",
             "$\\lambda$ n'est pas une variable de décision : les montants optimaux "
             "sont $x$ et $y$."),
            (f"Le budget est dépassé de {lam} €.",
             "À l'optimum, la contrainte est exactement saturée, jamais dépassée."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dérivée partielle",
        "2️⃣ Productivité marginale",
        "3️⃣ Le Lagrangien",
        "4️⃣ Le multiplicateur λ",
    ]
)

with onglets[0]:
    st.subheader("Dériver une variable à la fois")
    executer("s11_partielle", gen_partielle)

with onglets[1]:
    st.subheader("Toutes choses égales par ailleurs")
    executer("s11_marginale", gen_marginale)

with onglets[2]:
    st.subheader("Optimiser sous contrainte budgétaire")
    executer("s11_lagrangien", gen_lagrangien)

with onglets[3]:
    st.subheader("Que vaut une contrainte desserrée ?")
    executer("s11_lambda", gen_lambda)

st.markdown("---")
st.caption(
    "Semestre — séance n°11 : Plusieurs variables et optimisation sous contrainte "
    "(non exigible à l'examen final) · Fil rouge H : l'arbitrage budgétaire · "
    "Sciences Po."
)
