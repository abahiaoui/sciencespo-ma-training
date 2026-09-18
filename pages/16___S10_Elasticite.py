"""Série S10 — Élasticité, dérivée logarithmique et rendements d'échelle."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S10 | Élasticité", page_icon="🔁", layout="wide")

p_, x = sp.symbols("p x")

st.title("🔁 S10 — Élasticité et rendements d'échelle")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **élasticité**, la lire correctement (elle est sans unité et se lit en
pourcentages), distinguer une réaction élastique d'une réaction rigide, et identifier
les **rendements d'échelle** d'une fonction puissance.

### 🧠 Pourquoi une notion de plus
La dérivée dépend des unités : un coût marginal s'exprime en euros par unité, et deux
grandeurs mesurées différemment sont incomparables. L'élasticité règle ce problème en
rapportant une **variation relative** à une **variation relative**. Le nombre obtenu
est pur, donc comparable d'un pays à l'autre, d'un bien à l'autre.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 10")
    st.markdown("**Élasticité de $f$ par rapport à $x$**")
    st.latex(r"e_f(x) = \frac{f'(x)}{f(x)} \times x")
    st.markdown("Lecture : si $x$ augmente de 1 %, $f$ varie de $e_f$ %.")
    st.markdown("**Cas des fonctions puissances**")
    st.latex(r"f(x) = k\,x^{\alpha} \;\Longrightarrow\; e_f(x) = \alpha")
    st.markdown("L'élasticité est **constante**, égale à l'exposant.")
    st.markdown("**Demande**")
    st.markdown(
        "$|e| > 1$ : demande **élastique** · "
        "$|e| < 1$ : demande **rigide** (inélastique)"
    )
    st.info(
        "**Sans unité**\n\n"
        "Une élasticité ne s'exprime ni en euros ni en tonnes : c'est un rapport "
        "de pourcentages."
    )

BIENS = [
    ("les trajets en transport public", "le prix du ticket"),
    ("la consommation d'électricité des ménages", "le tarif du kWh"),
    ("les inscriptions en médiathèque", "le montant de l'abonnement"),
    ("la fréquentation de la piscine municipale", "le prix d'entrée"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Élasticité d'une fonction puissance --------------------------------


def gen_puissance() -> Exercice:
    k = random.choice([50, 120, 400, 1000])
    alpha = random.choice([-2, sp.Rational(-3, 2), -1, sp.Rational(1, 2), 2, 3])
    reponse = float(alpha)

    enonce = f"""
> Une grandeur est modélisée par la fonction puissance
>
> $$ f(x) = {k}\\,x^{{{sp.latex(alpha)}}} $$
>
> Quelle est son **élasticité** par rapport à $x$ ?
"""

    f = k * x**alpha
    fp = sp.simplify(sp.diff(f, x))

    etapes = [
        Etape(
            "Identifier — appliquer la définition",
            "L'élasticité rapporte la variation relative de $f$ à la variation "
            "relative de $x$. Sa formule s'obtient en divisant la dérivée par la "
            "fonction, puis en multipliant par $x$.",
            r"e_f(x) = \frac{f'(x)}{f(x)} \times x",
        ),
        Etape(
            "Calculer la dérivée puis le rapport",
            "",
            rf"f'(x) = {sp.latex(fp)} \qquad\Rightarrow\qquad "
            rf"e_f(x) = \frac{{{sp.latex(fp)}}}{{{sp.latex(f)}}} \times x "
            rf"= {sp.latex(alpha)}",
        ),
        Etape(
            "Vérifier — le résultat ne dépend plus de $x$",
            f"L'élasticité vaut ${sp.latex(alpha)}$ **en tout point** : c'est la "
            "propriété caractéristique des fonctions puissances, et la raison pour "
            "laquelle on les utilise si souvent en modélisation. Le coefficient $k$ "
            "a disparu : seul l'exposant compte.",
        ),
        Etape(
            "Interpréter",
            f"Si $x$ augmente de 1 %, $f$ varie d'environ **{reponse:.4g} %**. "
            + (
                "L'élasticité étant négative, les deux grandeurs évoluent en sens "
                "opposés."
                if reponse < 0 else
                "Les deux grandeurs évoluent dans le même sens."
            )
            + " C'est un nombre pur, directement comparable à celui d'un autre pays "
            "ou d'un autre bien, ce qu'une dérivée ne permettrait pas.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Élasticité",
        tolerance=1e-6,
        indice="Pour une fonction puissance, le résultat se lit directement sur "
        "l'écriture.",
        pieges=[
            (float(k),
             "Le coefficient multiplicatif **disparaît** dans le calcul de "
             "l'élasticité : il se simplifie entre le numérateur et le dénominateur."),
            (float(alpha) - 1,
             "Vous avez donné l'exposant de la **dérivée**, pas l'élasticité. "
             "La multiplication finale par $x$ rétablit l'exposant d'origine."),
        ],
    )


# --- 2. Élasticité-prix ponctuelle ------------------------------------------


def gen_elasticite_prix() -> Exercice:
    bien, prix_de = random.choice(BIENS)
    # On retire tant que la demande n'est pas confortablement positive au prix
    # considéré : une demande nulle ou négative n'aurait aucun sens économique
    # et rendrait l'élasticité incalculable.
    while True:
        a = random.choice([500, 800, 1200, 2000])
        b = random.choice([20, 30, 50, 80])
        p0 = random.choice([4, 5, 6, 8, 10])
        if a - b * p0 > 0.3 * a:
            break
    # D(p) = a - b p
    D = a - b * p_
    Dp = sp.diff(D, p_)
    d0 = D.subs(p_, p0)
    reponse = float(Dp * p0 / d0)

    enonce = f"""
