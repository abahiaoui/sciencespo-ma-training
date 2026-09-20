"""Série S4 — Le second degré : parabole et forme factorisée. Fil rouge E : le festival.

Variation sur trois axes (cf. `contextes.py`) : le contexte (marché ou fonction
abstraite), la notation ($f$ de $x$, $R$ de $p$, $C$ de $q$…) et surtout la
**forme** du trinôme — développée, factorisée, canonique, ou produit de deux
facteurs affines. Reconnaître la même parabole sous ces quatre habits est
exactement l'objectif de la séance.
"""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S4 | Second degré", page_icon="🎪", layout="wide")

st.title("🎪 S4 — Le second degré : parabole et forme factorisée")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Reconnaître une fonction du second degré, lire l'**orientation** de sa parabole,
trouver ses **racines** à partir de la forme factorisée, et localiser son **sommet**.

### 🧠 Pourquoi on quitte l'affine
Une recette n'est pas proportionnelle au prix : augmenter le prix rapporte plus par
billet, mais fait fuir des spectateurs. Le produit de ces deux effets contraires n'est
plus une droite — c'est une parabole, et son sommet est précisément le point qu'on
cherche.

### 🎪 Fil rouge E — Le festival de Villeneuve
Au prix $p$ (en euros), le nombre de spectateurs est $N(p) = 9\\,000 - 60p$.
La recette de billetterie vaut donc $R(p) = p\\,(9\\,000 - 60p)$.

