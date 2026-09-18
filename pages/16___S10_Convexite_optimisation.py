"""Série S10 — Dérivée seconde, convexité et optimisation. Fil rouge G (clôture)."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S10 | Convexité et optimisation", page_icon="🥣",
                   layout="wide")

x, q = sp.symbols("x q")

st.title("🥣 S10 — Dérivée seconde, convexité et optimisation")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **dérivée seconde**, lire la **convexité**, et appliquer les
**conditions du premier et du second ordre** pour conclure proprement un problème
d'optimisation.

### 🧠 Ce que la dérivée seconde ajoute
$f'$ dit si la fonction monte ou descend. $f''$ dit si elle monte **de plus en plus
vite** ou **de moins en moins vite**. La distinction est décisive : une dépense qui
augmente et une dépense dont la hausse ralentit décrivent deux situations politiques
très différentes, que $f'$ seule ne sépare pas.

### 🔧 Fil rouge G — L'atelier municipal (clôture)
$\\pi(q) = -0{,}02\\,q^2 + 65q - 40\\,000$, donc
$\\pi'(q) = -0{,}04q + 65$ et $\\pi''(q) = -0{,}04 < 0$.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 10")
    st.latex(r"f'' > 0 \;\Rightarrow\; f \text{ convexe}")
    st.latex(r"f'' < 0 \;\Rightarrow\; f \text{ concave}")
    st.markdown(
        "**Convexe** : courbe « en bol », pente qui **augmente**\n\n"
        "**Concave** : courbe « en dôme », pente qui **diminue**"
    )
    st.markdown("**Conditions d'optimalité**")
    st.latex(r"f'(a) = 0 \quad \text{(premier ordre)}")
    st.latex(r"f''(a) < 0 \Rightarrow \text{maximum} \qquad "
             r"f''(a) > 0 \Rightarrow \text{minimum}")
    st.error(
        "**À ne pas confondre**\n\n"
        "$f' < 0$ : la fonction **diminue**.\n\n"
        "$f'' < 0$ : la fonction **ralentit** — elle peut très bien continuer "
        "d'augmenter."
    )

CONTEXTES = [
    ("la dépense publique du secteur", "années", "M€"),
    ("le nombre de dossiers en stock", "semaines", "dossiers"),
    ("la fréquentation de l'équipement", "mois", "visites"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Dérivée seconde -----------------------------------------------------


def gen_seconde() -> Exercice:
    a = random.choice([1, 2, 3, -2])
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
            "Identifier — dériver deux fois, pas élever au carré",
            "$f''$ s'obtient en dérivant $f'$, exactement comme $f'$ s'obtient en "
            "dérivant $f$. Aucune règle nouvelle : la même opération, appliquée une "
            "seconde fois.",
        ),
        Etape("Calculer la dérivée première", "", rf"f'(x) = {sp.latex(fp)}"),
        Etape(
            "Dériver à nouveau",
            "Le terme constant de $f'$ disparaît à son tour.",
            rf"f''(x) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — deux degrés perdus",
            f"$f$ est de degré ${sp.degree(f, x)}$, $f'$ de degré "
            f"${sp.degree(fp, x)}$, $f''$ de degré "
            f"${sp.degree(reponse, x) if reponse.free_symbols else 0}$. ✓",
        ),
        Etape(
            "Interpréter",
            "$f''$ mesure la variation de la **pente**. Positive, la pente augmente : "
            "la fonction accélère. Négative, la pente diminue : la fonction ralentit, "
            "même si elle continue de croître.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="f''(x) =",
        symboles=["x"],
        indice="Dérivez une fois, puis dérivez le résultat.",
        pieges=[
            (fp, "Vous vous êtes arrêté à la dérivée **première**."),
            (sp.expand(fp**2),
             "$f''$ n'est pas le carré de $f'$ : c'est la dérivée de $f'$."),
        ],
    )


# --- 2. Convexe ou concave (QCM) -------------------------------------------


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

    borne_g = "-\\infty" if cote == "gauche" else str(sol)
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
            "sens de variation. Croissance et convexité sont indépendantes : une "
            "fonction peut parfaitement être décroissante et convexe.",
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
            "l'intervalle. Le signe est donc constant sur tout l'intérieur. ✓",
        ),
        Etape(
            "Interpréter",
            f"$f''$ étant {'positive' if convexe else 'négative'}, $f$ est "
            f"**{'convexe' if convexe else 'concave'}** : courbe tournée vers le "
            f"{'haut' if convexe else 'bas'}, pente qui "
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
             "Le sens de variation se lit sur $f'$, pas sur $f''$."),
            ("f est décroissante sur cet intervalle",
             "Le sens de variation se lit sur $f'$, pas sur $f''$."),
            ("f est concave sur cet intervalle" if convexe
             else "f est convexe sur cet intervalle",
             f"Vérifiez le signe : $f''({x_test}) = {signe:.0f}$."),
        ],
    )


# --- 3. Conditions du premier et du second ordre (QCM) ---------------------


def gen_conditions() -> Exercice:
    a = random.choice([-3, -2, -1, 1, 2, 3])
    q0 = random.choice([5, 10, 20, 500])
    seconde = 2 * a

    bonne = (
        f"C'est un maximum : la condition du premier ordre est vérifiée et "
        f"f''({q0}) < 0"
        if seconde < 0 else
        f"C'est un minimum : la condition du premier ordre est vérifiée et "
        f"f''({q0}) > 0"
    )
    options = [
        f"C'est un maximum : la condition du premier ordre est vérifiée et "
        f"f''({q0}) < 0",
        f"C'est un minimum : la condition du premier ordre est vérifiée et "
        f"f''({q0}) > 0",
        f"On ne peut pas conclure : f'({q0}) = 0 ne suffit jamais",
        "C'est un point d'inflexion",
    ]

    enonce = f"""