> La demande pour **{bien}** est modélisée par
>
> $$ D(p) = {sp.latex(D)} $$
>
> où $p$ est {prix_de}, en euros.
>
> Calculez l'**élasticité-prix** de la demande au prix $p = {p0}$ €.
> Arrondissez à $0{{,}}01$.
"""

    etapes = [
        Etape(
            "Identifier — trois ingrédients",
            "La formule demande la dérivée, la valeur de la fonction et le point "
            "considéré. Contrairement au cas des fonctions puissances, l'élasticité "
            "d'une demande affine **dépend du prix** : il n'y a pas une élasticité, "
            "mais une élasticité en chaque point.",
            r"e_D(p) = \frac{D'(p)}{D(p)} \times p",
        ),
        Etape(
            "Calculer les trois éléments",
            f"$D'(p) = {Dp}$ (constante), et "
            f"$D({p0}) = {a} - {b} \\times {p0} = {d0}$.",
            rf"e_D({p0}) = \frac{{{Dp}}}{{{d0}}} \times {p0} = {reponse:.4f}",
        ),
        Etape(
            "Vérifier — le signe est-il cohérent ?",
            "L'élasticité-prix d'une demande est **négative** : une hausse du prix "
            "fait baisser la demande. Un résultat positif signalerait une erreur de "
            "signe, ou un bien très particulier.",
        ),
        Etape(
            "Interpréter",
            f"Au prix de {p0} €, une hausse de 1 % du prix fait baisser la demande "
            f"d'environ **{abs(reponse):.2f} %**. La demande est donc "
            f"**{'élastique' if abs(reponse) > 1 else 'rigide'}** : "
            + (
                "les usagers réagissent fortement, et une hausse de tarif ferait "
                "*baisser* la recette totale."
                if abs(reponse) > 1 else
                "les usagers réagissent peu, et une hausse de tarif ferait "
                "*augmenter* la recette totale."
            )
            + " C'est exactement le calcul qui précède une décision tarifaire.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Élasticité-prix",
        tolerance=0.01,
        indice="Calculez $D'(p)$, puis $D(p_0)$, puis assemblez selon la formule.",
        pieges=[
            (float(Dp),
             "Vous avez donné la **dérivée**, qui s'exprime en unités par euro. "
             "L'élasticité est sans unité : il reste à diviser par $D(p_0)$ et à "
             "multiplier par $p_0$."),
            (float(-Dp * p0 / d0),
             "Erreur de signe : la dérivée est négative, donc l'élasticité aussi."),
            (float(d0),
             "Vous avez donné le niveau de la demande, pas son élasticité."),
        ],
    )


# --- 3. Élastique ou rigide (QCM) -------------------------------------------


def gen_lecture_elasticite() -> Exercice:
    bien, prix_de = random.choice(BIENS)
    e = random.choice([-2.4, -1.6, -1.2, -0.7, -0.4, -0.25])
    elastique = abs(e) > 1
    hausse = random.choice([5, 10])

    effet = abs(e) * hausse
    bonne = (
        f"Une hausse de {hausse} % du prix ferait baisser la demande "
        f"d'environ {effet:.0f} %, donc la recette "
        f"{'diminuerait' if elastique else 'augmenterait'}."
    )
    options = [
        bonne,
        f"Une hausse de {hausse} % du prix ferait baisser la demande "
        f"de {abs(e):.2f} unités.",
        f"Une hausse de {hausse} % du prix ferait baisser la demande "
        f"d'environ {effet:.0f} %, donc la recette "
        f"{'augmenterait' if elastique else 'diminuerait'}.",
        f"La demande ne réagirait pas au prix, l'élasticité étant inférieure à zéro.",
    ]
    random.shuffle(options)

    enonce = f"""