### ⚠️ Quatre habits pour la même parabole
Un trinôme peut arriver développé ($ax^2+bx+c$), factorisé ($a(x-x_1)(x-x_2)$),
sous forme canonique ($a(x-\\alpha)^2+\\beta$) ou comme produit de deux facteurs
affines. Chaque forme rend une information gratuite et en cache une autre :
apprenez à reconnaître laquelle.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 4")
    st.latex(r"f(x) = ax^2 + bx + c \quad (a \neq 0)")
    st.markdown("**Orientation**")
    st.markdown(
        "$a > 0$ : parabole tournée vers le **haut**, sommet = **minimum**\n\n"
        "$a < 0$ : tournée vers le **bas**, sommet = **maximum**"
    )
    st.markdown("**Forme factorisée**")
    st.latex(r"f(x) = a(x - x_1)(x - x_2)")
    st.markdown("Les racines $x_1$ et $x_2$ se lisent directement.")
    st.markdown("**Forme canonique**")
    st.latex(r"f(x) = a(x - \alpha)^2 + \beta")
    st.markdown("Le sommet $(\\alpha\\,;\\,\\beta)$ se lit directement.")
    st.markdown("**Le sommet est au milieu des racines**")
    st.latex(r"x_S = \frac{x_1 + x_2}{2} \qquad x_S = -\frac{b}{2a}")
    st.info(
        "**Un produit de deux facteurs affines est un trinôme**\n\n"
        "$(mx + n)(px + q)$ est bien du second degré : son coefficient dominant "
        "est le **produit** $m \\times p$. C'est lui qui donne l'orientation."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


#: Nom de fonction et variable : la parabole ne s'appelle pas toujours $f(x)$.
NOTATIONS = [
    cx.NotationFonction("f", "x"),
    cx.NotationFonction("g", "x"),
    cx.NotationFonction("h", "t"),
    cx.NotationFonction("R", "p"),
    cx.NotationFonction("B", "q"),
]


def _signe(valeur) -> str:
    """« x - 3 » ou « x + 3 » : évite le disgracieux « x - (-3) »."""
    return f"- {L(valeur)}" if valeur >= 0 else f"+ {L(-valeur)}"


# --- 1. Orientation de la parabole (QCM) -----------------------------------


def gen_orientation() -> Exercice:
    notation = random.choice(NOTATIONS)
    v = sp.Symbol(notation.var)
    forme = random.choice(["developpee", "factorisee", "canonique", "produit"])

    if forme == "produit":
        # Le coefficient dominant est un produit : c'est là que l'erreur se niche.
        m = random.choice([-3, -2, -1, 2, 3])
        n = random.choice([-12, -5, 6, 18])
        pp = random.choice([-2, -1, 2, 4])
        qq = random.choice([-8, 3, 15])
        a = m * pp
        expression = rf"({sp.latex(m * v + n)})\,({sp.latex(pp * v + qq)})"
        lecture = (
            f"La fonction n'est pas écrite sous la forme $a{notation.var}^2 + "
            f"b{notation.var} + c$, mais c'est bien un trinôme : en développant, le "
            f"terme en ${notation.var}^2$ vaut ${m} \\times {pp} = {a}$. Le "
            f"coefficient dominant est le **produit** des deux pentes — inutile de "
            "développer le reste."
        )
    elif forme == "factorisee":
        a = random.choice([-3, -2, -1, 2, 4])
        x1 = random.choice([-6, -3, 1, 4])
        x2 = x1 + random.choice([2, 5, 7])
        expression = (
            rf"{L(a)}\,({notation.var} {_signe(x1)})\,({notation.var} {_signe(x2)})"
        )
        lecture = (
            f"Sous forme factorisée, le coefficient dominant est le facteur placé "
            f"**devant** les parenthèses : ${L(a)}$. Les deux parenthèses, elles, "
            f"contribuent chacune un ${notation.var}$, donc un ${notation.var}^2$ au "
            "total, avec un coefficient 1."
        )
    elif forme == "canonique":
        a = random.choice([-4, -2, -1, 2, 3])
        alpha = random.choice([-5, -2, 1, 3, 6])
        beta = random.choice([-18, -4, 7, 25])
        expression = (
            rf"{L(a)}\,({notation.var} {_signe(alpha)})^2 {'+' if beta >= 0 else '-'} "
            rf"{L(abs(beta))}"
        )
        lecture = (
            f"Sous forme canonique, le coefficient dominant est encore le facteur de "
            f"tête : ${L(a)}$. Le carré est toujours positif ou nul ; c'est le signe "
            f"de ${L(a)}$ qui décide si on ajoute ou si on retranche à ${L(beta)}$."
        )
    else:
        a = random.choice([-3, -2, -1, 2, 4])
        b = random.choice([-12, -5, 6, 18])
        c = random.choice([-8, 0, 15])
        expression = sp.latex(a * v**2 + b * v + c)
        lecture = (
            f"Le coefficient de ${notation.var}^2$ vaut ${L(a)}$. C'est **lui seul** "
            "qui décide de l'orientation : ni $b$ ni $c$ n'y changent quoi que ce "
            "soit. Ils déplacent la parabole, ils ne la retournent pas."
        )

    haut = "Tournée vers le haut : le sommet est un minimum"
    bas = "Tournée vers le bas : le sommet est un maximum"
    depend_c = "L'orientation dépend du signe du terme constant"
    bonne = haut if a > 0 else bas
    options = [haut, bas, depend_c]

    enonce = f"""
> Soit la fonction du second degré
>
> $$ {notation.de()} = {expression} $$
>
> Comment sa parabole est-elle orientée, et que représente son sommet ?
"""

    # Calculé hors f-string : une expression de f-string ne peut pas contenir
    # de contre-oblique avant Python 3.12.
    infini = "$+\\infty$" if a > 0 else "$-\\infty$"

    etapes = [
        Etape(
            "Identifier — retrouver le coefficient dominant",
            lecture,
        ),
        Etape(
            "Appliquer la règle",
            f"${L(a)}$ est **{'positif' if a > 0 else 'négatif'}**, donc la parabole "
            f"est tournée vers le **{'haut' if a > 0 else 'bas'}** et son sommet est "
            f"un **{'minimum' if a > 0 else 'maximum'}**.",
        ),
        Etape(
            "Vérifier — le comportement aux extrêmes",
            f"Pour ${notation.var}$ très grand, le terme en ${notation.var}^2$ écrase "
            f"tous les autres : ${notation.nom}$ part donc vers {infini} des deux "
            "côtés. C'est cohérent avec l'orientation annoncée. ✓",
        ),
        Etape(
            "Interpréter — pourquoi le signe de $a$ est décisif en pratique",
            "Une recette ou un profit a presque toujours $a < 0$ : il existe donc un "
            "**maximum**, et la question « quel prix choisir ? » a une réponse. "
            "Avec $a > 0$, on cherche au contraire un minimum — un coût moyen, par "
            "exemple. Le signe de $a$ dit quel type de question on peut poser.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Orientation",
        indice="Quel est le coefficient du terme en carré, une fois tout développé ?",
        pieges=[
            (
                bas if a > 0 else haut,
                f"Le coefficient dominant vaut ${L(a)}$, donc "
                f"**{'positif' if a > 0 else 'négatif'}** : la parabole est tournée "
                f"vers le {'haut' if a > 0 else 'bas'}."
                + (
                    " Attention, il s'agit du **produit** des deux pentes."
                    if forme == "produit"
                    else ""
                ),
            ),
            (
                depend_c,
                "Le terme constant est l'ordonnée à l'origine : il translate la "
                "parabole verticalement, sans jamais la retourner.",
            ),
        ],
    )


# --- 2. Racines d'un trinôme factorisé -------------------------------------


def gen_racines() -> Exercice:
    notation = random.choice(NOTATIONS)
    v = sp.Symbol(notation.var)
    forme = random.choice(["classique", "affines", "produit_prix"])

    if forme == "classique":
        a = random.choice([-2, -1, 1, 2, 3])
        x1 = random.choice([-6, -3, -1, 2, 4])
        x2 = x1 + random.choice([2, 3, 5, 7])
        expression = (
            rf"{L(a)}\,({notation.var} {_signe(x1)})\,({notation.var} {_signe(x2)})"
        )
        lecture = (
            f"Le facteur ${L(a)}$ ne s'annule jamais : il règle l'ouverture de la "
            "parabole, pas ses racines. Seules les deux parenthèses peuvent "
            "s'annuler."
        )
        detail = (
            rf"{notation.var} {_signe(x1)} = 0 \ \text{{ou}}\ "
            rf"{notation.var} {_signe(x2)} = 0 \iff "
            rf"{notation.var} = {L(x1)} \ \text{{ou}}\ {notation.var} = {L(x2)}"
        )
    elif forme == "affines":
        # Racines rationnelles : les pentes ne valent pas 1, il faut diviser.
        m = random.choice([2, 3, 4])
        pp = random.choice([2, 5])
        x1 = random.choice([-3, -1, 2, 5])
        x2 = x1 + random.choice([3, 6])
        n, qq = -m * x1, -pp * x2
        expression = rf"({sp.latex(m * v + n)})\,({sp.latex(pp * v + qq)})"
        lecture = (
            f"Chaque facteur est affine, mais sa pente n'est pas $1$ : annuler "
            f"${sp.latex(m * v + n)}$ demande une **division** par ${m}$. C'est là "
            "que les erreurs de signe apparaissent."
        )
        detail = (
            rf"{sp.latex(m * v + n)} = 0 \iff {notation.var} = "
            rf"\frac{{{L(-n)}}}{{{m}}} = {L(x1)} \qquad "
            rf"{sp.latex(pp * v + qq)} = 0 \iff {notation.var} = "
            rf"\frac{{{L(-qq)}}}{{{pp}}} = {L(x2)}"
        )
        a = m * pp
    else:
        # Forme « recette » : un facteur est la variable elle-même.
        sensibilite = random.choice([50, 60, 75, 90])
        x2 = random.choice([80, 120, 150, 200])
        base = sensibilite * x2
        x1 = 0
        expression = rf"{notation.var}\,({L(base)} - {sensibilite}\,{notation.var})"
        lecture = (
            "Le premier facteur est la variable elle-même : elle s'annule en $0$. "
            "Le second est affine décroissant. Ce produit est la forme typique d'une "
            "recette : une quantité multipliée par un prix qui décroît."
        )
        detail = (
            rf"{notation.var} = 0 \quad \text{{ou}} \quad "
            rf"{L(base)} - {sensibilite}\,{notation.var} = 0 \iff "
            rf"{notation.var} = \frac{{{L(base)}}}{{{sensibilite}}} = {L(x2)}"
        )
        a = -sensibilite

    reponse = float(max(x1, x2))

    enonce = f"""
> Soit la fonction du second degré donnée sous **forme factorisée** :
>
> $$ {notation.de()} = {expression} $$
>
> Quelle est la **plus grande** de ses deux racines ?
"""

    etapes = [
        Etape(
            "Identifier — surtout ne pas développer",
            "La forme factorisée livre les racines presque sans calcul. Développer "
            "reviendrait à détruire l'information qu'on cherche, pour devoir la "
            f"reconstruire ensuite avec le discriminant. {lecture}",
        ),
        Etape(
            "Appliquer l'équation produit nul",
            "Un produit est nul si l'un des facteurs est nul — règle de la "
            "pré-rentrée 3, appliquée telle quelle.",
            detail,
        ),
        Etape(
            "Vérifier",
            f"En remplaçant ${notation.var}$ par ${L(max(x1, x2))}$, le facteur "
            "correspondant s'annule, donc le produit entier s'annule — quelle que "
            "soit la valeur de l'autre facteur. ✓",
        ),
        Etape(
            "Interpréter — ce que les racines représentent",
            "Les racines sont les points où la courbe **coupe l'axe horizontal**, "
            "c'est-à-dire où la grandeur modélisée s'annule. Pour une recette, ce "
            "sont les prix qui ne rapportent rien : un prix nul, et un prix si élevé "
            f"que plus personne n'achète. Et le sommet est déjà connu : il est au "
            f"milieu, en ${L(Fraction(int(x1 + x2), 2))}$.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Plus grande racine",
        tolerance=1e-6,
        indice="Un produit est nul si l'un de ses facteurs est nul.",
        pieges=[
            (
                float(min(x1, x2)),
                "C'est la **plus petite** racine. L'énoncé demande la plus grande.",
            ),
            (
                float(-max(x1, x2)),
                "Attention au signe : un facteur s'annule pour la valeur qui rend la "
                "parenthèse nulle, pas pour son opposé.",
            ),
            (
                float(a),
                "Vous avez donné un coefficient, pas une racine : les coefficients ne "
                "s'annulent pas.",
            ),
        ],
    )


# --- 3. Le sommet -----------------------------------------------------------


def gen_sommet() -> Exercice:
    notation = random.choice(NOTATIONS)
    v = sp.Symbol(notation.var)
    forme = random.choice(["racines", "coefficients", "canonique", "factorisee"])

    if forme == "racines":
        x1 = random.choice([-8, -4, 0, 2, 6])
        x2 = x1 + random.choice([4, 6, 10])
        reponse = float(Fraction(x1 + x2, 2))
        enonce = f"""
> Une parabole a pour racines ${notation.var}_1 = {L(x1)}$ et
> ${notation.var}_2 = {L(x2)}$.
>
> Quelle est l'**abscisse de son sommet** ?
"""
        etapes = [
            Etape(
                "Identifier — la parabole est symétrique",
                "Une parabole est symétrique par rapport à l'axe vertical qui passe "
                "par son sommet. Les deux racines, situées à la même hauteur (zéro), "
                "sont donc **symétriques** l'une de l'autre par rapport à cet axe.",
            ),
            Etape(
                "Prendre le milieu des racines",
                "L'abscisse du sommet est donc exactement au milieu.",
                rf"{notation.var}_S = \frac{{{L(x1)} + {L(x2)}}}{{2}} = {L(reponse)}",
            ),
            Etape(
                "Vérifier — l'écart aux deux racines",
                f"La distance du sommet à chaque racine vaut ${L(abs(reponse - x1))}$ "
                "des deux côtés. ✓ C'est la définition même de la symétrie.",
            ),
            Etape(
                "Interpréter",
                "Ce raisonnement évite toute formule : dès qu'on connaît les deux "
                "racines, le sommet s'obtient de tête. C'est la méthode la plus "
                "rapide, et elle marche dans tous les cas où la forme factorisée "
                "est disponible.",
            ),
        ]
        pieges = [
            (
                float(x2 - x1),
                "C'est l'**écart** entre les racines, pas leur milieu. Il reste à le "
                "diviser par deux et à l'ajouter à la première racine.",
            ),
            (
                float(x1 * x2),
                "Le sommet est au milieu — donc une moyenne, pas un produit.",
            ),
        ]
    elif forme == "factorisee":
        a = random.choice([-2, -1, 2, 3])
        # Pas de racine nulle ici : « (x - 0) » s'écrirait mal.
        x1 = random.choice([-6, -2, 1, 3])
        x2 = x1 + random.choice([4, 6, 8])
        reponse = float(Fraction(x1 + x2, 2))
        enonce = f"""
> Soit la fonction du second degré
>
> $$ {notation.de()} = {L(a)}\\,({notation.var} {_signe(x1)})\\,({notation.var} {_signe(x2)}) $$
>
> Quelle est l'**abscisse de son sommet** ?
"""
        etapes = [
            Etape(
                "Identifier — la forme factorisée donne d'abord les racines",
                f"Inutile de développer pour appliquer $-\\frac{{b}}{{2a}}$ : les "
                f"racines sont lisibles (${L(x1)}$ et ${L(x2)}$), et le sommet est "
                "à leur milieu par symétrie.",
            ),
            Etape(
                "Prendre le milieu des racines",
                "",
                rf"{notation.var}_S = \frac{{{L(x1)} + {L(x2)}}}{{2}} = {L(reponse)}",
            ),
            Etape(
                "Vérifier — par la forme développée",
                f"En développant, ${notation.nom}({notation.var}) = "
                f"{sp.latex(sp.expand(a * (v - x1) * (v - x2)))}$, donc "
                f"$-\\frac{{b}}{{2a}} = {L(reponse)}$. ✓ Les deux chemins coïncident, "
                "mais le premier est bien plus rapide.",
            ),
            Etape(
                "Interpréter",
                f"Le facteur ${L(a)}$ n'intervient pas dans l'abscisse du sommet : il "
                "change la hauteur du sommet et l'ouverture de la parabole, pas sa "
                "position horizontale.",
            ),
        ]
        pieges = [
            (
                float(x1 + x2),
                "Vous avez oublié de diviser par deux : le sommet est la **moyenne** "
                "des racines.",
            ),
            (float(a), "Vous avez donné le coefficient dominant, pas une abscisse."),
        ]
    elif forme == "canonique":
        a = random.choice([-3, -2, 2, 4])
        alpha = random.choice([-4, -1, 2, 5])
        beta = random.choice([-12, -3, 8, 20])
        reponse = float(alpha)
        enonce = f"""
> Soit la fonction du second degré donnée sous **forme canonique** :
>
> $$ {notation.de()} = {L(a)}\\,({notation.var} {_signe(alpha)})^2 {'+' if beta >= 0 else '-'} {L(abs(beta))} $$
>
> Quelle est l'**abscisse de son sommet** ?
"""
        etapes = [
            Etape(
                "Identifier — la forme canonique affiche le sommet",
                f"Cette écriture est faite pour cela : le carré est nul exactement "
                f"quand ${notation.var} {_signe(alpha)} = 0$, c'est-à-dire en "
                f"${notation.var} = {L(alpha)}$. Partout ailleurs, le carré est "
                "strictement positif.",
            ),
            Etape(
                "Lire le sommet",
                f"Le sommet est le point $({L(alpha)}\\,;\\,{L(beta)})$ : l'abscisse "
                "dans la parenthèse — **avec le signe opposé** — et l'ordonnée à la "
                "fin.",
                rf"{notation.var}_S = {L(alpha)} \qquad "
                rf"{notation.nom}({L(alpha)}) = {L(beta)}",
            ),
            Etape(
                "Vérifier — de part et d'autre",
                f"${notation.nom}({L(alpha - 1)}) = "
                f"{L(a + beta)}$ et ${notation.nom}({L(alpha + 1)}) = {L(a + beta)}$ : "
                f"deux points symétriques ont la même image, et l'écart à ${L(beta)}$ "
                f"est {'positif' if a > 0 else 'négatif'} — donc "
                f"${L(beta)}$ est bien un {'minimum' if a > 0 else 'maximum'}. ✓",
            ),
            Etape(
                "Interpréter",
                "La forme canonique est la seule des trois à donner le sommet "
                "gratuitement. C'est pour cela qu'on la cherche en optimisation : "
                "elle répond directement à « quelle est la meilleure valeur, et où "
                "est-elle atteinte ? ».",
            ),
        ]
        pieges = [
            (
                float(-alpha),
                f"Signe inversé : dans $({notation.var} {_signe(alpha)})^2$, le carré "
                f"s'annule en ${notation.var} = {L(alpha)}$, pas en ${L(-alpha)}$.",
            ),
            (
                float(beta),
                "C'est l'**ordonnée** du sommet, sa hauteur. L'énoncé demande "
                "l'abscisse.",
            ),
        ]
    else:
        a = random.choice([-3, -2, 2, 4])
        xs = random.choice([-3, -1, 2, 5])
        b = -2 * a * xs
        c = random.choice([-6, 0, 12])
        f = a * v**2 + b * v + c
        reponse = float(xs)
        enonce = f"""
> Soit la fonction du second degré
>
> $$ {notation.de()} = {sp.latex(f)} $$
>
> Quelle est l'**abscisse de son sommet** ?
"""
        etapes = [
            Etape(
                "Identifier — la formule du sommet",
                "Quand ni les racines ni la forme canonique ne sont disponibles, "
                "l'abscisse du sommet se lit directement sur les coefficients.",
                r"x_S = -\frac{b}{2a}",
            ),
            Etape(
                "Appliquer",
                f"Ici $a = {L(a)}$ et $b = {L(b)}$.",
                rf"{notation.var}_S = -\frac{{{L(b)}}}{{2 \times {L(a)}}} = {L(reponse)}",
            ),
            Etape(
                "Vérifier — la symétrie",
                f"${notation.nom}({L(xs - 2)}) = {L(float(f.subs(v, xs - 2)))}$ et "
                f"${notation.nom}({L(xs + 2)}) = {L(float(f.subs(v, xs + 2)))}$ : deux "
                "points symétriques ont bien la même image. ✓ C'est le meilleur "
                "contrôle d'une abscisse de sommet.",
            ),
            Etape(
                "Interpréter",
                f"Le sommet est le point où la grandeur atteint son "
                f"{'maximum' if a < 0 else 'minimum'}. Sa valeur s'obtient ensuite en "
                f"calculant ${notation.nom}({L(reponse)})$ — c'est une seconde étape, "
                "souvent oubliée.",
            ),
        ]
        pieges = [
            (
                float(b) / (2 * a),
                "Erreur de signe : la formule est $-\\frac{b}{2a}$, avec un signe moins.",
            ),
            (float(-b / a), "Il manque le facteur 2 au dénominateur."),
        ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Abscisse du sommet",
        tolerance=1e-6,
        indice="Selon la forme : milieu des racines, lecture de la canonique, ou "
        "$-\\frac{b}{2a}$.",
        pieges=pieges,
    )


# --- 4. Fil rouge : les prix qui annulent la recette -----------------------


def gen_festival() -> Exercice:
    ctx = cx.tirer(cx.MARCHES)
    var = random.choice(["p", "x"])
    sensibilite = random.choice([50, 60, 75, 90])
    prix_max = random.choice([100, 120, 150, 180])
    base = sensibilite * prix_max
    reponse = float(prix_max)
    prix_sommet = prix_max / 2
    forme = random.choice(["quantite", "factorisee", "developpee"])

    if forme == "quantite":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}), la quantité vendue est
>
> $$ N({var}) = {L(base)} - {sensibilite}\\,{var} $$
>
> La recette vaut donc $R({var}) = {var} \\times N({var})$.
>
> À partir de quel prix la recette devient-elle **nulle** (hors prix nul) ?
"""
        lecture = (
            f"$R({var}) = {var}\\,({L(base)} - {sensibilite}{var})$ est un produit de "
            "deux facteurs affines. Il n'y a rien à développer : les racines se "
            "lisent directement."
        )
    elif forme == "factorisee":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}), la recette s'écrit
>
> $$ R({var}) = {var}\\,({L(base)} - {sensibilite}\\,{var}) $$
>
> À partir de quel prix la recette devient-elle **nulle** (hors prix nul) ?
"""
        lecture = (
            "La recette est déjà factorisée : c'est la forme la plus favorable, "
            "puisque les racines s'obtiennent en annulant chaque facteur."
        )
    else:
        # Écrit à la main : SymPy n'espace pas les milliers ni ne place le
        # terme dominant en tête.
        developpee = rf"-{sensibilite}\,{var}^2 + {L(base)}\,{var}"
        enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}), la recette s'écrit
