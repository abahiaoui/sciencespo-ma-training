"""Série S2 — Taux d'accroissement et droite sécante."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S2 | Taux d'accroissement", page_icon="📊", layout="wide")

x, h = sp.symbols("x h")

st.title("📊 S2 — Taux d'accroissement")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer un **taux d'accroissement moyen** entre deux points, l'interpréter avec son
unité, et observer ce qu'il devient quand les deux points se rapprochent.

### 🧠 Où cela mène
Le taux d'accroissement est la pente d'une droite — la **sécante** qui joint deux
points de la courbe. Toute la séance 3 consistera à faire tendre l'écart entre ces
deux points vers zéro. La dérivée n'est rien d'autre que cette limite, et vous en
aurez calculé les premiers cas ici.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 2")
    st.markdown("**Taux d'accroissement moyen**")
    st.latex(r"\tau = \frac{f(b) - f(a)}{b - a}")
    st.markdown("**Écriture avec un pas $h$**")
    st.latex(r"\tau(h) = \frac{f(a+h) - f(a)}{h}")
    st.info(
        "**La lecture**\n\n"
        "« En moyenne, entre $a$ et $b$, $f$ varie de $\\tau$ unités "
        "par unité de $x$. »\n\n"
        "C'est la pente de la **sécante** joignant les deux points."
    )
    st.error(
        "**À ne pas confondre**\n\n"
        "La **variation** $f(b) - f(a)$ (en unités de $y$)\n\n"
        "et le **taux** $\\dfrac{f(b)-f(a)}{b-a}$ (en unités de $y$ par unité de $x$)."
    )

SERIES = [
    ("le nombre de demandes déposées", "mois", "demandes"),
    ("la fréquentation d'un équipement", "semaines", "visites"),
    ("le stock de logements vacants", "années", "logements"),
    ("les émissions du parc automobile", "années", "milliers de tonnes"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Taux d'accroissement entre deux valeurs ----------------------------


def gen_taux_moyen() -> Exercice:
    serie, unite_x, unite_y = random.choice(SERIES)
    a = random.choice([0, 1, 2, 3])
    b = a + random.choice([2, 3, 4, 5])
    fa = random.choice([120, 180, 250, 340, 500])
    variation = random.choice([-90, -60, -30, 40, 75, 120, 200])
    fb = fa + variation
    reponse = (fb - fa) / (b - a)

    enonce = f"""
> On observe {serie} à deux dates :
>
> - au temps $t = {a}$ ({unite_x}) : **{fa:,} {unite_y}**
> - au temps $t = {b}$ ({unite_x}) : **{fb:,} {unite_y}**
>
> Calculez le **taux d'accroissement moyen** entre ces deux dates.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — un taux est un rapport, pas une différence",
            f"La variation brute vaut ${fb} - {fa} = {fb - fa}$ {unite_y}. Mais elle "
            f"s'est produite sur ${b} - {a} = {b - a}$ {unite_x} : pour comparer des "
            "périodes de durées différentes, il faut **rapporter** la variation à la "
            "durée.",
        ),
        Etape(
            "Calculer",
            "",
            rf"\tau = \frac{{f({b}) - f({a})}}{{{b} - {a}}} "
            rf"= \frac{{{fb - fa}}}{{{b - a}}} = {reponse:.2f}",
        ),
        Etape(
            "Vérifier — le signe et l'unité",
            f"Le taux est **{'positif' if reponse > 0 else 'négatif'}**, ce qui "
            f"correspond bien à une {'hausse' if reponse > 0 else 'baisse'} entre les "
            f"deux dates. Son unité est **{unite_y} par {unite_x[:-1]}** : un taux "
            "porte toujours deux unités, et les oublier rend l'interprétation "
            "impossible.",
        ),
        Etape(
            "Interpréter — « en moyenne »",
            f"Entre $t = {a}$ et $t = {b}$, {serie} a varié en moyenne de "
            f"**{_fr(reponse)} {unite_y} par {unite_x[:-1]}**. Le mot « en moyenne » "
            "est essentiel : le taux ne dit rien de ce qui s'est passé **entre** les "
            "deux dates, où l'évolution a pu être très irrégulière. C'est exactement "
            "la limite que la dérivée viendra lever.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux d'accroissement moyen",
        unite=f"{unite_y}/{unite_x[:-1]}",
        tolerance=0.005,
        indice="Variation de la grandeur divisée par la durée écoulée.",
        pieges=[
            (float(fb - fa),
             f"C'est la **variation** totale en {unite_y}, pas le taux. Il reste à la "
             f"diviser par les {b - a} {unite_x} écoulés."),
            (float(b - a) / (fb - fa) if fb != fa else 0.0,
             "Vous avez inversé le rapport : la variation de la grandeur va au "
             "**numérateur**, la durée au dénominateur."),
            (100 * (fb - fa) / fa,
             "Vous avez calculé un taux de variation **en pourcentage**. Ce n'est pas "
             "la même chose : le taux d'accroissement rapporte la variation à la "
             "**durée**, pas à la valeur initiale."),
        ],
    )


