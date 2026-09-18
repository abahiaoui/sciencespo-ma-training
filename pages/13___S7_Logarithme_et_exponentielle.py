"""Série S7 — Logarithme népérien et exponentielle."""

import math
import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S7 | Logarithme et exponentielle", page_icon="🌱", layout="wide")

x = sp.Symbol("x")  # symbole sans hypothèse : le moteur parse les saisies avec un symbole nu

st.title("🌱 S7 — Logarithme et exponentielle")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Utiliser les propriétés du logarithme, résoudre une équation où l'inconnue est **en
exposant**, dériver $\\ln$ et $\\exp$, et comparer une croissance exponentielle à une
croissance linéaire.

### 🧠 À quoi sert le logarithme
À **descendre un exposant**. Dès qu'une inconnue est en exposant — un nombre d'années,
une durée de doublement — aucune manipulation algébrique ordinaire ne l'atteint. Le
logarithme est le seul outil qui la libère, parce qu'il transforme les produits en
sommes et les puissances en produits.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 7")
    st.markdown("**Propriétés du logarithme** ($a, b > 0$)")
    st.latex(r"\ln(ab) = \ln a + \ln b")
    st.latex(r"\ln\!\left(\frac{a}{b}\right) = \ln a - \ln b")
    st.latex(r"\ln(a^n) = n \ln a")
    st.latex(r"\ln 1 = 0 \qquad \ln e = 1")
    st.markdown("**Dérivées**")
    st.latex(r"(\ln x)' = \frac{1}{x} \qquad (e^x)' = e^x")
    st.error(
        "**L'erreur interdite**\n\n"
        r"$\ln(a+b) \neq \ln a + \ln b$"
        "\n\nLe logarithme transforme les **produits** en sommes, jamais les sommes."
    )
    st.info(
        "**Valeurs utiles**\n\n"
        "$\\ln 2 \\approx 0{,}693$ · $\\ln 10 \\approx 2{,}303$"
    )

