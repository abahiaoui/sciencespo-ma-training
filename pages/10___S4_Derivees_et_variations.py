"""Série S4 — Du signe de la dérivée au tableau de variations."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S4 | Dérivées et variations", page_icon="↗️", layout="wide")

x = sp.Symbol("x")

st.title("↗️ S4 — Dérivées et variations")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Trouver les **points critiques** ($f'(x) = 0$), déterminer le **signe** de la dérivée,
en déduire les variations de $f$, et identifier un maximum ou un minimum.

### 🧠 L'idée qui organise tout le chapitre
On ne regarde plus la valeur de $f'$, mais son **signe**. Une dérivée positive veut
dire que $f$ monte ; négative, qu'elle descend ; nulle, qu'elle marque une pause.
Étudier une fonction devient donc étudier le signe d'une autre fonction — souvent
beaucoup plus simple.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 4")
    st.latex(r"f'(x) > 0 \;\Rightarrow\; f \text{ croissante}")
    st.latex(r"f'(x) < 0 \;\Rightarrow\; f \text{ décroissante}")
    st.latex(r"f'(x) = 0 \;\Rightarrow\; \text{point critique}")
    st.markdown("**Extremum**")
    st.markdown(
        "$f'$ change de signe **+ → −** : maximum local\n\n"
        "$f'$ change de signe **− → +** : minimum local\n\n"
        "$f'$ s'annule **sans changer de signe** : pas d'extremum"
    )
    st.error(
        "**L'erreur interdite**\n\n"
        "Conclure à un extremum dès que $f'(a) = 0$.\n\n"
        "Il faut que $f'$ **change de signe**."
    )
    st.info(
        "**Méthode**\n\n"
        "1. Dériver · 2. Résoudre $f'(x) = 0$ · 3. Étudier le signe de $f'$ · "
        "4. Conclure sur $f$"
    )

CONTEXTES = [
    ("le bénéfice de l'atelier", "réparations", "€"),
    ("la recette du service", "abonnements", "€"),
    ("le rendement du dispositif", "bénéficiaires", "points"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Point critique ------------------------------------------------------


def gen_point_critique() -> Exercice:
    a = random.choice([1, 2, 3, -1, -2])
    sol = random.choice([-4, -2, 1, 3, 5, 6])
    b = -2 * a * sol
    c = random.choice([-6, 0, 4, 10])
    f = a * x**2 + b * x + c
    fp = sp.diff(f, x)

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> En quelle valeur de $x$ la dérivée s'annule-t-elle ?
"""

    etapes = [
        Etape(
            "Identifier — pourquoi chercher là où $f'$ s'annule",
            "Ce sont les seuls points où $f$ peut changer de sens. Ailleurs, $f'$ garde "
            "un signe constant et $f$ varie de façon monotone. Les points critiques "
            "découpent donc l'axe en zones de comportement homogène.",
        ),
        Etape(
            "Dériver",
            "",
            rf"f'(x) = {sp.latex(fp)}",
        ),
        Etape(
            "Résoudre $f'(x) = 0$",
            "C'est une équation du premier degré, comme en P4.",
            rf"{sp.latex(fp)} = 0 \iff x = \frac{{{-b}}}{{{2*a}}} = {sol}",
        ),
        Etape(
            "Vérifier — la dérivée s'annule-t-elle bien ?",
            f"$f'({sol}) = {2*a} \\times {sol} + ({b}) = {2*a*sol + b}$. ✓",
        ),
        Etape(
            "Interpréter — s'annuler ne suffit pas",
            f"On sait maintenant **où** $f$ peut changer de sens, pas encore s'il "
            f"s'agit d'un maximum ou d'un minimum. Comme $a = {a}$ est "
            f"{'positif' if a > 0 else 'négatif'}, la parabole est tournée vers le "
            f"{'haut' if a > 0 else 'bas'} : ce point sera donc un "
            f"**{'minimum' if a > 0 else 'maximum'}**. C'est l'objet des onglets "
            "suivants.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="x =",
        tolerance=1e-6,
        indice="Dérivez, puis résolvez l'équation $f'(x) = 0$.",
        pieges=[
            (float(-c / b) if b != 0 else 0.0,
             "Vous avez résolu $f(x) = 0$ ou une autre équation : c'est bien la "
             "**dérivée** qu'il faut annuler."),
            (float(b),
             "Vous avez donné un coefficient, pas la solution de l'équation."),
        ],
    )


# --- 2. Sens de variation sur un intervalle (QCM) --------------------------


def gen_sens_variation() -> Exercice:
    a = random.choice([1, 2, -1, -2])
    sol = random.choice([-2, 1, 3, 4])
    b = -2 * a * sol
    c = random.choice([-3, 2, 8])
    f = a * x**2 + b * x + c
    fp = sp.diff(f, x)

    cote = random.choice(["gauche", "droite"])
    x_test = sol - 2 if cote == "gauche" else sol + 2
    valeur_fp = fp.subs(x, x_test)
    croissante = valeur_fp > 0

    borne_g = sol - 4 if cote == "gauche" else sol
    borne_d = sol if cote == "gauche" else sol + 4

    bonne = "f est croissante sur cet intervalle" if croissante else \
        "f est décroissante sur cet intervalle"
    options = [
        "f est croissante sur cet intervalle",
        "f est décroissante sur cet intervalle",
        "f est constante sur cet intervalle",
    ]

    enonce = f"""
> Soit $f(x) = {sp.latex(f)}$, dont la dérivée est $f'(x) = {sp.latex(fp)}$.
>
> Que peut-on dire de $f$ sur l'intervalle $]{borne_g}\\,;\\,{borne_d}[$ ?
"""

    etapes = [
        Etape(
            "Identifier — c'est le signe de $f'$ qui décide",
            "On n'a pas besoin de calculer $f$ : le signe de la dérivée sur "
            "l'intervalle suffit à conclure. C'est tout l'intérêt de la méthode.",
        ),
        Etape(
            "Calculer le signe de $f'$ sur l'intervalle",
            f"La dérivée est affine et s'annule en ${sol}$. Testons un point de "
            f"l'intervalle, par exemple $x = {x_test}$ :",
            rf"f'({x_test}) = {sp.latex(fp.subs(x, x_test))} = {valeur_fp}"
            rf"\quad ({'positif' if valeur_fp > 0 else 'négatif'})",
        ),
        Etape(
            "Vérifier — un seul test suffit-il ?",
            f"Oui, parce que $f'$ est affine et ne change de signe qu'en ${sol}$, qui "
            "est une borne de l'intervalle. Sur tout l'intérieur de l'intervalle, le "
            "signe est donc constant — c'est précisément pour cela qu'on découpe l'axe "
            "aux points critiques.",
        ),
        Etape(
            "Interpréter",
            f"$f'$ étant {'positive' if croissante else 'négative'} sur cet "
            f"intervalle, $f$ y est **{'croissante' if croissante else 'décroissante'}**. "
            "Notez que la valeur de $f'$ n'a servi à rien : seul son signe compte. "
            "Une dérivée valant 0,01 ou 400 donne la même conclusion qualitative.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Conclusion",
        indice="Testez le signe de $f'$ en un point quelconque de l'intervalle.",
        pieges=[
            ("f est constante sur cet intervalle",
             "$f$ ne serait constante que si $f'$ était **nulle partout** sur "
             f"l'intervalle. Ici $f'$ ne s'annule qu'en un seul point, ${sol}$."),
            ("f est croissante sur cet intervalle" if not croissante
             else "f est décroissante sur cet intervalle",
             f"Vérifiez le signe : $f'({x_test}) = {valeur_fp}$, donc "
             f"{'positive' if valeur_fp > 0 else 'négative'}."),
        ],
    )


# --- 3. Valeur de l'extremum ------------------------------------------------


def gen_extremum() -> Exercice:
    contexte, unite_x, unite_y = random.choice(CONTEXTES)
    a = random.choice([-1, -2, -3])  # maximum
    sol = random.choice([20, 30, 40, 50, 60])
    b = -2 * a * sol
    c = random.choice([200, 500, 800, 1200])
    f = a * x**2 + b * x + c
    reponse = float(f.subs(x, sol))

    enonce = f"""
> On modélise {contexte} par
>
> $$ B(q) = {sp.latex(f.subs(x, sp.Symbol('q')))} \\qquad \\text{{(en {unite_y})}} $$
>
> où $q$ est le nombre de {unite_x}.
>
> Quelle est la **valeur maximale** de $B$ ?
"""

    etapes = [
        Etape(
            "Identifier — deux questions à ne pas confondre",
            "« Pour quelle valeur de $q$ ? » et « combien vaut le maximum ? » sont "
            "deux questions distinctes. La dérivée répond à la première ; il faut "
            "ensuite revenir à $B$ pour répondre à la seconde.",
        ),
        Etape(
            "Trouver le point critique",
            f"$B'(q) = {2*a}q + {b}$, qui s'annule pour $q = {sol}$.",
            rf"B'(q) = 0 \iff q = {sol}\ \text{{{unite_x}}}",
        ),
        Etape(
            "Calculer la valeur du maximum",
            f"On revient à la fonction de départ — c'est l'étape que l'on oublie.",
            rf"B({sol}) = {a}({sol})^2 + {b} \times {sol} + {c} = {reponse:.0f}"
            rf"\ \text{{{unite_y}}}",
        ),
        Etape(
            "Vérifier — est-ce bien un maximum ?",
            f"Testons de part et d'autre : $B({sol - 10}) = "
            f"{float(f.subs(x, sol-10)):.0f}$ et $B({sol + 10}) = "
            f"{float(f.subs(x, sol+10)):.0f}$, tous deux inférieurs à "
            f"{reponse:.0f}. ✓ La dérivée passe bien du positif au négatif.",
        ),
        Etape(
            "Interpréter",
            f"Le maximum vaut **{reponse:.0f} {unite_y}**, atteint pour {sol} "
            f"{unite_x}. Les deux nombres répondent à des questions différentes : "
            "l'un dit *combien on gagne au mieux*, l'autre *ce qu'il faut faire pour "
            "l'obtenir*. En décision publique, c'est le second qui est actionnable.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur maximale",
        unite=unite_y,
        tolerance=1e-6,
        indice="Trouvez d'abord où la dérivée s'annule, puis revenez à $B$.",
        pieges=[
            (float(sol),
             f"Vous avez donné la **quantité** {sol} qui réalise le maximum, pas la "
             "valeur du maximum lui-même. Il reste à calculer $B$ en ce point."),
            (float(c),
             "Vous avez donné la valeur en $q = 0$, c'est-à-dire l'ordonnée à "
             "l'origine, pas le maximum."),
        ],
    )


# --- 4. Annulation sans extremum (QCM) -------------------------------------


def gen_sans_extremum() -> Exercice:
    a = random.choice([1, 2])
    x0 = random.choice([-2, 1, 2, 3])
    # f(x) = a(x - x0)^3 + k : f' = 3a(x-x0)^2 >= 0, s'annule sans changer de signe
    k = random.choice([-5, 0, 4])
    f = sp.expand(a * (x - x0) ** 3 + k)
    fp = sp.expand(sp.diff(f, x))

    bonne = f"f n'a ni maximum ni minimum en {x0} : elle reste croissante"
    options = [
        bonne,
        f"f admet un maximum en {x0}",
        f"f admet un minimum en {x0}",
        f"f est constante au voisinage de {x0}",
    ]
    random.shuffle(options)

    enonce = f"""
> Soit $f(x) = {sp.latex(f)}$, dont la dérivée est
>
> $$ f'(x) = {sp.latex(fp)} = {a*3}(x - {x0})^2 $$
>
> La dérivée s'annule en $x = {x0}$. Que peut-on en conclure sur $f$ ?
"""

    etapes = [
        Etape(
            "Identifier — annulation n'est pas extremum",
            f"$f'({x0}) = 0$ dit seulement que la tangente y est **horizontale**. "
            "Pour conclure à un extremum, il faut une information de plus : que "
            "la dérivée **change de signe** en ce point.",
        ),
        Etape(
            "Étudier le signe de la dérivée",
            f"$f'(x) = {3*a}(x - {x0})^2$ est un carré multiplié par un nombre "
            f"positif : il est donc **positif ou nul partout**, et ne s'annule qu'en "
            f"${x0}$.",
            rf"f'({x0 - 1}) = {float(fp.subs(x, x0-1)):.0f} > 0 \qquad "
            rf"f'({x0 + 1}) = {float(fp.subs(x, x0+1)):.0f} > 0",
        ),
        Etape(
            "Vérifier — comparer les valeurs de $f$",
            f"$f({x0 - 1}) = {float(f.subs(x, x0-1)):.0f}$, "
            f"$f({x0}) = {float(f.subs(x, x0)):.0f}$, "
            f"$f({x0 + 1}) = {float(f.subs(x, x0+1)):.0f}$ : "
            "les valeurs continuent de croître en traversant le point. "
            "Il n'y a donc ni maximum ni minimum.",
        ),
        Etape(
            "Interpréter — le point d'inflexion",
            f"En ${x0}$, la courbe marque une pause dans sa pente sans changer de "
            "sens : elle change en revanche de **courbure**. Ce type de point sera "
            "nommé et étudié en séance 6 — c'est un point d'inflexion à tangente "
            "horizontale.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Conclusion",
        indice="Le signe de $f'$ change-t-il de part et d'autre du point ?",
        pieges=[
            (f"f admet un maximum en {x0}",
             "La dérivée s'annule, mais elle ne change pas de signe : elle reste "
             "positive des deux côtés. Il n'y a donc pas de maximum."),
            (f"f admet un minimum en {x0}",
             "Même remarque : pour un minimum, il faudrait que $f'$ passe du négatif "
             "au positif. Ici elle reste positive."),
            (f"f est constante au voisinage de {x0}",
             f"$f$ ne serait constante que si $f'$ était nulle sur tout un intervalle. "
             f"Ici elle ne s'annule qu'au seul point ${x0}$."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Point critique",
        "2️⃣ Sens de variation",
        "3️⃣ Valeur de l'extremum",
        "4️⃣ Annulation sans extremum",
    ]
)

with onglets[0]:
    st.subheader("Où la dérivée s'annule-t-elle ?")
    executer("s4_critique", gen_point_critique)

with onglets[1]:
    st.subheader("Du signe de f' aux variations de f")
    executer("s4_sens", gen_sens_variation)

with onglets[2]:
    st.subheader("Combien vaut le maximum ?")
    executer("s4_extremum", gen_extremum)

with onglets[3]:
    st.subheader("Quand f' s'annule sans changer de signe")
    executer("s4_sans_extremum", gen_sans_extremum)

st.markdown("---")
st.caption(
    "Semestre — séance n°4 : Dérivées et variations · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