> Une fonction objectif $f$ vérifie
>
> $$ f'({q0}) = 0 \\qquad \\text{{et}} \\qquad f''(q) = {seconde}
>    \\ \\text{{pour tout }} q $$
>
> Que peut-on conclure au point $q = {q0}$ ?
"""

    etapes = [
        Etape(
            "Identifier — deux conditions, deux rôles",
            "La condition du **premier ordre** ($f' = 0$) **localise** le point "
            "critique. La condition du **second ordre** (signe de $f''$) en "
            "**détermine la nature**. La première seule ne permet jamais de conclure.",
        ),
        Etape(
            "Lire le signe de la dérivée seconde",
            f"$f''(q) = {seconde}$, constante et "
            f"**{'négative' if seconde < 0 else 'positive'}** : la fonction est "
            f"{'concave' if seconde < 0 else 'convexe'} sur tout son domaine.",
        ),
        Etape(
            "Vérifier — le caractère global",
            f"Comme $f''$ garde le même signe **partout**, l'extremum n'est pas "
            "seulement local : c'est un extremum **global**. Cette information forte "
            "n'est accessible que par le second ordre.",
        ),
        Etape(
            "Interpréter — pourquoi on ne peut pas s'en dispenser",
            "Sans cette vérification, on ne distingue pas un maximum d'un minimum — "
            "ni d'un point d'inflexion à tangente horizontale, comme $x^3$ en 0. "
            "En décision publique, confondre un coût minimal avec un coût maximal "
            "n'est pas une nuance de rédaction.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Conclusion",
        indice="Quel est le signe de la dérivée seconde ?",
        pieges=[
            (f"On ne peut pas conclure : f'({q0}) = 0 ne suffit jamais",
             "Il est vrai que $f' = 0$ ne suffit pas — mais ici on dispose **aussi** "
             "du signe de $f''$, qui permet précisément de trancher."),
            ("C'est un point d'inflexion",
             f"Un point d'inflexion suppose que $f''$ **s'annule et change de signe**. "
             f"Ici $f''$ vaut ${seconde}$ partout."),
            (f"C'est un minimum : la condition du premier ordre est vérifiée et "
             f"f''({q0}) > 0" if seconde < 0 else
             f"C'est un maximum : la condition du premier ordre est vérifiée et "
             f"f''({q0}) < 0",
             f"Relisez le signe : $f'' = {seconde}$, donc "
             f"{'négative' if seconde < 0 else 'positive'}."),
        ],
    )


# --- 4. Fil rouge : optimisation complète de l'atelier ---------------------


def gen_atelier_complet() -> Exercice:
    prix = 100
    fixe = random.choice([30_000, 40_000, 50_000])
    lineaire = random.choice([25, 35, 40])
    quad = random.choice([0.01, 0.02, 0.025])
    marge = prix - lineaire
    q_star = marge / (2 * quad)
    reponse = -quad * q_star**2 + marge * q_star - fixe

    enonce = f"""
