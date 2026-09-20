"""Série S10 — Dérivée seconde, convexité et optimisation. Fil rouge G (clôture).

Variation sur trois axes (cf. `contextes.py`) : le contexte, la notation et la
**forme** de la donnée — fonction seule (à dériver deux fois), fonction et
dérivée seconde fournies, ou dérivée seconde seule ; polynôme de degré 3 ou 4,
somme comportant une exponentielle.
"""

import random

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S10 | Convexité et optimisation", page_icon="🥣",
                   layout="wide")

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

### ⚠️ Ce qu'on vous donne varie, la méthode non
Parfois la dérivée seconde est fournie, parfois il faut la calculer, parfois elle
est la **seule** donnée disponible. Dans les trois cas, c'est son **signe** qui
répond à la question.
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


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


def _de(mot: str) -> str:
    """« de repas » mais « d'affiches » : élision devant une voyelle."""
    return ("d'" if mot[:1].lower() in "aeiouyéèêh" else 'de ') + mot


NOTATIONS = [
    cx.NotationFonction("f", "x"),
    cx.NotationFonction("g", "x"),
    cx.NotationFonction("h", "t"),
    cx.NotationFonction("C", "q"),
    cx.NotationFonction("D", "t"),
]


# --- 1. Dérivée seconde -----------------------------------------------------


