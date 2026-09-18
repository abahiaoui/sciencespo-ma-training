"""Série S6 — Convexité, concavité et point d'inflexion."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S6 | Convexité", page_icon="🥣", layout="wide")

x = sp.Symbol("x")

st.title("🥣 S6 — Convexité et point d'inflexion")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **dérivée seconde**, en lire le signe, distinguer convexité et
concavité, et repérer un **point d'inflexion**.

### 🧠 Ce que la dérivée seconde ajoute
$f'$ dit si la fonction monte ou descend. $f''$ dit si elle monte **de plus en plus
vite** ou **de moins en moins vite**. C'est une distinction décisive : une dépense qui
augmente et une dépense dont la hausse ralentit décrivent deux situations politiques
très différentes, alors que $f'$ seule ne les sépare pas.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 6")
    st.latex(r"f'' > 0 \;\Rightarrow\; f \text{ convexe}")
    st.latex(r"f'' < 0 \;\Rightarrow\; f \text{ concave}")
    st.markdown(
        "**Convexe** : courbe « en bol », tangentes en dessous, "
        "croissance qui **accélère**\n\n"
        "**Concave** : courbe « en dôme », tangentes au-dessus, "
        "croissance qui **ralentit**"
    )
    st.markdown("**Point d'inflexion**")
    st.markdown("$f''$ s'annule **et change de signe** : la courbure s'inverse.")
    st.error(
        "**À ne pas confondre**\n\n"
        "$f' < 0$ : la fonction **diminue**.\n\n"
        "$f'' < 0$ : la fonction **ralentit** — elle peut très bien "
        "continuer d'augmenter."
    )

CONTEXTES = [
    ("la dépense publique du secteur", "années", "M€"),
    ("le nombre de dossiers en stock", "semaines", "dossiers"),
    ("la consommation d'un service", "mois", "unités"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Dérivée seconde -----------------------------------------------------


def gen_derivee_seconde() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-6, -3, 2, 5])
    c = random.choice([-8, 4, 9])
    d = random.choice([-5, 0, 7])
    f = a * x**3 + b * x**2 + c * x + d
    fp = sp.expand(sp.diff(f, x))
    reponse = sp.expand(sp.diff(f, x, 2))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez la **dérivée seconde** $f''(x)$.
"""

    etapes = [
        Etape(
            "Identifier — dériver deux fois, pas dériver au carré",
            "$f''$ s'obtient en dérivant $f'$, exactement comme $f'$ s'obtient en "
            "dérivant $f$. Il n'y a aucune règle nouvelle : c'est la même opération, "
            "appliquée une seconde fois.",
        ),
        Etape(
            "Calculer la dérivée première",
            "",
            rf"f'(x) = {sp.latex(fp)}",
        ),
        Etape(
            "Dériver à nouveau",
            "Le terme constant de $f'$ disparaît à son tour.",
            rf"f''(x) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — deux degrés perdus",
            f"$f$ est de degré ${sp.degree(f, x)}$, $f'$ de degré "
            f"${sp.degree(fp, x)}$, et $f''$ de degré "
            f"${sp.degree(reponse, x) if reponse.free_symbols else 0}$. ✓ "
            "Chaque dérivation abaisse le degré d'une unité.",
        ),
        Etape(
            "Interpréter",
            "$f''$ mesure la variation de la pente. Là où elle est positive, la pente "
            "augmente : la fonction accélère. Là où elle est négative, la pente "
            "diminue : la fonction ralentit, même si elle continue de croître.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="f''(x) =",
        symboles=["x"],
        indice="Dérivez une première fois, puis dérivez le résultat.",
        pieges=[
            (fp,
             "Vous vous êtes arrêté à la dérivée **première**. Il faut dériver une "
             "seconde fois."),
            (sp.expand(fp**2),
             "$f''$ n'est pas le carré de $f'$ : c'est la dérivée de $f'$."),
        ],
    )


def _pieges_inflexion(f):
    """Points critiques réels de f : réponses typiques d'un étudiant qui a annulé f'."""
    pieges = []
    for racine in sp.solve(sp.diff(f, x), x):
        if racine.is_real:
            pieges.append(
                (float(racine),
                 "Vous avez annulé la dérivée **première**, ce qui donne un point "
                 "critique — un maximum ou un minimum — et non un point d'inflexion.")
            )
    return pieges


# --- 2. Point d'inflexion ---------------------------------------------------


def gen_inflexion() -> Exercice:
    a = random.choice([1, 2, -1, -2])
    sol = random.choice([-3, -1, 1, 2, 4])
    b = -3 * a * sol  # f'' = 6a x + 2b s'annule en -b/(3a) = sol
    c = random.choice([-6, 2, 8])
    d = random.choice([-4, 0, 5])
    f = a * x**3 + b * x**2 + c * x + d
    fpp = sp.expand(sp.diff(f, x, 2))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> En quelle valeur de $x$ la courbe admet-elle un **point d'inflexion** ?
"""

    etapes = [
        Etape(
            "Identifier — un point d'inflexion est un changement de courbure",
            "Ce n'est pas un extremum. La fonction peut y être croissante, "
            "décroissante ou stationnaire ; ce qui change, c'est le **sens de la "
            "courbure** — donc le signe de $f''$.",
        ),
        Etape(
            "Calculer la dérivée seconde",
            "",
            rf"f''(x) = {sp.latex(fpp)}",
        ),
        Etape(
            "Annuler la dérivée seconde",
            "",
            rf"{sp.latex(fpp)} = 0 \iff x = {sol}",
        ),
        Etape(
            "Vérifier — le signe change-t-il vraiment ?",
            f"$f''({sol - 1}) = {float(fpp.subs(x, sol-1)):.0f}$ et "
            f"$f''({sol + 1}) = {float(fpp.subs(x, sol+1)):.0f}$ : les deux signes "
            "sont opposés. ✓ C'est cette condition qui fait le point d'inflexion — "
            "s'annuler ne suffit pas, ici comme pour les extrema.",
        ),
        Etape(
            "Interpréter — le point de retournement d'une tendance",
            f"Avant ${sol}$, la courbe est "
            f"{'concave' if float(fpp.subs(x, sol-1)) < 0 else 'convexe'} ; après, "
            f"elle est {'convexe' if float(fpp.subs(x, sol-1)) < 0 else 'concave'}. "
            "Dans un suivi épidémique ou budgétaire, c'est le moment où « ça "
            "commence à ralentir » — souvent bien avant que la courbe elle-même "
            "redescende.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="Point d'inflexion x =",
        tolerance=1e-6,
        indice="Cherchez où la dérivée **seconde** s'annule.",
        pieges=_pieges_inflexion(f),
    )


# --- 3. Convexe ou concave (QCM) --------------------------------------------


def gen_convexite() -> Exercice:
    a = random.choice([1, 2, -1, -2])
    sol = random.choice([-2, 0, 2, 3])
    b = -3 * a * sol
    c = random.choice([-5, 3])
    f = a * x**3 + b * x**2 + c * x
    fpp = sp.expand(sp.diff(f, x, 2))

    cote = random.choice(["gauche", "droite"])
    x_test = sol - 2 if cote == "gauche" else sol + 2
    signe = float(fpp.subs(x, x_test))
    convexe = signe > 0

    borne_g = f"-\\infty" if cote == "gauche" else str(sol)
    borne_d = str(sol) if cote == "gauche" else "+\\infty"

    bonne = "f est convexe sur cet intervalle" if convexe else \
        "f est concave sur cet intervalle"
    options = [
        "f est convexe sur cet intervalle",
        "f est concave sur cet intervalle",
        "f est croissante sur cet intervalle",
        "f est décroissante sur cet intervalle",
    ]

    enonce = f"""
> Soit $f(x) = {sp.latex(f)}$, dont la dérivée seconde est
> $f''(x) = {sp.latex(fpp)}$.
>
> Que peut-on dire de $f$ sur l'intervalle $]{borne_g}\\,;\\,{borne_d}[$ ?
"""

    etapes = [
        Etape(
            "Identifier — la question porte sur la courbure",
            "Le signe de $f''$ renseigne sur la **forme** de la courbe, pas sur son "
            "sens de variation. Croissance et convexité sont deux propriétés "
            "indépendantes : une fonction peut être décroissante et convexe.",
        ),
        Etape(
            "Tester le signe de $f''$",
            f"Prenons $x = {x_test}$ :",
            rf"f''({x_test}) = {signe:.0f} \quad "
            rf"({'positif' if convexe else 'négatif'})",
        ),
        Etape(
            "Vérifier — le signe est-il constant sur l'intervalle ?",
            f"$f''$ est affine et ne s'annule qu'en ${sol}$, qui est une borne de "
            "l'intervalle. Le signe est donc bien constant sur tout l'intérieur. ✓",
        ),
        Etape(
            "Interpréter",
            f"$f''$ étant {'positive' if convexe else 'négative'}, $f$ est "
            f"**{'convexe' if convexe else 'concave'}** : la courbe est tournée vers "
            f"le {'haut' if convexe else 'bas'}, ses tangentes passent "
            f"{'en dessous' if convexe else 'au-dessus'} d'elle, et sa pente "
            f"{'augmente' if convexe else 'diminue'} continûment. "
            "Rien de tout cela ne dit si la fonction monte ou descend.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Conclusion",
        indice="La dérivée seconde parle de courbure, pas de sens de variation.",
        pieges=[
            ("f est croissante sur cet intervalle",
             "Le sens de variation se lit sur $f'$, pas sur $f''$. Ici l'énoncé ne "
             "fournit que la dérivée seconde."),
            ("f est décroissante sur cet intervalle",
             "Le sens de variation se lit sur $f'$, pas sur $f''$."),
            ("f est concave sur cet intervalle" if convexe
             else "f est convexe sur cet intervalle",
             f"Vérifiez le signe : $f''({x_test}) = {signe:.0f}$, donc "
             f"{'positif' if convexe else 'négatif'}."),
        ],
    )


# --- 4. Lire un ralentissement (QCM) ----------------------------------------


def gen_ralentissement() -> Exercice:
    grandeur, unite_x, unite_y = random.choice(CONTEXTES)
    t0 = random.choice([3, 4, 5, 6])

    bonne = (
        f"{grandeur.capitalize()} continue d'augmenter, mais de moins en moins vite."
    )
    options = [
        bonne,
        f"{grandeur.capitalize()} diminue à partir de {t0}.",
        f"{grandeur.capitalize()} est maximale en {t0}.",
        f"{grandeur.capitalize()} augmente de plus en plus vite.",
    ]
    random.shuffle(options)

    enonce = f"""
> On suit {grandeur} au cours du temps, $t$ étant mesuré en {unite_x}. On a établi
> qu'au voisinage de $t = {t0}$ :
>
> $$ f'({t0}) > 0 \\qquad \\text{{et}} \\qquad f''({t0}) < 0 $$
>
> Quelle est la bonne interprétation ?
"""

    etapes = [
        Etape(
            "Identifier — lire les deux informations séparément",
            "$f' > 0$ porte sur le **sens** : la grandeur augmente. "
            "$f'' < 0$ porte sur le **rythme** : la pente diminue. "
            "Les deux sont parfaitement compatibles.",
        ),
        Etape(
            "Combiner",
            f"La grandeur augmente (car $f' > 0$), mais chaque {unite_x[:-1]} "
            "supplémentaire apporte moins que le précédent (car $f''$ < 0). "
            "C'est un ralentissement, pas un recul.",
        ),
        Etape(
            "Vérifier — ce qu'il faudrait pour une baisse",
            f"Pour que {grandeur} **diminue**, il faudrait $f' < 0$. "
            "Tant que $f'$ reste positive, la grandeur continue de croître, quel que "
            "soit le signe de $f''$.",
        ),
        Etape(
            "Interpréter — pourquoi la distinction est politique",
            "« La hausse ralentit » et « la dépense baisse » sont deux affirmations "
            "très différentes, et leur confusion est fréquente dans le débat public. "
            "Un ralentissement de la croissance d'une dépense laisse cette dépense "
            "à un niveau plus élevé chaque année.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation",
        indice="$f'$ donne le sens, $f''$ donne le rythme. Que dit chacune ?",
        pieges=[
            (f"{grandeur.capitalize()} diminue à partir de {t0}.",
             "Vous avez lu $f'' < 0$ comme une baisse. C'est $f'$ qui donne le sens, "
             "et elle est **positive** : la grandeur augmente encore."),
            (f"{grandeur.capitalize()} est maximale en {t0}.",
             f"Un maximum exigerait $f'({t0}) = 0$. Ici $f'$ est strictement "
             "positive."),
            (f"{grandeur.capitalize()} augmente de plus en plus vite.",
             "Cela correspondrait à $f'' > 0$. Ici la dérivée seconde est négative : "
             "la croissance ralentit."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dérivée seconde",
        "2️⃣ Point d'inflexion",
        "3️⃣ Convexe ou concave ?",
        "4️⃣ Lire un ralentissement",
    ]
)

with onglets[0]:
    st.subheader("Dériver deux fois")
    executer("s6_seconde", gen_derivee_seconde)

with onglets[1]:
    st.subheader("Où la courbure s'inverse-t-elle ?")
    executer("s6_inflexion", gen_inflexion)

with onglets[2]:
    st.subheader("Lire la courbure")
    executer("s6_convexite", gen_convexite)

with onglets[3]:
    st.subheader("Ralentir n'est pas baisser")
    executer("s6_ralentissement", gen_ralentissement)

st.markdown("---")
st.caption(
    "Semestre — séance n°6 : Convexité et point d'inflexion · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