# --- 2. Interpréter un taux (QCM) -------------------------------------------


def gen_interpretation() -> Exercice:
    serie, unite_x, unite_y = random.choice(SERIES)
    tau = random.choice([-24, -15, -8, 12, 30, 45])

    sens = "augmenté" if tau > 0 else "diminué"
    bonne = (
        f"En moyenne, {serie} a {sens} de {abs(tau)} {unite_y} "
        f"par {unite_x[:-1]} sur la période."
    )
    options = [
        bonne,
        f"{serie.capitalize()} valait {abs(tau)} {unite_y} en moyenne sur la période.",
        f"{serie.capitalize()} a {sens} de {abs(tau)} % sur la période.",
        f"{serie.capitalize()} a {sens} de {abs(tau)} {unite_y} au total sur la période.",
    ]
    random.shuffle(options)

    enonce = f"""
> Le taux d'accroissement moyen de {serie} vaut **{tau}** sur une période donnée,
> le temps étant mesuré en {unite_x} et la grandeur en {unite_y}.
>
> Quelle est la bonne interprétation ?
"""

    etapes = [
        Etape(
            "Identifier — un taux répond à une question précise",
            "« De combien la grandeur varie-t-elle, en moyenne, quand le temps avance "
            "d'une unité ? » Ni un niveau, ni un total, ni un pourcentage : une "
            "**variation par unité de temps**.",
        ),
        Etape(
            "Vérifier l'unité avant tout",
            f"Le taux vaut ${tau}$ en **{unite_y} par {unite_x[:-1]}**. "
            "Toute interprétation qui ne fait pas apparaître les deux unités est "
            "incomplète ; celles qui parlent de pourcentage changent carrément de "
            "grandeur.",
        ),
        Etape(
            "Vérifier — le total n'est pas le taux",
            f"Sur une période de $n$ {unite_x}, la variation **totale** vaut "
            f"${tau} \\times n$, et non ${tau}$. Confondre le taux et la variation "
            "totale revient à oublier la division par la durée — l'erreur la plus "
            "fréquente de la séance.",
        ),
        Etape(
            "Interpréter — pourquoi « en moyenne »",
            "Le taux d'accroissement lisse tout ce qui s'est passé entre les deux "
            "dates. Deux trajectoires très différentes — une baisse brutale suivie "
            "d'un rebond, ou une décroissance régulière — peuvent donner exactement "
            "le même taux moyen. C'est utile et insuffisant à la fois.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation correcte",
        indice="Quelles sont les unités du taux ? L'interprétation doit les contenir "
        "toutes les deux.",
        pieges=[
            (f"{serie.capitalize()} valait {abs(tau)} {unite_y} en moyenne sur la période.",
             "Vous décrivez un **niveau moyen**. Le taux décrit une **variation**, "
             "ce qui est tout autre chose."),
            (f"{serie.capitalize()} a {sens} de {abs(tau)} % sur la période.",
             f"Le taux est exprimé en {unite_y} par {unite_x[:-1]}, pas en pourcentage. "
             "Un pourcentage rapporterait la variation à la valeur initiale, pas à "
             "la durée."),
            (f"{serie.capitalize()} a {sens} de {abs(tau)} {unite_y} au total sur la période.",
             "Vous confondez le taux avec la variation **totale**. Le taux est une "
             "variation **par unité de temps** : le total vaut le taux multiplié par "
             "la durée."),
        ],
    )


# --- 3. Taux d'accroissement d'une fonction --------------------------------


def gen_taux_fonction() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-4, -2, 0, 3, 5])
    x0 = random.choice([1, 2, 3, 4])
    x1 = x0 + random.choice([1, 2, 3])
    f = a * x**2 + b * x
    fa, fb = f.subs(x, x0), f.subs(x, x1)
    reponse = float((fb - fa) / (x1 - x0))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez le taux d'accroissement moyen de $f$ **entre ${x0}$ et ${x1}$**.