>
> $$ R({var}) = {developpee} $$
>
> À partir de quel prix la recette devient-elle **nulle** (hors prix nul) ?
"""
        lecture = (
            f"La recette est donnée **développée** : les racines n'y sont pas "
            f"lisibles. Premier geste, factoriser par ${var}$ — le facteur commun "
            f"évident : $R({var}) = {var}\\,({L(base)} - {sensibilite}{var})$. "
            "Le discriminant n'est pas nécessaire quand un facteur commun saute "
            "aux yeux."
        )

    etapes = [
        Etape(
            "Identifier — se ramener à un produit",
            lecture,
        ),
        Etape(
            "Annuler chaque facteur",
            "Un produit est nul si l'un de ses facteurs l'est.",
            rf"{var} = 0 \quad \text{{ou}} \quad {L(base)} - {sensibilite}\,{var} = 0 "
            rf"\iff {var} = \frac{{{L(base)}}}{{{sensibilite}}} = {L(prix_max)}",
        ),
        Etape(
            "Vérifier — les deux racines ont un sens concret",
            f"À ${var} = 0$, c'est gratuit : {_fr(base, 0)} {ctx.unite_quantite} "
            f"sont écoulées mais ne rapportent rien. À ${var} = {L(prix_max)}$ "
            f"{ctx.unite_prix}, le prix est si élevé que la quantité vendue tombe à "
            "zéro : la recette est nulle pour la raison inverse. ✓",
        ),
        Etape(
            "Interpréter — le sommet est déjà lisible",
            f"Les deux racines encadrent le maximum, qui se situe exactement à leur "
            f"milieu : ${var} = \\frac{{0 + {L(prix_max)}}}{{2}} = {L(prix_sommet)}$ "
            f"{ctx.unite_prix}. Sans aucun calcul supplémentaire, on connaît donc "
            "déjà le prix qui maximise la recette. C'est ce que la forme factorisée "
            "rend possible — et ce que la forme développée cache.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Prix annulant la recette",
        unite=ctx.unite_prix,
        tolerance=0.002,
        indice="La recette est un produit : quand un produit est-il nul ?",
        pieges=[
            (
                float(prix_sommet),
                "C'est le prix qui **maximise** la recette (le milieu des racines), "
                "pas celui qui l'annule.",
            ),
            (
                float(base),
                f"C'est une quantité, en {ctx.unite_quantite}, pas un prix. Vérifiez "
                "l'unité de votre réponse.",
            ),
            (
                0.0,
                "L'énoncé écarte explicitement le prix nul : on cherche l'autre racine.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Orientation de la parabole",
        "2️⃣ Racines",
        "3️⃣ Le sommet",
        "4️⃣ Recette nulle",
    ]
)

with onglets[0]:
    st.subheader("Vers le haut ou vers le bas ?")
    executer("s4_orientation", gen_orientation)

with onglets[1]:
    st.subheader("Lire les racines sur la forme factorisée")
    executer("s4_racines", gen_racines)

with onglets[2]:
    st.subheader("Localiser le sommet")
    executer("s4_sommet", gen_sommet)

with onglets[3]:
    st.subheader("Les prix qui annulent la recette")
    executer("s4_festival", gen_festival)

st.markdown("---")
st.caption(
    "Semestre — séance n°4 : Le second degré, parabole et forme factorisée · "
    "Fil rouge E : le festival de Villeneuve · Sciences Po."
)
