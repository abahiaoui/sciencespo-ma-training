"""Série S5 — Limites et asymptotes."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S5 | Limites et asymptotes", page_icon="➡️", layout="wide")

x, q = sp.symbols("x q")

st.title("➡️ S5 — Limites et asymptotes")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Déterminer le comportement d'une fonction **aux bornes** de son domaine : ce qu'elle
devient quand $x$ devient très grand, et ce qui se passe au voisinage d'une valeur
interdite.

### 🧠 Pourquoi cela intéresse les sciences sociales
Une limite répond à la question « et à long terme ? ». Un coût moyen qui tend vers une
valeur plancher, une part qui plafonne, une dette qui explose : dans chaque cas, c'est
le comportement asymptotique qui porte la conclusion, pas la valeur en un point.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 5")
    st.markdown("**Limites de référence**")
    st.latex(r"\lim_{x \to +\infty} \frac{k}{x} = 0 \qquad "
             r"\lim_{x \to +\infty} x^n = +\infty")
    st.markdown("**Quotient de polynômes en $+\\infty$**")
    st.markdown("On garde les **termes de plus haut degré** du numérateur et du "
                "dénominateur, puis on simplifie.")
    st.markdown("**Asymptotes**")
    st.markdown(
        "$\\lim_{x \\to +\\infty} f(x) = L$ : asymptote **horizontale** $y = L$\n\n"
        "$\\lim_{x \\to a} f(x) = \\pm\\infty$ : asymptote **verticale** $x = a$"
    )
    st.info(
        "**Le réflexe**\n\n"
        "Face à une forme indéterminée, factorisez par le terme dominant. "
        "C'est presque toujours ce qui débloque."
    )

SERVICES = [
    ("un atelier municipal", "réparations", "€"),
    ("une cuisine centrale", "repas", "€"),
    ("un service instructeur", "dossiers", "€"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Limite d'un quotient en +∞ ------------------------------------------


def gen_limite_quotient() -> Exercice:
    a = random.choice([2, 3, 4, 6, 8])
    b = random.choice([1, 2, 4, 5])
    c = random.choice([-10, -3, 5, 12])
    d = random.choice([-6, 2, 9])
    f = (a * x + c) / (b * x + d)
    reponse = float(sp.Rational(a, b))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = \\frac{{{sp.latex(a*x + c)}}}{{{sp.latex(b*x + d)}}} $$
>
> Vers quelle valeur $f(x)$ tend-il lorsque $x \\to +\\infty$ ?
"""

    etapes = [
        Etape(
            "Identifier — une forme indéterminée",
            "Numérateur et dénominateur tendent tous deux vers $+\\infty$. "
            "Le rapport $\\frac{\\infty}{\\infty}$ ne permet aucune conclusion "
            "directe : il faut transformer l'expression.",
        ),
        Etape(
            "Factoriser par le terme dominant",
            "On met $x$ en facteur en haut et en bas, puis on simplifie.",
            rf"\frac{{{a}x + {c}}}{{{b}x + {d}}} = "
            rf"\frac{{x\left({a} + \frac{{{c}}}{{x}}\right)}}"
            rf"{{x\left({b} + \frac{{{d}}}{{x}}\right)}} = "
            rf"\frac{{{a} + \frac{{{c}}}{{x}}}}{{{b} + \frac{{{d}}}{{x}}}}",
        ),
        Etape(
            "Passer à la limite",
            "Les termes en $\\frac{k}{x}$ tendent vers 0 : il ne reste que le rapport "
            "des coefficients dominants.",
            rf"\lim_{{x \to +\infty}} f(x) = \frac{{{a}}}{{{b}}} = {reponse:.4g}",
        ),
        Etape(
            "Vérifier — évaluer pour un grand $x$",
            f"$f(1000) = {float(f.subs(x, 1000)):.5f}$, très proche de "
            f"${reponse:.4g}$. ✓ Un test numérique ne démontre rien, mais il "
            "confirme qu'on ne s'est pas trompé de sens.",
        ),
        Etape(
            "Interpréter — l'asymptote horizontale",
            f"La courbe s'approche indéfiniment de la droite $y = {reponse:.4g}$ sans "
            "l'atteindre : c'est une **asymptote horizontale**. Autrement dit, la "
            "fonction **plafonne**. Pour un ratio en sciences sociales, cela signifie "
            "qu'au-delà d'une certaine taille, la valeur ne bouge pratiquement plus.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Limite en +∞",
        tolerance=1e-6,
        indice="Factorisez par $x$ au numérateur et au dénominateur.",
        pieges=[
            (float(sp.Rational(c, d)) if d != 0 else 0.0,
             "Vous avez gardé les termes **constants**. En $+\\infty$, ce sont les "
             "termes de plus haut degré qui dominent, pas les constantes."),
            (0.0,
             "La limite n'est pas nulle : numérateur et dénominateur croissent au "
             "**même rythme**, donc leur rapport tend vers une valeur finie non nulle."),
        ],
    )


# --- 2. Limite d'un coût moyen ----------------------------------------------


def gen_cout_moyen_limite() -> Exercice:
    service, unite, devise = random.choice(SERVICES)
    fixe = random.choice([2000, 4500, 8000, 12000])
    unitaire = random.choice([6, 9, 14, 22])
    reponse = float(unitaire)

    enonce = f"""
> Pour **{service}**, le coût total de production de $q$ {unite} est
>
> $$ C(q) = {fixe} + {unitaire}q $$
>
> Le coût moyen par unité vaut donc $CM(q) = \\dfrac{{C(q)}}{{q}}$.
>
> Vers quelle valeur le coût moyen tend-il quand $q \\to +\\infty$ ?
"""

    etapes = [
        Etape(
            "Identifier — décomposer avant de passer à la limite",
            "Le coût moyen est une fraction dont le numérateur est une somme. "
            "En la séparant en deux, chaque morceau devient lisible individuellement.",
            rf"CM(q) = \frac{{{fixe} + {unitaire}q}}{{q}} = "
            rf"\frac{{{fixe}}}{{q}} + {unitaire}",
        ),
        Etape(
            "Passer à la limite terme par terme",
            f"Le terme $\\frac{{{fixe}}}{{q}}$ tend vers 0 ; le terme ${unitaire}$ "
            "est constant et ne bouge pas.",
            rf"\lim_{{q \to +\infty}} CM(q) = 0 + {unitaire} = {unitaire}",
        ),
        Etape(
            "Vérifier — quelques valeurs",
            f"$CM(100) = {fixe/100 + unitaire:.2f}$ · "
            f"$CM(1000) = {fixe/1000 + unitaire:.2f}$ · "
            f"$CM(10000) = {fixe/10000 + unitaire:.2f}$ {devise}. "
            f"La décroissance vers {unitaire} est nette, et de plus en plus lente. ✓",
        ),
        Etape(
            "Interpréter — les économies d'échelle ont une limite",
            f"Le coût moyen diminue quand on produit plus, mais il ne descendra jamais "
            f"en dessous de **{unitaire} {devise}** : c'est le coût unitaire variable, "
            "incompressible. Les économies d'échelle portent uniquement sur la "
            "répartition du coût fixe, et leur bénéfice s'épuise. "
            "C'est un argument central des débats sur la taille optimale d'un service "
            "public.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Limite du coût moyen",
        unite=devise,
        tolerance=1e-6,
        indice="Séparez la fraction en deux termes avant de passer à la limite.",
        pieges=[
            (0.0,
             "Le coût moyen ne tend pas vers 0 : le terme constant "
             f"${unitaire}$ subsiste quoi qu'il arrive."),
            (float(fixe),
             "Le coût fixe est justement le terme qui **disparaît** à la limite, "
             "puisqu'il se répartit sur un nombre croissant d'unités."),
            (float(fixe + unitaire),
             "Vous avez additionné les deux paramètres sans passer à la limite."),
        ],
    )


# --- 3. Asymptote verticale -------------------------------------------------


def gen_asymptote_verticale() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-12, -8, -6, 4, 9])
    k = random.choice([1, 3, 5, 7])
    reponse = float(sp.Rational(-b, a))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = \\frac{{{k}}}{{{sp.latex(a*x + b)}}} $$