> **L'atelier municipal (clôture de l'arc).** Le résultat s'écrit
>
> $$ \\pi(q) = -{str(quad).replace('.', ',')}\\,q^2 + {marge}q - {fixe:,} $$
>
> On a établi que $\\pi'(q) = -{2*quad}q + {marge}$ et
> $\\pi''(q) = -{2*quad} < 0$.
>
> Quel est le **montant du résultat maximal**, en euros ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — deux questions distinctes",
            "« Pour quelle quantité ? » et « combien ? » sont deux questions "
            "différentes. La dérivée répond à la première ; il faut ensuite revenir "
            "à $\\pi$ pour répondre à la seconde. C'est l'étape qu'on oublie.",
        ),
        Etape(
            "Condition du premier ordre",
            "",
            rf"\pi'(q) = 0 \iff q = \frac{{{marge}}}{{{2*quad}}} = {q_star:.0f}"
            rf"\ \text{{réparations}}",
        ),
        Etape(
            "Condition du second ordre",
            f"$\\pi''(q) = -{2*quad}$, strictement négative partout : la fonction est "
            "concave, donc le point critique est un **maximum global**. "
            "Sans cette vérification, la réponse serait incomplète.",
        ),
        Etape(
            "Calculer la valeur du maximum",
            "",
            rf"\pi({q_star:.0f}) = -{quad} \times {q_star:.0f}^2 + {marge} \times "
            rf"{q_star:.0f} - {fixe} \approx {reponse:.0f}\ \text{{€}}",
        ),
        Etape(
            "Interpréter",
            f"Le résultat maximal atteint **{reponse:,.0f} €** pour "
            f"{q_star:.0f} réparations"
            + (". L'activité est donc viable à son optimum."
               if reponse > 0 else
               ". Il reste **négatif** : même au mieux, l'atelier ne couvre pas ses "
               "coûts. Optimiser ne garantit pas la rentabilité — cela garantit qu'on "
               "fait au mieux avec les paramètres donnés, ce qui reste une "
               "information utile pour arbitrer entre subventionner et fermer.")
            .replace(",", "\u202f"),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Résultat maximal",
        unite="€",
        tolerance=0.002,
        indice="Trouvez d'abord la quantité optimale, puis revenez à la fonction.",
        pieges=[
            (float(q_star),
             "C'est la **quantité** optimale, pas le montant du résultat. "
             "Il reste à calculer $\\pi$ en ce point."),
            (float(-fixe),
             "C'est le résultat pour $q = 0$, c'est-à-dire les coûts fixes non "
             "couverts, pas le maximum."),
            (float(prix * q_star),
             "C'est le **chiffre d'affaires** au point optimal, pas le résultat : "
             "il reste à retrancher le coût."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dérivée seconde",
        "2️⃣ Convexe ou concave ?",
        "3️⃣ Premier et second ordre",
        "4️⃣ L'atelier : le montant",
    ]
)

with onglets[0]:
    st.subheader("Dériver une deuxième fois")
    executer("s10_seconde", gen_seconde)

with onglets[1]:
    st.subheader("Lire la courbure")
    executer("s10_convexite", gen_convexite)

with onglets[2]:
    st.subheader("Conclure proprement une optimisation")
    executer("s10_conditions", gen_conditions)

with onglets[3]:
    st.subheader("Clôture de l'arc atelier municipal")
    executer("s10_atelier", gen_atelier_complet)

st.markdown("---")
st.caption(
    "Semestre — séance n°10 : Dérivée seconde, convexité et optimisation · "
    "Fil rouge G : l'atelier municipal · Sciences Po."
)