"""

    etapes = [
        Etape(
            "Identifier — la formule est la même, la fonction remplace le tableau",
            "Rien de nouveau par rapport à l'exercice sur données : on calcule les "
            "deux images, on fait la différence, on divise par l'écart des abscisses.",
            r"\tau = \frac{f(b) - f(a)}{b - a}",
        ),
        Etape(
            "Calculer les deux images",
            f"$f({x0}) = {a}({x0})^2 + ({b})({x0}) = {fa}$ et "
            f"$f({x1}) = {a}({x1})^2 + ({b})({x1}) = {fb}$.",
            rf"f({x0}) = {fa} \qquad f({x1}) = {fb}",
        ),
        Etape(
            "Former le rapport",
            "",
            rf"\tau = \frac{{{fb} - ({fa})}}{{{x1} - {x0}}} "
            rf"= \frac{{{fb - fa}}}{{{x1 - x0}}} = {reponse:.2f}",
        ),
        Etape(
            "Vérifier — comparer à un autre intervalle",
            f"Entre ${x0}$ et ${x0 + 1}$, le taux vaut "
            f"${float(f.subs(x, x0+1) - fa):.2f}$. Il **diffère** du taux précédent : "
            "contrairement à une droite, une parabole n'a pas la même pente partout. "
            "C'est précisément ce qui rend la notion de taux **local** nécessaire.",
        ),
        Etape(
            "Interpréter — la pente de la sécante",
            f"Le nombre ${reponse:.2f}$ est la pente de la droite qui joint les points "
            f"$({x0}\\,;\\,{fa})$ et $({x1}\\,;\\,{fb})$ de la courbe : la **sécante**. "
            "En rapprochant le second point du premier, cette sécante pivotera vers "
            "la tangente — et sa pente deviendra la dérivée.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux d'accroissement",
        tolerance=0.005,
        indice="Calculez les deux images d'abord, le rapport ensuite.",
        pieges=[
            (float(fb - fa),
             "C'est la variation de $f$, pas le taux : il reste à diviser par "
             f"${x1} - {x0} = {x1 - x0}$."),
            (float((fb + fa) / (x1 - x0)),
             "Vous avez **additionné** les deux images. Un taux d'accroissement "
             "repose sur leur différence."),
        ],
    )


# --- 4. Taux avec un pas h et passage à la limite --------------------------


def gen_taux_avec_h() -> Exercice:
    a = random.choice([1, 2, 3])
    x0 = random.choice([1, 2, 3, 4, 5])
    pas = random.choice([1, 0.5, 0.1, 0.01])
    # f(x) = a x^2 ; tau(h) = a(2 x0 + h)
    reponse = a * (2 * x0 + pas)

    enonce = f"""
> Soit $f(x) = {a}x^2$. On s'intéresse au taux d'accroissement de $f$ entre
> ${x0}$ et ${x0} + h$ :
>
> $$ \\tau(h) = \\frac{{f({x0}+h) - f({x0})}}{{h}} $$
>
> Calculez $\\tau(h)$ pour **$h = {pas}$**.
"""

    tau_exact = a * (2 * x0 + pas)

    etapes = [
        Etape(
            "Identifier — deux chemins possibles",
            "On peut substituer $h$ dès le départ et calculer numériquement, ou "
            "simplifier d'abord l'expression littérale. Le second chemin est plus "
            "long une fois, mais il donne bien davantage.",
        ),
        Etape(
            "Développer $f(x_0 + h)$",
            f"$f({x0}+h) = {a}({x0}+h)^2 = {a}({x0**2} + {2*x0}h + h^2)$. "
            "C'est ici que l'identité remarquable de la pré-rentrée sert : sans elle, "
            "le calcul s'arrête.",
            rf"f({x0}+h) = {a*x0**2} + {2*a*x0}h + {a}h^2",
        ),
        Etape(
            "Former le rapport et simplifier",
            f"La différence fait disparaître le terme constant ${a*x0**2}$, et tous "
            "les termes restants contiennent $h$ : on peut donc simplifier par $h$, "
            "à condition que $h \\neq 0$.",
            rf"\tau(h) = \frac{{{2*a*x0}h + {a}h^2}}{{h}} = {2*a*x0} + {a}h",
        ),
        Etape(
            "Substituer",
            f"Pour $h = {pas}$ :",
            rf"\tau({pas}) = {2*a*x0} + {a} \times {pas} = {tau_exact:.4g}",
        ),
        Etape(
            "Interpréter — ce que devient $\\tau$ quand $h$ diminue",
            f"L'expression $\\tau(h) = {2*a*x0} + {a}h$ est limpide : quand $h$ devient "
            f"très petit, le terme ${a}h$ s'efface et le taux s'approche de "
            f"**${2*a*x0}$**. Ce nombre — la pente de la tangente en $x = {x0}$ — est "
            f"la dérivée de $f$ en ${x0}$. Vous venez de la calculer sans la nommer.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"τ({pas}) =",
        tolerance=0.0005,
        indice="Développez $({x0}+h)^2$ avec l'identité remarquable, puis simplifiez "
        "par $h$ avant de remplacer.",
        pieges=[
            (float(2 * a * x0),
             f"Vous avez donné la **limite** quand $h$ tend vers 0, pas la valeur "
             f"pour $h = {pas}$. Il reste le terme ${a}h$."),
            (float(a * (x0 + pas) ** 2 - a * x0**2),
             "Vous avez calculé la variation de $f$ sans diviser par $h$."),
        ],
    )


# --- 5. Vers la dérivée : la limite ----------------------------------------


def gen_limite() -> Exercice:
    a = random.choice([1, 2, 3, 4])
    b = random.choice([-6, -3, 0, 2, 5])
    x0 = random.choice([1, 2, 3, 4, 5])
    reponse = float(2 * a * x0 + b)

    enonce = f"""