>
> Cette fonction admet une **asymptote verticale**. Pour quelle valeur de $x$ ?
"""

    etapes = [
        Etape(
            "Identifier — une asymptote verticale naît d'une division par zéro",
            "Quand le dénominateur s'approche de 0 alors que le numérateur reste non "
            "nul, le quotient devient arbitrairement grand en valeur absolue. "
            "C'est exactement la situation d'une asymptote verticale.",
        ),
        Etape(
            "Annuler le dénominateur",
            "",
            rf"{sp.latex(a*x + b)} = 0 \iff x = {sp.latex(sp.Rational(-b, a))}",
        ),
        Etape(
            "Vérifier — s'approcher de chaque côté",
            f"Pour $x$ légèrement supérieur à ${sp.latex(sp.Rational(-b, a))}$, le "
            f"dénominateur est un petit nombre positif et $f(x)$ est très grand. "
            "Pour $x$ légèrement inférieur, il est négatif et $f(x)$ très grand "
            "négativement. La courbe part donc dans deux directions opposées de part "
            "et d'autre de l'asymptote.",
        ),
        Etape(
            "Interpréter — une asymptote verticale est un signal",
            "Dans un modèle, elle indique presque toujours qu'une grandeur explose "
            "au voisinage d'un seuil : une capacité saturée, une ressource épuisée. "
            "C'est un point où le modèle cesse d'être exploitable — et cette "
            "information est utile en soi.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Asymptote verticale x =",
        tolerance=1e-6,
        indice="Cherchez la valeur qui annule le dénominateur.",
        pieges=[
            (float(sp.Rational(b, a)),
             "Erreur de signe : résoudre $ax + b = 0$ donne $x = -\\frac{b}{a}$."),
            (float(k),
             "Vous avez donné le numérateur. C'est le **dénominateur** qui doit "
             "s'annuler."),
        ],
    )


# --- 4. Croissance comparée (QCM) -------------------------------------------


def gen_croissance_comparee() -> Exercice:
    a = random.choice([2, 3, 5])
    n = random.choice([2, 3])
    b = random.choice([50, 100, 500, 1000])

    bonne = f"f(x) tend vers +∞ : le terme en x^{n} finit par dominer"
    options = [
        bonne,
        f"f(x) tend vers {b} : le terme constant l'emporte",
        "f(x) tend vers 0",
        f"f(x) tend vers {a} : c'est le coefficient dominant",
    ]
    random.shuffle(options)

    enonce = f"""