> L'élasticité-prix de la demande pour **{bien}** vaut **{e}**.
>
> La collectivité envisage une hausse de **{hausse} %** de {prix_de}.
>
> Quelle est la bonne analyse ?
"""

    etapes = [
        Etape(
            "Identifier — lire l'élasticité en pourcentages",
            f"Une élasticité de ${e}$ signifie : si le prix augmente de 1 %, la "
            f"demande baisse de {abs(e):.2f} %. Le signe donne le sens, la valeur "
            "absolue donne l'intensité.",
        ),
        Etape(
            "Calculer l'effet de la hausse envisagée",
            f"L'effet est approximativement proportionnel : "
            f"${hausse} \\times {abs(e):.2f} \\approx {effet:.1f}$ % de baisse "
            "de la demande. L'approximation vaut pour de petites variations, "
            "comme toute lecture marginale.",
        ),
        Etape(
            "Vérifier — l'effet sur la recette",
            f"La recette est le produit du prix par la quantité. Le prix monte de "
            f"{hausse} %, la quantité baisse de {effet:.1f} % : la recette "
            f"**{'diminue' if elastique else 'augmente'}**, puisque l'effet "
            f"{'quantité' if elastique else 'prix'} l'emporte. "
            f"C'est la conséquence directe de $|e| {'>' if elastique else '<'} 1$.",
        ),
        Etape(
            "Interpréter — ce que cela implique pour la décision",
            (
                "Face à une demande élastique, augmenter le tarif est "
                "contre-productif si l'objectif est la recette : on perd plus "
                "d'usagers qu'on ne gagne par unité."
                if elastique else
                "Face à une demande rigide, une hausse de tarif rapporte "
                "effectivement davantage — mais c'est aussi ce qui la rend "
                "socialement sensible, les usagers ne pouvant pas se détourner "
                "du service."
            ),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Analyse correcte",
        indice="La valeur absolue de l'élasticité est-elle supérieure ou inférieure "
        "à 1 ?",
        pieges=[
            (f"Une hausse de {hausse} % du prix ferait baisser la demande "
             f"de {abs(e):.2f} unités.",
             "Une élasticité est **sans unité** : elle ne se lit pas en unités de "
             "demande mais en pourcentages."),
            (f"Une hausse de {hausse} % du prix ferait baisser la demande "
             f"d'environ {effet:.0f} %, donc la recette "
             f"{'augmenterait' if elastique else 'diminuerait'}.",
             f"L'effet quantité est {'plus' if elastique else 'moins'} fort que "
             f"l'effet prix, puisque $|e| = {abs(e):.2f} "
             f"{'>' if elastique else '<'} 1$. La recette évolue donc dans l'autre "
             "sens."),
            ("La demande ne réagirait pas au prix, l'élasticité étant inférieure à zéro.",
             "Un signe négatif ne veut pas dire absence de réaction : il indique que "
             "la demande évolue en **sens opposé** au prix."),
        ],
    )


# --- 4. Rendements d'échelle (QCM) -----------------------------------------


def gen_rendements() -> Exercice:
    alpha = random.choice([0.6, 0.8, 1.0, 1.2, 1.5])
    k = random.choice([5, 10, 20])

    if alpha > 1:
        bonne = "Rendements d'échelle croissants"
    elif alpha < 1:
        bonne = "Rendements d'échelle décroissants"
    else:
        bonne = "Rendements d'échelle constants"

    options = [
        "Rendements d'échelle croissants",
        "Rendements d'échelle décroissants",
        "Rendements d'échelle constants",
    ]

    enonce = f"""