> Soit $f(x) = {sp.latex(a*x**2 + b*x)}$. On montre que son taux d'accroissement entre
> ${x0}$ et ${x0}+h$ s'écrit
>
> $$ \\tau(h) = {2*a*x0 + b} + {a}h $$
>
> Vers quelle valeur $\\tau(h)$ **tend-il** lorsque $h$ devient de plus en plus
> proche de $0$ ?
"""

    etapes = [
        Etape(
            "Identifier — faire tendre, ce n'est pas remplacer",
            "On ne peut pas poser $h = 0$ dans le rapport de départ : le dénominateur "
            "s'annulerait. Mais **après simplification**, l'expression obtenue est "
            "parfaitement définie en $0$, et c'est vers cette valeur que le taux tend.",
        ),
        Etape(
            "Observer terme par terme",
            f"Le terme ${2*a*x0 + b}$ ne dépend pas de $h$ : il ne bouge pas. "
            f"Le terme ${a}h$ devient aussi petit qu'on veut lorsque $h$ approche "
            "de $0$.",
            rf"\tau(0.1) = {2*a*x0 + b + a*0.1:.4g} \quad "
            rf"\tau(0.01) = {2*a*x0 + b + a*0.01:.4g} \quad "
            rf"\tau(0.001) = {2*a*x0 + b + a*0.001:.5g}",
        ),
        Etape(
            "Conclure",
            "",
            rf"\lim_{{h \to 0}} \tau(h) = {2*a*x0 + b}",
        ),
        Etape(
            "Vérifier — le résultat a-t-il un sens géométrique ?",
            f"Quand $h$ diminue, le second point glisse vers le premier et la sécante "
            f"pivote. Sa position limite est la **tangente** à la courbe au point "
            f"d'abscisse ${x0}$, dont la pente vaut ${reponse:.0f}$.",
        ),
        Etape(
            "Interpréter — ce nombre porte un nom",
            f"Ce ${reponse:.0f}$ est le **nombre dérivé** de $f$ en ${x0}$, noté "
            f"$f'({x0})$. Il se lit : « au voisinage immédiat de ${x0}$, $f$ varie de "
            f"{reponse:.0f} unité(s) par unité de $x$ ». Toute la séance 3 consistera "
            "à calculer ce nombre sans repasser par la limite à chaque fois.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Limite du taux",
        tolerance=1e-6,
        indice="Que devient chacun des deux termes quand $h$ s'approche de 0 ?",
        pieges=[
            (float(2 * a * x0 + b + a),
             "Vous avez posé $h = 1$ et non $h \\to 0$. Le terme en $h$ doit "
             "disparaître."),
            (float(a),
             "Vous avez donné le coefficient de $h$, c'est-à-dire précisément le terme "
             "qui **s'efface** à la limite."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Taux sur données",
        "2️⃣ Interpréter un taux",
        "3️⃣ Taux d'une fonction",
        "4️⃣ Le pas h",
        "5️⃣ Vers la dérivée",
    ]
)

with onglets[0]:
    st.subheader("Taux d'accroissement entre deux dates")
    executer("s2_taux_moyen", gen_taux_moyen)

with onglets[1]:
    st.subheader("Que dit exactement un taux ?")
    executer("s2_interpretation", gen_interpretation)

with onglets[2]:
    st.subheader("Taux d'accroissement d'une fonction")
    executer("s2_fonction", gen_taux_fonction)

with onglets[3]:
    st.subheader("Écrire le taux avec un pas h")
    executer("s2_pas_h", gen_taux_avec_h)

with onglets[4]:
    st.subheader("Quand h tend vers zéro")
    executer("s2_limite", gen_limite)

st.markdown("---")
st.caption(
    "Semestre — séance n°2 : Taux d'accroissement et sécante · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