> Soit la fonction
>
> $$ f(x) = {a}x^{{{n}}} - {b} $$
>
> Quel est son comportement lorsque $x \\to +\\infty$ ?
"""

    etapes = [
        Etape(
            "Identifier — comparer les rythmes de croissance",
            f"Deux termes s'opposent : ${a}x^{{{n}}}$, qui croît sans limite, et "
            f"$-{b}$, qui reste fixe. La question est de savoir lequel l'emporte "
            "à long terme.",
        ),
        Etape(
            "Calculer quelques valeurs",
            f"$f(10) = {a*10**n - b}$ · $f(50) = {a*50**n - b}$ · "
            f"$f(100) = {a*100**n - b}$. "
            f"La soustraction de ${b}$ devient rapidement négligeable devant le "
            "premier terme.",
        ),
        Etape(
            "Vérifier — factoriser par le terme dominant",
            f"$f(x) = x^{{{n}}}\\left({a} - \\frac{{{b}}}{{x^{{{n}}}}}\\right)$. "
            f"Le contenu de la parenthèse tend vers ${a}$, strictement positif, et "
            f"$x^{{{n}}}$ tend vers $+\\infty$ : le produit tend donc vers "
            "$+\\infty$. ✓",
        ),
        Etape(
            "Interpréter — une constante ne résiste jamais à une croissance",
            "Aussi grande soit-elle, une quantité fixe finit toujours par être "
            "dépassée par une quantité qui croît. C'est ce raisonnement qui fonde "
            "les alertes sur la soutenabilité de long terme — et c'est aussi pourquoi "
            "il faut toujours demander *à quel horizon* une comparaison est faite.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Comportement en +∞",
        indice="Lequel des deux termes grandit, et lequel reste fixe ?",
        pieges=[
            (f"f(x) tend vers {b} : le terme constant l'emporte",
             f"Une constante ne peut pas « l'emporter » : elle ne bouge pas, tandis "
             f"que ${a}x^{{{n}}}$ croît sans limite."),
            ("f(x) tend vers 0",
             "Rien ici ne pousse la fonction vers 0 : aucun terme ne décroît."),
            (f"f(x) tend vers {a} : c'est le coefficient dominant",
             "Le coefficient dominant donne la limite dans un **quotient** de "
             "polynômes de même degré. Ici il s'agit d'une différence, pas d'un "
             "quotient."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Limite d'un quotient",
        "2️⃣ Limite d'un coût moyen",
        "3️⃣ Asymptote verticale",
        "4️⃣ Croissance comparée",
    ]
)

with onglets[0]:
    st.subheader("Quotient de polynômes en +∞")
    executer("s5_quotient", gen_limite_quotient)

with onglets[1]:
    st.subheader("Jusqu'où descend le coût moyen ?")
    executer("s5_cout_moyen", gen_cout_moyen_limite)

with onglets[2]:
    st.subheader("Où la fonction explose-t-elle ?")
    executer("s5_verticale", gen_asymptote_verticale)

with onglets[3]:
    st.subheader("Qui l'emporte à long terme ?")
    executer("s5_croissance", gen_croissance_comparee)

st.markdown("---")
st.caption(
    "Semestre — séance n°5 : Limites et asymptotes · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