def gen_seconde() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    forme = random.choice(["degre3", "degre4", "exponentielle"])
    b = random.choice([-6, -3, 2, 5])
    c = random.choice([-8, 4, 9])
    d = random.choice([-5, 0, 7])

    if forme == "degre4":
        a = random.choice([1, 2, -1])
        f = a * v**4 + b * v**2 + c * v + d
        controle = (
            f"${notation.nom}$ est de degré $4$, sa dérivée de degré $3$, sa dérivée "
            "seconde de degré $2$. ✓ Chaque dérivation fait perdre exactement un "
            "degré."
        )
    elif forme == "exponentielle":
        a = random.choice([2, 3, 5])
        f = a * sp.exp(v) + b * v**2 + c * v
        controle = (
            f"Le terme ${L(a)}e^{{{var}}}$ traverse les deux dérivations sans "
            "changer : c'est la propriété caractéristique de l'exponentielle, et "
            "elle rend le contrôle immédiat. ✓"
        )
    else:
        a = random.choice([1, 2, 3, -2])
        f = a * v**3 + b * v**2 + c * v + d
        controle = (
            f"${notation.nom}$ est de degré $3$, sa dérivée de degré $2$, sa dérivée "
            "seconde de degré $1$. ✓ Deux degrés perdus au total."
        )

    premiere = sp.expand(sp.diff(f, v))
    reponse = sp.expand(sp.diff(f, v, 2))

    enonce = f"""
> Soit la fonction ${notation.nom}$ définie par
>
> $$ {notation.de()} = {sp.latex(f)} $$
>
> Calculez la **dérivée seconde** ${notation.seconde()}$.
"""

    etapes = [
        Etape(
            "Identifier — dériver deux fois, pas élever au carré",
            f"${notation.seconde()}$ s'obtient en dérivant ${notation.derivee()}$, "
            f"exactement comme ${notation.derivee()}$ s'obtient en dérivant "
            f"${notation.de()}$. Aucune règle nouvelle : la même opération, appliquée "
            "une seconde fois.",
        ),
        Etape(
            "Calculer la dérivée première",
            "",
            rf"{notation.derivee()} = {sp.latex(premiere)}",
        ),
        Etape(
            "Dériver à nouveau",
            "Le terme constant de la dérivée première disparaît à son tour.",
            rf"{notation.seconde()} = {sp.latex(reponse)}",
        ),
        Etape("Vérifier", controle),
        Etape(
            "Interpréter",
            f"${notation.seconde()}$ mesure la variation de la **pente**. Positive, "
            "la pente augmente : la fonction accélère. Négative, la pente diminue : "
            "la fonction ralentit, même si elle continue de croître.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle=f"{notation.nom}''({var}) =",
        symboles=[var],
        indice="Dérivez une fois, puis dérivez le résultat.",
        pieges=[
            (premiere, "Vous vous êtes arrêté à la dérivée **première**."),
            (
                sp.expand(premiere**2),
                f"${notation.seconde()}$ n'est pas le carré de "
                f"${notation.derivee()}$ : c'est sa dérivée.",
            ),
        ],
    )


# --- 2. Convexe ou concave (QCM) -------------------------------------------


def gen_convexite() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    a = random.choice([1, 2, -1, -2])
    inflexion = random.choice([-2, 0, 2, 3])
    b = -3 * a * inflexion
    c = random.choice([-5, 3])
    f = a * v**3 + b * v**2 + c * v
    seconde = sp.expand(sp.diff(f, v, 2))
    presentation = random.choice(["f_et_seconde", "f_seule", "seconde_seule"])

    cote = random.choice(["gauche", "droite"])
    point_test = inflexion - 2 if cote == "gauche" else inflexion + 2
    valeur_test = float(seconde.subs(v, point_test))
    convexe = valeur_test > 0

    borne_g = "-\\infty" if cote == "gauche" else L(inflexion)
    borne_d = L(inflexion) if cote == "gauche" else "+\\infty"

    convexite = f"{notation.nom} est convexe sur cet intervalle"
    concavite = f"{notation.nom} est concave sur cet intervalle"
    croissante = f"{notation.nom} est croissante sur cet intervalle"
    decroissante = f"{notation.nom} est décroissante sur cet intervalle"
    bonne = convexite if convexe else concavite
    options = [convexite, concavite, croissante, decroissante]

    if presentation == "f_et_seconde":
        corps = (
            f"> Soit ${notation.de()} = {sp.latex(f)}$, dont la dérivée seconde est\n"
            f"> ${notation.seconde()} = {sp.latex(seconde)}$."
        )
        premier_pas = "La dérivée seconde est fournie : il ne reste qu'à en lire le signe."
    elif presentation == "f_seule":
        corps = f"> Soit ${notation.de()} = {sp.latex(f)}$."
        premier_pas = (
            f"Rien n'est fourni : il faut dériver deux fois, ce qui donne "
            f"${notation.seconde()} = {sp.latex(seconde)}$."
        )
    else:
        corps = (
            f"> D'une fonction ${notation.nom}$, on sait seulement que sa dérivée "
            f"seconde vaut ${notation.seconde()} = {sp.latex(seconde)}$."
        )
        premier_pas = (
            "La fonction elle-même est inconnue, et cela n'a aucune importance : "
            "la convexité ne dépend que du signe de la dérivée seconde."
        )

    enonce = f"""
{corps}
>
> Que peut-on dire de ${notation.nom}$ sur l'intervalle
> $]{borne_g}\\,;\\,{borne_d}[$ ?
"""

    etapes = [
        Etape(
            "Identifier — la question porte sur la courbure",
            f"{premier_pas} Le signe de ${notation.seconde()}$ renseigne sur la "
            "**forme** de la courbe, pas sur son sens de variation. Croissance et "
            "convexité sont indépendantes : une fonction peut parfaitement être "
            "décroissante et convexe.",
        ),
        Etape(
            "Tester le signe de la dérivée seconde",
            f"Prenons ${var} = {L(point_test)}$, à l'intérieur de l'intervalle :",
            rf"{notation.seconde(str(point_test))} = {L(valeur_test, 0)} \quad "
            rf"({'positif' if convexe else 'négatif'})",
        ),
        Etape(
            "Vérifier — le signe est-il constant sur l'intervalle ?",
            f"${notation.seconde()}$ est affine et ne s'annule qu'en "
            f"${L(inflexion)}$, qui est une **borne** de l'intervalle. Le signe est "
            "donc constant sur tout l'intérieur. ✓",
        ),
        Etape(
            "Interpréter",
            f"La dérivée seconde étant {'positive' if convexe else 'négative'}, "
            f"${notation.nom}$ est **{'convexe' if convexe else 'concave'}** : courbe "
            f"tournée vers le {'haut' if convexe else 'bas'}, pente qui "
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
            (
                croissante,
                f"Le sens de variation se lit sur ${notation.derivee()}$, pas sur "
                f"${notation.seconde()}$.",
            ),
            (
                decroissante,
                f"Le sens de variation se lit sur ${notation.derivee()}$, pas sur "
                f"${notation.seconde()}$.",
            ),
            (
                concavite if convexe else convexite,
                f"Vérifiez le signe : ${notation.seconde(str(point_test))} = "
                f"{L(valeur_test, 0)}$.",
            ),
        ],
    )


# --- 3. Conditions du premier et du second ordre (QCM) ---------------------


def gen_conditions() -> Exercice:
    ctx = cx.tirer(cx.PRODUCTIONS)
    notation = random.choice(NOTATIONS)
    var = notation.var
    a = random.choice([-3, -2, -1, 1, 2, 3])
    point = random.choice([5, 10, 20, 500])
    seconde = 2 * a
    presentation = random.choice(["abstraite", "contextuelle"])

    maximum = (
        f"C'est un maximum : la condition du premier ordre est vérifiée et "
        f"{notation.nom}''({point}) < 0"
    )
    minimum = (
        f"C'est un minimum : la condition du premier ordre est vérifiée et "
        f"{notation.nom}''({point}) > 0"
    )
    indecidable = (
        f"On ne peut pas conclure : {notation.nom}'({point}) = 0 ne suffit jamais"
    )
    inflexion = "C'est un point d'inflexion"
    bonne = maximum if seconde < 0 else minimum
    options = [maximum, minimum, indecidable, inflexion]

    if presentation == "abstraite":
        enonce = f"""
> Une fonction objectif ${notation.nom}$ vérifie
>
> $$ {notation.derivee(str(point))} = 0 \\qquad \\text{{et}} \\qquad
>    {notation.seconde()} = {L(seconde)} \\ \\text{{pour tout }} {var} $$
>
> Que peut-on conclure au point ${var} = {point}$ ?
"""
    else:
        enonce = f"""
> **{_maj(ctx.acteur)}.** Sa fonction objectif ${notation.nom}$, exprimée en fonction
> du nombre {_de(ctx.unite_quantite)} ${var}$, vérifie
>
> $$ {notation.derivee(str(point))} = 0 \\qquad \\text{{et}} \\qquad
>    {notation.seconde()} = {L(seconde)} \\ \\text{{pour tout }} {var} $$
>
> Que peut-on conclure au niveau ${var} = {point}$ {ctx.unite_quantite} ?
"""

    etapes = [
        Etape(
            "Identifier — deux conditions, deux rôles",
            "La condition du **premier ordre** (dérivée nulle) **localise** le point "
            "critique. La condition du **second ordre** (signe de la dérivée seconde) "
            "en **détermine la nature**. La première seule ne permet jamais de "
            "conclure.",
        ),
        Etape(
            "Lire le signe de la dérivée seconde",
            f"${notation.seconde()} = {L(seconde)}$, constante et "
            f"**{'négative' if seconde < 0 else 'positive'}** : la fonction est "
            f"{'concave' if seconde < 0 else 'convexe'} sur tout son domaine.",
        ),
        Etape(
            "Vérifier — le caractère global",
            "Comme la dérivée seconde garde le même signe **partout**, l'extremum "
            "n'est pas seulement local : c'est un extremum **global**. Cette "
            "information forte n'est accessible que par le second ordre.",
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
            (
                indecidable,
                "Il est vrai que la dérivée nulle ne suffit pas — mais ici on dispose "
                "**aussi** du signe de la dérivée seconde, qui permet précisément de "
                "trancher.",
            ),
            (
                inflexion,
                f"Un point d'inflexion suppose que la dérivée seconde **s'annule et "
                f"change de signe**. Ici elle vaut ${L(seconde)}$ partout.",
            ),
            (
                minimum if seconde < 0 else maximum,
                f"Relisez le signe : la dérivée seconde vaut ${L(seconde)}$, donc "
                f"{'négative' if seconde < 0 else 'positive'}.",
            ),
        ],
    )


# --- 4. Fil rouge : optimisation complète ----------------------------------


def gen_atelier_complet() -> Exercice:
    ctx = cx.tirer(cx.PRODUCTIONS)
    var = random.choice(["q", "x"])
    nom = random.choice(["\\pi", "B", "P"])
    prix = random.choice([100, 120, 80])
    fixe = random.choice([30_000, 40_000, 50_000])
    lineaire = random.choice([25, 35, 40])
    quad = random.choice([0.01, 0.02, 0.025])
    marge = prix - lineaire
    q_star = marge / (2 * quad)
    reponse = -quad * q_star**2 + marge * q_star - fixe
    presentation = random.choice(["derivees_fournies", "profit_seul"])

    profit_latex = rf"-{L(quad)}\,{var}^2 + {L(marge)}\,{var} - {L(fixe)}"

    if presentation == "derivees_fournies":
        enonce = f"""
> **{_maj(ctx.acteur)}.** Son résultat s'écrit
>
> $$ {nom}({var}) = {profit_latex} $$
>
> On a établi que ${nom}'({var}) = -{L(2 * quad)}\\,{var} + {L(marge)}$ et
> ${nom}''({var}) = -{L(2 * quad)} < 0$.
>
> Quel est le **montant du résultat maximal**, en euros ?
"""
        premier_pas = (
            "Les deux dérivées sont fournies : l'exercice porte entièrement sur "
            "l'enchaînement des conditions, et sur l'étape finale qu'on oublie."
        )
    else:
        enonce = f"""
> **{_maj(ctx.acteur)}.** Son résultat, en euros, s'écrit
>
> $$ {nom}({var}) = {profit_latex} $$
>
> où ${var}$ est le nombre {_de(ctx.unite_quantite)}.
>
> Quel est le **montant du résultat maximal** ?
"""
        premier_pas = (
            f"Rien n'est fourni : il faut dériver. ${nom}'({var}) = "
            f"-{L(2 * quad)}\\,{var} + {L(marge)}$, puis ${nom}''({var}) = "
            f"-{L(2 * quad)}$, constante et négative."
        )

    etapes = [
        Etape(
            "Identifier — deux questions distinctes",
            f"{premier_pas} « Pour quelle quantité ? » et « combien ? » sont deux "
            "questions différentes. La dérivée répond à la première ; il faut ensuite "
            "revenir à la fonction pour répondre à la seconde. C'est l'étape qu'on "
            "oublie.",
        ),
        Etape(
            "Condition du premier ordre",
            "",
            rf"{nom}'({var}) = 0 \iff {var} = \frac{{{L(marge)}}}{{{L(2 * quad)}}} "
            rf"= {L(q_star, 0)}\ \text{{{ctx.unite_quantite}}}",
        ),
        Etape(
            "Condition du second ordre",
            f"${nom}''({var}) = -{L(2 * quad)}$, strictement négative partout : la "
            "fonction est concave, donc le point critique est un **maximum global**. "
            "Sans cette vérification, la réponse serait incomplète.",
        ),
        Etape(
            "Calculer la valeur du maximum",
            "",
            rf"{nom}({L(q_star, 0)}) = -{L(quad)} \times {L(q_star, 0)}^2 + "
            rf"{L(marge)} \times {L(q_star, 0)} - {L(fixe)} \approx {L(reponse, 0)}"
            rf"\ \text{{€}}",
        ),
        Etape(
            "Interpréter",
            f"Le résultat maximal atteint **{_fr(reponse, 0)} €** pour "
            f"{_fr(q_star, 0)} {ctx.unite_quantite}"
            + (
                ". L'activité est donc viable à son optimum."
                if reponse > 0
                else ". Il reste **négatif** : même au mieux, l'activité ne couvre pas "
                "ses coûts. Optimiser ne garantit pas la rentabilité — cela garantit "
                "qu'on fait au mieux avec les paramètres donnés, ce qui reste une "
                "information utile pour arbitrer entre subventionner et fermer."
            ),
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
            (
                float(q_star),
                f"C'est la **quantité** optimale, en {ctx.unite_quantite}, pas le "
                "montant du résultat. Il reste à calculer la fonction en ce point.",
            ),
            (
                float(-fixe),
                "C'est le résultat pour une production nulle, c'est-à-dire les coûts "
                "fixes non couverts, pas le maximum.",
            ),
            (
                float(prix * q_star),
                "C'est le **chiffre d'affaires** au point optimal, pas le résultat : "
                "il reste à retrancher le coût.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dérivée seconde",
        "2️⃣ Convexe ou concave ?",
        "3️⃣ Premier et second ordre",
        "4️⃣ Le montant de l'optimum",
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