GRANDEURS = [
    ("la dette de la collectivité", "M€"),
    ("le nombre de bénéficiaires", "personnes"),
    ("le stock de logements vacants", "logements"),
    ("la consommation d'énergie", "MWh"),
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
        detail = (
            f"$\\ln({a} \\times {b}) = \\ln {a} + \\ln {b} "
            f"\\approx {math.log(a):.4f} + {math.log(b):.4f}$"
        )
        regle = r"\ln(ab) = \ln a + \ln b"
        piege = (math.log(a) * math.log(b),
                 "Vous avez **multiplié** les logarithmes. La règle transforme le "
                 "produit en **somme** : $\\ln(ab) = \\ln a + \\ln b$.")
    elif modele == "quotient":
        expression = rf"\ln\!\left(\frac{{{a*b}}}{{{b}}}\right)"
        reponse = math.log(a)
        detail = (
            f"$\\ln\\left(\\frac{{{a*b}}}{{{b}}}\\right) = \\ln {a*b} - \\ln {b} "
            f"\\approx {math.log(a*b):.4f} - {math.log(b):.4f}$"
        )
        regle = r"\ln\!\left(\frac{a}{b}\right) = \ln a - \ln b"
        piege = (math.log(a * b) / math.log(b),
                 "Vous avez **divisé** les logarithmes. La règle transforme le "
                 "quotient en **différence**.")
    else:
        expression = rf"\ln({a}^{{{n}}})"
        reponse = n * math.log(a)
        detail = (
            f"$\\ln({a}^{{{n}}}) = {n} \\ln {a} "
            f"\\approx {n} \\times {math.log(a):.4f}$"
        )
        regle = r"\ln(a^n) = n \ln a"
        piege = (math.log(a) ** n,
                 "Vous avez élevé le logarithme à la puissance. L'exposant **descend "
                 "en facteur** : $\\ln(a^n) = n \\ln a$.")

    enonce = f"""
> Calculez, à l'aide des propriétés du logarithme :
>
> $$ {expression} $$
>
> Donnez une valeur approchée à $0{{,}}01$ près.
"""

    etapes = [
        Etape(
            "Identifier — quelle propriété s'applique ?",
            "Le logarithme fait **descendre d'un cran** dans la hiérarchie des "
            "opérations : une puissance devient un produit, un produit devient une "
            "somme, un quotient devient une différence. Reconnaître l'opération de "
            "départ donne immédiatement la règle.",
        ),
        Etape(
            "Appliquer la règle",
            "",
            regle,
        ),
        Etape(
            "Calculer",
            detail,
            rf"\approx {reponse:.4f}",
        ),
        Etape(
            "Vérifier — le calcul direct",
            "Le calcul direct donne la même valeur. La propriété n'a pas changé le "
            "résultat : elle a changé la **forme**, et c'est cette forme — une somme "
            "plutôt qu'un produit — qui permettra de résoudre des équations autrement "
            "inaccessibles.",
        ),
        Etape(
            "Interpréter — pourquoi cette transformation est précieuse",
            "En sciences sociales, on passe souvent une série en logarithme "
            "précisément pour cela : une croissance multiplicative devient additive, "
            "donc linéaire, donc lisible sur un graphique et estimable par une droite.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur",
        tolerance=0.01,
        indice="Repérez l'opération (produit, quotient, puissance) et appliquez la "
        "propriété correspondante.",
        pieges=[piege],
    )


# --- 2. Résoudre une équation avec l'inconnue en exposant ------------------


def gen_temps_doublement() -> Exercice:
    grandeur, unite = random.choice(GRANDEURS)
    depart = random.choice([200, 400, 500, 1000, 2000])
    taux = random.choice([2, 3, 4, 5, 6, 8])
    cible_facteur = random.choice([1.5, 2, 2.5, 3])
    cm = 1 + taux / 100
    cible = depart * cible_facteur
    reponse = math.log(cible_facteur) / math.log(cm)

    enonce = f"""
> {grandeur.capitalize()} vaut aujourd'hui **{depart:,} {unite}** et progresse de
> **{taux} % par an**.
>
> Au bout de combien d'années aura-t-elle atteint **{cible:,.0f} {unite}** ?
> Donnez le nombre d'années (non entier) à $0{{,}}01$ près.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — l'inconnue est en exposant",
            "L'équation à résoudre s'écrit avec $n$ **en exposant**. Aucune "
            "manipulation ordinaire — addition, division, factorisation — ne peut "
            "l'atteindre là. C'est exactement la situation où le logarithme est "
            "indispensable.",
            rf"{depart} \times ({cm})^n = {cible:.0f}",
        ),
        Etape(
            "Isoler la puissance",
            f"On divise les deux membres par ${depart}$.",
            rf"({cm})^n = \frac{{{cible:.0f}}}{{{depart}}} = {cible_facteur}",
        ),
        Etape(
            "Appliquer le logarithme pour faire descendre l'exposant",
            "C'est la propriété $\\ln(a^n) = n \\ln a$ qui fait tout le travail.",
            rf"n \ln({cm}) = \ln({cible_facteur}) \iff "
            rf"n = \frac{{\ln({cible_facteur})}}{{\ln({cm})}} "
            rf"= \frac{{{math.log(cible_facteur):.4f}}}{{{math.log(cm):.4f}}} "
            rf"\approx {reponse:.2f}",
        ),
        Etape(
            "Vérifier — recalculer la valeur atteinte",
            f"${depart} \\times ({cm})^{{{reponse:.2f}}} \\approx "
            f"{depart * cm**reponse:,.0f}$ {unite}. ✓ "
            "On retrouve bien la cible.".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — une durée, pas un montant",
            f"Il faut environ **{reponse:.1f} ans** pour que {grandeur} soit "
            f"multipliée par {cible_facteur}. Ce résultat ne dépend **pas** du niveau "
            "de départ : seuls comptent le taux et le facteur visé. C'est pourquoi on "
            "parle d'un « temps de doublement » propre à un taux de croissance, "
            "indépendamment de la grandeur considérée.",
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
             "Vous avez pris le logarithme des deux valeurs sans isoler la puissance "
             "au préalable. Divisez d'abord par la valeur de départ."),
            (float(cible_facteur - 1) * 100 / taux,
             "Vous avez raisonné en évolution **linéaire** : cela reviendrait à "
             "ajouter le même montant chaque année, alors que le taux s'applique "
             "chaque année à la valeur précédente."),
        ],
    )


# --- 3. Dériver ln et exp ---------------------------------------------------


def gen_derivee_log() -> Exercice:
    modele = random.choice(["ln_simple", "exp_simple", "produit_ln"])
    a = random.choice([2, 3, 4, 5])
    b = random.choice([1, 2, 3])

    if modele == "ln_simple":
        f = a * sp.log(x) + b * x
        indice = "La dérivée de $\\ln x$ est $\\frac{1}{x}$."
        piege = (sp.Rational(1, 1) / x + b,
                 f"Vous avez oublié le coefficient ${a}$ : "
                 f"$({a}\\ln x)' = \\frac{{{a}}}{{x}}$.")
    elif modele == "exp_simple":
        f = a * sp.exp(x) + b * x**2
        indice = "La dérivée de $e^x$ est $e^x$ : elle est égale à elle-même."
        piege = (a * sp.exp(x) * x + 2 * b * x,
                 "La dérivée de $e^x$ est $e^x$, sans facteur supplémentaire.")
    else:
        f = x * sp.log(x)
        indice = "C'est un produit : appliquez $(uv)' = u'v + uv'$."
        piege = (1 / x,
                 "Vous n'avez dérivé que le facteur $\\ln x$. Il s'agit d'un "
                 "**produit** : les deux facteurs varient.")

    reponse = sp.simplify(sp.diff(f, x))

    enonce = f"""
> Soit la fonction $f$ définie pour $x > 0$ par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez $f'(x)$.
"""

    etapes = [
        Etape(
            "Identifier — reconnaître la structure",
            "Avant de dériver, on repère s'il s'agit d'une somme (on dérive terme à "
            "terme), d'un produit (règle $u'v + uv'$) ou d'une composée. "
            "Les dérivées de $\\ln$ et $\\exp$ s'ajoutent simplement au catalogue "
            "déjà connu.",
        ),
        Etape(
            "Appliquer les dérivées de référence",
            r"$(\ln x)' = \dfrac{1}{x}$ et $(e^x)' = e^x$. "
            "La seconde est remarquable : l'exponentielle est la seule fonction "
            "égale à sa propre dérivée, ce qui explique qu'elle décrive toute "
            "croissance proportionnelle à elle-même.",
        ),
        Etape(
            "Assembler",
            "",
            rf"f'(x) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — un test numérique",
            f"En $x = 2$ : $f'(2) = {float(reponse.subs(x, 2)):.4f}$, à comparer au "
            f"taux d'accroissement entre $2$ et $2{{,}}001$, qui vaut "
            f"${float((f.subs(x, 2.001) - f.subs(x, 2))/0.001):.4f}$. ✓ "
            "Les deux coïncident, comme attendu.",
        ),
        Etape(
            "Interpréter",
            "Le fait que $(\\ln x)' = \\frac{1}{x}$ a une conséquence importante : "
            "la pente du logarithme diminue quand $x$ grandit. Le logarithme croît "
            "indéfiniment, mais de plus en plus lentement — d'où son usage pour "
            "représenter des grandeurs dont les grandes valeurs comptent "
            "proportionnellement moins.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="f'(x) =",
        symboles=["x"],
        indice=indice,
        pieges=[piege],
    )


# --- 4. Exponentielle contre linéaire (QCM) --------------------------------


def gen_comparaison(): 
    taux = random.choice([3, 5, 8])
    lineaire = random.choice([50, 100, 200])
    depart = random.choice([1000, 2000])

    bonne = (
        "La croissance exponentielle finit toujours par dépasser la croissance "
        "linéaire, quel que soit l'écart de départ."
    )
    options = [
        bonne,
        "La croissance linéaire reste supérieure, car elle ajoute un montant plus "
        "important chaque année.",
        "Les deux croissances restent proportionnelles l'une à l'autre.",
        "La croissance exponentielle plafonne au bout de quelques années.",
    ]
    random.shuffle(options)

    enonce = f"""
> Deux grandeurs partent de **{depart:,} unités** :
>
> - la première progresse de **{taux} % par an** (croissance exponentielle) ;
> - la seconde progresse de **{lineaire} unités par an** (croissance linéaire).
>
> Laquelle de ces affirmations est correcte sur le long terme ?
""".replace(",", "\u202f")

    cm = 1 + taux / 100
    n_croise = 1
    while depart * cm**n_croise <= depart + lineaire * n_croise and n_croise < 300:
        n_croise += 1

    etapes = [
        Etape(
            "Identifier — deux logiques d'accroissement",
            f"La croissance linéaire ajoute **toujours {lineaire} unités**. "
            f"La croissance exponentielle ajoute **{taux} % de la valeur courante**, "
            "donc un montant qui grossit avec elle. Le second mécanisme se nourrit "
            "de lui-même, pas le premier.",
        ),
        Etape(
            "Calculer quelques années",
            f"Année 1 : {depart*cm:,.0f} contre {depart + lineaire:,}. "
            f"Année 10 : {depart*cm**10:,.0f} contre {depart + 10*lineaire:,}. "
            f"Année 30 : {depart*cm**30:,.0f} contre {depart + 30*lineaire:,}."
            .replace(",", "\u202f"),
        ),
        Etape(
            "Vérifier — le croisement a bien lieu",
            f"L'exponentielle dépasse la linéaire à partir de l'année "
            f"**{n_croise}** environ. Même en partant loin derrière, elle finit "
            "toujours par passer devant : c'est un résultat général, pas un accident "
            "des chiffres choisis.",
        ),
        Etape(
            "Interpréter — pourquoi l'intuition se trompe",
            "Sur les premières années, l'écart paraît dérisoire et l'exponentielle "
            "semble inoffensive. C'est précisément ce qui rend ce mécanisme difficile "
            "à traiter politiquement : au moment où le problème devient visible, il "
            "est déjà bien engagé. La dette publique, fil rouge de ce chapitre, en "
            "est l'exemple canonique.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Affirmation correcte",
        indice="Le montant ajouté chaque année reste-t-il constant dans les deux cas ?",
        pieges=[
            ("La croissance linéaire reste supérieure, car elle ajoute un montant plus "
             "important chaque année.",
             "C'est vrai les premières années seulement. L'accroissement exponentiel "
             "grossit avec la valeur, et finit par dépasser tout montant fixe."),
            ("Les deux croissances restent proportionnelles l'une à l'autre.",
             "Leur rapport ne cesse au contraire de croître : c'est ce qui définit "
             "la différence entre les deux régimes."),
            ("La croissance exponentielle plafonne au bout de quelques années.",
             "Rien dans le modèle ne la fait plafonner : un plafond supposerait une "
             "asymptote horizontale, absente ici."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Propriétés du logarithme",
        "2️⃣ L'inconnue en exposant",
        "3️⃣ Dériver ln et exp",
        "4️⃣ Exponentielle ou linéaire ?",
    ]
)

with onglets[0]:
    st.subheader("Transformer un produit en somme")
    executer("s7_proprietes", gen_proprietes)

with onglets[1]:
    st.subheader("Combien de temps pour atteindre une cible ?")
    executer("s7_doublement", gen_temps_doublement)

with onglets[2]:
    st.subheader("Les nouvelles dérivées de référence")
    executer("s7_derivee", gen_derivee_log)

with onglets[3]:
    st.subheader("Deux régimes de croissance")
    executer("s7_comparaison", gen_comparaison)

st.markdown("---")
st.caption(
    "Semestre — séance n°7 : Logarithme et exponentielle · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
