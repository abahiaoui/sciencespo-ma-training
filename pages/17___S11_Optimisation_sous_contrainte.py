"""Série S11 — Plusieurs variables et optimisation sous contrainte.

Fil rouge H : l'arbitrage budgétaire. Séance d'ouverture, non exigible à l'examen.
"""

import random

import streamlit as st
import sympy as sp

from contextes import a_contracte, latex_nombre as L
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
    return f"{v:,.2f}".replace(",", "\u202f").replace(".", ",") if n == 2 else (
        f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")
    )


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


#: Les deux leviers d'un arbitrage, et le nom de l'objectif. Changer de couple
#: oblige à relire l'énoncé plutôt qu'à reconnaître un gabarit.
ARBITRAGES = [
    ("Q", "x", "y", "les infrastructures", "le personnel", "la qualité du service"),
    ("Q", "K", "L", "l'équipement", "la main-d'œuvre", "la production"),
    ("U", "x", "y", "la prévention", "les soins", "le bénéfice sanitaire"),
    ("S", "a", "b", "les acquisitions", "les animations", "le service rendu"),
]


# --- 1. Dérivée partielle ---------------------------------------------------


def gen_partielle() -> Exercice:
    nom, v1, v2, _, _, _ = random.choice(ARBITRAGES)
    s1, s2 = sp.Symbol(v1), sp.Symbol(v2)
    variable = random.choice([v1, v2])
    autre = v2 if variable == v1 else v1
    cible = s1 if variable == v1 else s2
    forme = random.choice(["croisee", "separee", "cobb"])
    a = random.choice([2, 3, 4])
    b = random.choice([1, 2, 5])
    c = random.choice([1, 2, 3])

    if forme == "separee":
        f = a * s1**3 + b * s2**2 + c * s1
        lecture = (
            f"Ici les deux variables n'apparaissent **jamais ensemble** : les termes "
            f"qui ne contiennent pas ${variable}$ disparaissent purement et "
            "simplement, comme des constantes."
        )
    elif forme == "cobb":
        f = a * s1**2 * s2**3
        lecture = (
            f"Un seul terme, mais les deux variables y figurent. En dérivant par "
            f"rapport à ${variable}$, le facteur en ${autre}$ reste **intact** : il "
            "joue le rôle d'un coefficient."
        )
    else:
        f = a * s1**2 * s2 + b * s1 * s2**2 + c * s2
        lecture = (
            f"Chaque terme contient les deux variables, sauf le dernier. Dans chacun, "
            f"tout ce qui ne contient pas ${variable}$ n'est qu'un coefficient."
        )

    reponse = sp.expand(sp.diff(f, cible))

    enonce = f"""
> Soit la fonction de deux variables
>
> $$ {nom}({v1}, {v2}) = {sp.latex(f)} $$
>
> Calculez la dérivée partielle
> $\\dfrac{{\\partial {nom}}}{{\\partial {variable}}}$.
"""

    etapes = [
        Etape(
            "Identifier — l'autre variable devient une constante",
            f"Dériver par rapport à ${variable}$, c'est dériver **comme si "
            f"${autre}$ était un nombre fixe. Aucune règle nouvelle : ce sont les "
            "dérivées de la séance 9, appliquées à une seule lettre à la fois.",
        ),
        Etape(
            "Traiter terme par terme",
            lecture,
            rf"\frac{{\partial {nom}}}{{\partial {variable}}} = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — un test numérique",
            f"En $({v1}, {v2}) = (1, 1)$, la dérivée partielle vaut "
            f"${L(float(reponse.subs({s1: 1, s2: 1})), 0)}$. On peut le confirmer en "
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
        libelle=f"∂{nom}/∂{variable} =",
        symboles=[v1, v2],
        indice=f"Traitez ${autre}$ comme un nombre, puis dérivez normalement.",
        pieges=[
            (
                sp.expand(sp.diff(f, s1) + sp.diff(f, s2)),
                "Vous avez dérivé par rapport aux **deux** variables et additionné. "
                "Une dérivée partielle ne porte que sur une variable.",
            ),
            (
                sp.expand(sp.diff(f, s2 if variable == v1 else s1)),
                f"Vous avez dérivé par rapport à ${autre}$ au lieu de ${variable}$.",
            ),
        ],
    )


# --- 2. Productivité marginale ---------------------------------------------


def gen_marginale() -> Exercice:
    nom, v1, v2, levier1, levier2, objectif = random.choice(ARBITRAGES)
    s1, s2 = sp.Symbol(v1), sp.Symbol(v2)
    alpha = random.choice([2, 3])
    beta = random.choice([1, 2])
    k = random.choice([1, 2, 5])
    x0 = random.choice([2, 3, 4])
    y0 = random.choice([2, 3, 5])
    f = k * s1**alpha * s2**beta
    derivee = sp.diff(f, s1)
    reponse = float(derivee.subs({s1: x0, s2: y0}))

    enonce = f"""
> On modélise {objectif} par
>
> $$ {nom}({v1}, {v2}) = {sp.latex(f)} $$
>
> où ${v1}$ est la dépense consacrée {a_contracte(levier1)} et ${v2}$ celle
> consacrée {a_contracte(levier2)} (en centaines de milliers d'euros).
>
> Calculez $\\dfrac{{\\partial {nom}}}{{\\partial {v1}}}({x0}, {y0})$.
"""

    etapes = [
        Etape(
            "Identifier — c'est un effet marginal",
            f"La question revient à : « que gagne-t-on pour un euro de plus consacré "
            f"{a_contracte(levier1)}, l'autre poste restant inchangé ? ». C'est bien "
            "toutes choses égales par ailleurs.",
        ),
        Etape(
            f"Dériver par rapport à ${v1}$",
            f"${v2}^{{{beta}}}$ joue le rôle d'un simple coefficient constant.",
            rf"\frac{{\partial {nom}}}{{\partial {v1}}} = "
            rf"{sp.latex(sp.expand(derivee))}",
        ),
        Etape(
            "Substituer",
            "",
            rf"\frac{{\partial {nom}}}{{\partial {v1}}}({x0}, {y0}) = "
            rf"{L(reponse, 0)}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur",
            f"L'objectif lui-même vaut ${nom}({x0}, {y0}) = "
            f"{L(float(f.subs({s1: x0, s2: y0})), 0)}$. La dérivée partielle "
            f"({_fr(reponse, 0)}) est du même ordre : cohérent. ✓",
        ),
        Etape(
            "Interpréter — le rapport des marginales décide de l'arbitrage",
            "Ce nombre ne dit rien seul. Ce qui compte, c'est sa comparaison avec la "
            "productivité marginale de l'**autre** levier : si un euro rapporte plus "
            "sur un levier que sur l'autre, il faut redéployer. L'optimum est atteint "
            "quand les deux s'égalisent — c'est exactement ce que formalise l'onglet "
            "suivant.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Productivité marginale",
        tolerance=1e-6,
        indice=f"Dérivez par rapport à ${v1}$ en traitant ${v2}$ comme une constante, "
        "puis remplacez.",
        pieges=[
            (
                float(f.subs({s1: x0, s2: y0})),
                "Vous avez calculé la **valeur** de l'objectif, pas sa dérivée "
                "partielle.",
            ),
            (
                float(sp.diff(f, s2).subs({s1: x0, s2: y0})),
                f"Vous avez dérivé par rapport à ${v2}$. La question porte sur ${v1}$.",
            ),
        ],
    )


# --- 3. Le Lagrangien en pratique ------------------------------------------


def gen_lagrangien() -> Exercice:
    nom, v1, v2, levier1, levier2, objectif = random.choice(ARBITRAGES)
    alpha_num = random.choice([1, 2, 3])
    beta_num = random.choice([1, 2, 3])
    budget = random.choice([300_000, 400_000, 500_000, 600_000])
    prix1 = random.choice([1, 1, 2])  # un prix unitaire différent de 1 change la règle
    alpha = sp.Rational(alpha_num, alpha_num + beta_num)
    beta = 1 - alpha
    reponse = float(alpha * budget / prix1)

    if prix1 == 1:
        contrainte = rf"{v1} + {v2} = {L(budget)}"
        regle = (
            "le rapport des productivités marginales égale le rapport des prix — ici "
            "$1$, puisque les deux dépenses sont en euros"
        )
        resolution = (
            rf"{v1} = {sp.latex(alpha)} \times {L(budget)} = {L(reponse, 0)}"
            rf"\ \text{{€}}"
        )
        commentaire_part = (
            f"La **part** du budget consacrée à {levier1} vaut ${sp.latex(alpha)}$, "
            "c'est-à-dire exactement l'exposant — indépendamment du montant du budget."
        )
    else:
        contrainte = rf"{prix1}\,{v1} + {v2} = {L(budget)}"
        regle = (
            f"le rapport des productivités marginales égale le rapport des prix, qui "
            f"vaut ici ${prix1}$ : une unité du premier levier coûte ${prix1}$ fois "
            "plus cher"
        )
        resolution = (
            rf"{prix1}\,{v1} = {sp.latex(alpha)} \times {L(budget)} "
            rf"\quad\Longrightarrow\quad {v1} = {L(reponse, 0)}"
        )
        commentaire_part = (
            f"La part du **budget** consacrée à {levier1} vaut toujours "
            f"${sp.latex(alpha)}$, mais comme une unité coûte ${prix1}$ €, la "
            f"**quantité** achetée est divisée d'autant. Part et quantité ne se "
            "confondent que lorsque le prix unitaire vaut 1."
        )

    enonce = f"""
> **L'arbitrage budgétaire.** Une collectivité consacre **{_fr(budget, 0)} €** à une
> politique publique, répartis entre ${v1}$ unités de {levier1} et ${v2}$ unités de
> {levier2}.
>
> On estime {objectif} par
>
> $$ {nom}({v1}, {v2}) = {v1}^{{{sp.latex(alpha)}}}\\,{v2}^{{{sp.latex(beta)}}}
>    \\qquad \\text{{sous la contrainte}} \\qquad {contrainte} $$
>
> Quelle valeur de ${v1}$ faut-il retenir à l'optimum ?
"""

    etapes = [
        Etape(
            "Identifier — sans contrainte, le problème n'a pas de solution",
            f"On augmenterait indéfiniment ${v1}$ et ${v2}$. C'est le budget qui rend "
            "la question intéressante : chaque euro consacré à un levier se paie en un "
            "euro de moins sur l'autre. Le Lagrangien sert à intégrer cette contrainte "
            "au calcul plutôt qu'à la traiter à part.",
            rf"\mathcal{{L}} = {v1}^{{{sp.latex(alpha)}}}{v2}^{{{sp.latex(beta)}}} "
            rf"- \lambda\,\big({contrainte.replace('=', '-')}\big)",
        ),
        Etape(
            "Écrire les conditions du premier ordre",
            f"On annule les trois dérivées partielles. Les deux premières, mises en "
            f"rapport, éliminent $\\lambda$ et laissent la règle d'arbitrage : {regle}.",
            rf"\frac{{\partial \mathcal{{L}}}}{{\partial {v1}}} = 0 \ ,\quad "
            rf"\frac{{\partial \mathcal{{L}}}}{{\partial {v2}}} = 0 "
            rf"\quad\Longrightarrow\quad \frac{{{sp.latex(alpha)}\,{v2}}}"
            rf"{{{sp.latex(beta)}\,{v1}}} = {prix1}",
        ),
        Etape(
            "Résoudre avec la contrainte",
            "La troisième condition redonne simplement la contrainte budgétaire. "
            "En y reportant la relation précédente, on obtient la solution.",
            resolution,
        ),
        Etape(
            "Vérifier — la contrainte est-elle saturée ?",
            f"Il reste {_fr(budget - prix1 * reponse, 0)} € pour {levier2}, et le "
            f"total fait bien {_fr(budget, 0)} €. ✓ À l'optimum, la contrainte est "
            "**toujours** saturée : laisser de l'argent inutilisé ne peut pas être "
            "optimal.",
        ),
        Etape(
            "Interpréter — la règle des parts constantes",
            f"{commentaire_part} C'est la propriété caractéristique des fonctions "
            "Cobb-Douglas, et la raison de leur succès en modélisation : elle rend "
            "les arbitrages prévisibles et transposables d'une collectivité à l'autre.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur de {v1} à l'optimum",
        tolerance=0.002,
        indice="À l'optimum, le rapport des dérivées partielles égale le rapport des "
        "prix.",
        pieges=[
            (
                float(budget) / 2,
                "Vous avez partagé le budget en deux parts égales. Ce ne serait "
                "correct que si les deux exposants (et les deux prix) étaient "
                "identiques.",
            ),
            (
                float(budget) - reponse,
                f"C'est ce qui reste pour {levier2}. L'énoncé demande ${v1}$.",
            ),
            (
                float(budget),
                "Vous avez tout consacré à un seul levier : la contrainte impose de "
                "partager, et l'exposant de l'autre levier interdit de le laisser à "
                "zéro.",
            ),
        ],
    )


# --- 4. Que représente λ ? (QCM) -------------------------------------------


def gen_lambda() -> Exercice:
    nom, v1, v2, levier1, levier2, objectif = random.choice(ARBITRAGES)
    lam = random.choice([0.4, 1.5, 2.8, 6.0])
    budget = random.choice([300_000, 500_000, 750_000])
    unite_objectif = random.choice(["unité(s)", "point(s)"])

    bonne = (
        f"Un euro de budget supplémentaire augmenterait {objectif} optimal(e) "
        f"d'environ {_fr(lam, 1)} {unite_objectif}."
    )
    valeur = f"{_maj(objectif)} optimal(e) vaut {_fr(lam, 1)}."
    decision = f"Il faut consacrer {_fr(lam, 1)} € {a_contracte(levier1)}."
    depassement = f"Le budget est dépassé de {_fr(lam, 1)} €."
    options = [bonne, valeur, decision, depassement]
    random.shuffle(options)

    enonce = f"""
> Le problème d'arbitrage sous contrainte budgétaire de **{_fr(budget, 0)} €**, entre
> {levier1} et {levier2}, a été résolu. Le multiplicateur de Lagrange à l'optimum vaut
>
> $$ \\lambda = {L(lam)} $$
>
> Que signifie ce nombre ?
"""

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
            rf"\lambda = \frac{{\partial {nom}^{{*}}}}{{\partial R}}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur",
            f"Avec $\\lambda = {L(lam)}$, passer de {_fr(budget, 0)} à "
            f"{_fr(budget + 1, 0)} € ferait gagner environ {_fr(lam, 1)} "
            f"{unite_objectif}. Comme toute lecture marginale, l'approximation ne "
            "vaut que pour une petite variation.",
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
            (
                valeur,
                "$\\lambda$ n'est pas la **valeur** de l'objectif, mais sa "
                "**sensibilité** à un relâchement de la contrainte.",
            ),
            (
                decision,
                f"$\\lambda$ n'est pas une variable de décision : les montants "
                f"optimaux sont ${v1}$ et ${v2}$.",
            ),
            (
                depassement,
                "À l'optimum, la contrainte est exactement saturée, jamais dépassée.",
            ),
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