> La production d'un service est modélisée par
>
> $$ Y(L) = {k}\\,L^{{{alpha}}} $$
>
> où $L$ est la quantité de travail mobilisée.
>
> De quel type de **rendements d'échelle** s'agit-il ?
"""

    facteur = 2
    effet = facteur**alpha

    etapes = [
        Etape(
            "Identifier — l'exposant est l'élasticité",
            f"Pour une fonction puissance, l'élasticité vaut directement l'exposant, "
            f"soit **{alpha}**. Elle se lit : si $L$ augmente de 1 %, la production "
            f"varie de {alpha} %.",
        ),
        Etape(
            "Calculer — doubler le facteur de production",
            f"Multiplier $L$ par {facteur} multiplie $Y$ par "
            f"${facteur}^{{{alpha}}} \\approx {effet:.3f}$.",
            rf"Y({facteur}L) = {k}({facteur}L)^{{{alpha}}} = "
            rf"{facteur}^{{{alpha}}}\,Y(L) \approx {effet:.3f}\,Y(L)",
        ),
        Etape(
            "Vérifier — comparer au doublement",
            f"En doublant le travail, la production est multipliée par "
            f"{effet:.3f}, soit "
            f"{'plus' if alpha > 1 else 'moins' if alpha < 1 else 'exactement'} "
            f"que 2. Les rendements sont donc **{bonne.split()[-1]}**. ✓",
        ),
        Etape(
            "Interpréter — ce que cela dit de l'organisation",
            (
                "Des rendements croissants signifient qu'il est avantageux de "
                "concentrer l'activité : un grand service est plus efficace que "
                "deux petits. C'est l'argument classique en faveur des fusions de "
                "communes ou d'hôpitaux."
                if alpha > 1 else
                "Des rendements décroissants signifient qu'ajouter des moyens "
                "rapporte de moins en moins : au-delà d'un certain point, la "
                "coordination coûte plus qu'elle ne rapporte. C'est l'argument "
                "inverse, en faveur d'unités de taille limitée."
                if alpha < 1 else
                "Des rendements constants signifient que la taille de l'unité est "
                "indifférente à l'efficacité : deux petits services valent un grand. "
                "L'argument d'échelle ne peut alors pas être invoqué."
            ),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Type de rendements",
        indice="Comparez l'exposant à 1.",
        pieges=[
            ("Rendements d'échelle croissants" if alpha < 1
             else "Rendements d'échelle décroissants" if alpha > 1
             else "Rendements d'échelle croissants",
             f"Comparez l'exposant à 1 : ici $\\alpha = {alpha}$, donc "
             f"{'inférieur' if alpha < 1 else 'supérieur' if alpha > 1 else 'égal'} "
             "à 1."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Élasticité d'une puissance",
        "2️⃣ Élasticité-prix",
        "3️⃣ Élastique ou rigide ?",
        "4️⃣ Rendements d'échelle",
    ]
)

with onglets[0]:
    st.subheader("L'élasticité se lit sur l'exposant")
    executer("s10_puissance", gen_puissance)

with onglets[1]:
    st.subheader("Élasticité-prix de la demande")
    executer("s10_prix", gen_elasticite_prix)

with onglets[2]:
    st.subheader("Que faire du tarif ?")
    executer("s10_lecture", gen_lecture_elasticite)

with onglets[3]:
    st.subheader("La taille compte-t-elle ?")
    executer("s10_rendements", gen_rendements)

st.markdown("---")
st.caption(
    "Semestre — séance n°10 : Élasticité et rendements d'échelle · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
