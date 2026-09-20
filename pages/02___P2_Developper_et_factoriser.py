"""Série P2 — Développer et factoriser. Identités remarquables, facteur commun."""

import random

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P2 | Développer et factoriser", page_icon="✳️", layout="wide")

x, q, n, p_, y = sp.symbols("x q n p y")

st.title("✳️ P2 — Développer et factoriser")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Distribuer un facteur sans perdre un signe, développer un produit de deux parenthèses,
reconnaître une **identité remarquable** au passage, et faire le chemin inverse :
**factoriser**, c'est-à-dire réécrire une somme sous forme de produit.

### 🧠 Pourquoi les deux sens comptent
Développer sert à **comparer** deux expressions ; factoriser sert à **résoudre** et à
**lire un signe**. Au semestre, factoriser une dérivée sera le seul moyen de savoir si
une grandeur augmente ou diminue.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 2")
    st.latex(r"k(a+b) = ka + kb")
    st.latex(r"(a+b)(c+d) = ac + ad + bc + bd")
    st.markdown("**Les trois identités remarquables**")
    st.latex(r"(a+b)^2 = a^2 + 2ab + b^2")
    st.latex(r"(a-b)^2 = a^2 - 2ab + b^2")
    st.latex(r"a^2 - b^2 = (a+b)(a-b)")
    st.error(
        "**L'erreur interdite**\n\n"
        r"$(a+b)^2 \neq a^2 + b^2$"
        "\n\nIl manque le **double produit** $2ab$."
    )
    st.info(
        "**Le réflexe de vérification**\n\n"
        "Remplacez la lettre par $1$ ou $2$ dans l'expression de départ et dans votre "
        "résultat. Les deux doivent donner le même nombre."
    )

CONTEXTES = [
    ("une subvention", "associations"),
    ("une aide au logement", "ménages"),
    ("une bourse", "étudiants"),
    ("une prime de transport", "agents"),
    ("un chèque culture", "lycéens"),
]

#: La lettre change d'un énoncé à l'autre : la méthode, non.
LETTRES = ["x", "y", "q", "n", "t", "p"]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


def _de(mot: str) -> str:
    """« de ménages » mais « d'agents » : élision devant une voyelle."""
    return ("d'" if mot[:1].lower() in "aeiouyéèêh" else 'de ') + mot


# --- 1. Distributivité simple ----------------------------------------------


def gen_distributivite() -> Exercice:
    lettre = random.choice(LETTRES)
    v = sp.Symbol(lettre)
    forme = random.choice(["somme", "difference", "variable_devant"])
    a = random.choice([-4, -3, -2, 2, 3, 5])
    b = random.choice([2, 3, 4, 5])
    c = random.choice([-6, -5, -3, 3, 4, 7])
    d = random.choice([2, 3, 4, 6])
    e = random.choice([1, 2, 3])
    f = random.choice([-3, -1, 1, 2, 4])

    if forme == "difference":
        expression_latex = (
            rf"{sp.latex(a)}({sp.latex(b * v + c)}) - {sp.latex(d)}"
            rf"({sp.latex(e * v + f)})"
        )
        expr = a * (b * v + c) - d * (e * v + f)
        avertissement = (
            f"Le signe **moins** devant ${sp.latex(d)}$ porte sur **toute** la seconde "
            f"parenthèse : il faut distribuer $-{sp.latex(d)}$, donc changer le signe "
            "des deux termes. C'est l'erreur la plus fréquente de la séance."
        )
        piege_signe = sp.expand(a * (b * v + c) - d * e * v + d * f)
        message_signe = (
            "Vous n'avez appliqué le signe moins qu'au **premier** terme de la "
            "parenthèse. Il porte sur les deux."
        )
    elif forme == "variable_devant":
        expression_latex = (
            rf"{lettre}({sp.latex(b * v + c)}) + {sp.latex(d)}({sp.latex(e * v + f)})"
        )
        expr = v * (b * v + c) + d * (e * v + f)
        avertissement = (
            f"Le premier facteur est la lettre elle-même : distribuer donne un terme "
            f"en ${lettre}^2$. Le résultat n'est plus affine, et c'est normal."
        )
        piege_signe = sp.expand(b * v + c + d * (e * v + f))
        message_signe = (
            f"Vous avez oublié de multiplier par ${lettre}$ : chaque terme de la "
            "parenthèse doit être multiplié."
        )
    else:
        expression_latex = (
            rf"{sp.latex(a)}({sp.latex(b * v + c)}) + {sp.latex(d)}"
            rf"({sp.latex(e * v + f)})"
        )
        expr = a * (b * v + c) + d * (e * v + f)
        avertissement = (
            f"Chaque facteur se distribue sur **tous** les termes de sa parenthèse. "
            f"Attention en particulier à ${sp.latex(a)} \\times {sp.latex(c)} = "
            f"{sp.latex(a * c)}$ : le signe fait partie du facteur."
        )
        piege_signe = sp.expand(a * (b * v - c) + d * (e * v + f))
        message_signe = (
            f"Erreur de signe : ${sp.latex(a)} \\times {sp.latex(c)}$ vaut "
            f"${sp.latex(a * c)}$."
        )

    reponse = sp.expand(expr)

    enonce = f"""
> Développez et réduisez :
>
> $$ {expression_latex} $$
"""

    etapes = [
        Etape(
            "Identifier — distribuer, puis réduire",
            avertissement,
        ),
        Etape(
            "Distribuer chaque facteur",
            "On écrit tous les produits avant de regrouper quoi que ce soit. "
            "Sauter cette ligne intermédiaire est la première cause d'erreur.",
            rf"{sp.latex(sp.expand(expr))}",
        ),
        Etape(
            "Regrouper les termes semblables",
            f"On additionne d'un côté les termes en ${lettre}$, de l'autre les "
            "constantes. Ce sont deux familles distinctes qui ne se mélangent jamais.",
            rf"= {sp.latex(reponse)}",
        ),
        Etape(
            f"Vérifier — le test à ${lettre} = 1$",
            f"Dans l'expression de départ comme dans le résultat, remplacer "
            f"${lettre}$ par $1$ doit donner le même nombre : "
            f"${sp.latex(expr.subs(v, 1))}$ dans les deux cas. ✓ Dix secondes qui "
            "évitent une faute.",
        ),
        Etape(
            "Interpréter",
            "Développer sert à **comparer** : deux expressions écrites différemment "
            "ne sont comparables qu'une fois réduites à la même forme. C'est ce qu'on "
            "fera systématiquement pour départager deux dispositifs publics.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="Expression développée et réduite",
        symboles=[lettre],
        indice="Distribuez d'abord, réduisez ensuite. Ne sautez pas l'étape "
        "intermédiaire : c'est là que les signes se perdent.",
        pieges=[(piege_signe, message_signe)],
    )


# --- 2. Double distributivité ----------------------------------------------


def gen_double_distributivite() -> Exercice:
    lettre = random.choice(LETTRES)
    v = sp.Symbol(lettre)
    forme = random.choice(["general", "unitaire", "carre"])

    if forme == "unitaire":
        b = random.choice([-5, -3, 2, 4])
        d = random.choice([-4, -1, 3, 6])
        facteur1, facteur2 = v + b, v + d
        lecture = (
            "Les deux coefficients dominants valent $1$ : le terme en carré a donc "
            "lui aussi un coefficient $1$, et les deux autres produits se regroupent."
        )
    elif forme == "carre":
        a = random.choice([1, 2, 3])
        b = random.choice([-5, -3, 2, 4])
        facteur1 = facteur2 = a * v + b
        lecture = (
            "Les deux parenthèses sont **identiques** : c'est un carré. On peut "
            "appliquer l'identité remarquable, ou faire les quatre produits — les "
            "deux produits croisés étant égaux, ils forment le **double produit**."
        )
    else:
        a = random.choice([1, 2, 3])
        b = random.choice([-5, -3, -2, 2, 4])
        c = random.choice([1, 2])
        d = random.choice([-4, -1, 3, 5, 6])
        facteur1, facteur2 = a * v + b, c * v + d
        lecture = (
            "Chaque terme de la première parenthèse multiplie **chaque** terme de la "
            "seconde. Deux termes par deux termes font quatre produits."
        )

    reponse = sp.expand(facteur1 * facteur2)

    enonce = f"""
> Développez et réduisez :
>
> $$ ({sp.latex(facteur1)})({sp.latex(facteur2)}) $$
"""

    etapes = [
        Etape("Identifier — quatre produits, pas deux", lecture),
        Etape(
            "Écrire les quatre produits",
            "Dans l'ordre, sans en oublier ni en inventer.",
            rf"{sp.latex(sp.expand(facteur1 * facteur2, mul=True))}",
        ),
        Etape(
            "Réduire",
            f"Seuls les termes en ${lettre}$ se regroupent ; le carré et la constante "
            "restent seuls de leur espèce.",
            rf"= {sp.latex(reponse)}",
        ),
        Etape(
            f"Vérifier — le test à ${lettre} = 1$",
            f"Départ : $({sp.latex(facteur1.subs(v, 1))}) \\times "
            f"({sp.latex(facteur2.subs(v, 1))}) = "
            f"{sp.latex(facteur1.subs(v, 1) * facteur2.subs(v, 1))}$. "
            f"Arrivée : ${sp.latex(reponse.subs(v, 1))}$. ✓",
        ),
        Etape(
            "Interpréter",
            "Un produit de deux facteurs devient une somme de trois termes : "
            "la forme change, la valeur non. C'est exactement ce va-et-vient "
            "entre produit et somme qui sera l'outil central du semestre.",
        ),
    ]

    coef1 = sp.Poly(facteur1, v).all_coeffs()
    coef2 = sp.Poly(facteur2, v).all_coeffs()

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="Expression développée et réduite",
        symboles=[lettre],
        indice="Quatre produits. Écrivez-les tous avant de réduire.",
        pieges=[
            (
                sp.expand(coef1[0] * coef2[0] * v**2 + coef1[1] * coef2[1]),
                "Vous n'avez fait que **deux** produits (les premiers entre eux, "
                "les seconds entre eux). Il en manque deux — c'est la même erreur "
                "que $(a+b)^2 = a^2+b^2$.",
            ),
        ],
    )


# --- 3. Identité remarquable : reconnaître le double produit ----------------


def gen_identite() -> Exercice:
    lettre = random.choice(LETTRES)
    v = sp.Symbol(lettre)
    k = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
    signe = random.choice([1, -1])
    ordre = random.choice(["decroissant", "croissant"])

    expression = sp.expand((v + signe * k) ** 2)
    if ordre == "croissant":
        # k^2 ± 2k·lettre + lettre^2 : même expression, écriture inversée.
        affichage = (
            rf"{k ** 2} {'+' if signe > 0 else '-'} {2 * k}\,{lettre} + {lettre}^2"
        )
        remarque_ordre = (
            "Les termes sont écrits dans l'ordre croissant des puissances : cela ne "
            "change rien à l'identité, mais il faut repérer les deux carrés avant de "
            "conclure."
        )
    else:
        affichage = sp.latex(expression)
        remarque_ordre = (
            "Les termes sont dans l'ordre habituel : le carré, le double produit, "
            "puis la constante."
        )

    enonce = f"""
> L'expression suivante est une identité remarquable :
>
> $$ {affichage} $$
>
> Elle se factorise sous la forme $({lettre} {'+' if signe > 0 else '-'} k)^2$.
> **Donnez la valeur de $k$.**
"""

    etapes = [
        Etape(
            "Identifier — trois termes, deux carrés",
            f"{remarque_ordre} La forme $a^2 \\pm 2ab + b^2$ se reconnaît à deux "
            f"carrés encadrant un **double produit**. Ici ${lettre}^2$ et ${k ** 2}$ "
            f"sont les carrés ; le terme du milieu doit valoir "
            f"$2 \\times {lettre} \\times k$.",
        ),
        Etape(
            "Trouver $k$ par le carré, puis confirmer par le double produit",
            f"Le terme constant vaut ${k ** 2}$, donc $k = \\sqrt{{{k ** 2}}} = {k}$. "
            "C'est une hypothèse : il faut la **confirmer** avec le terme du milieu.",
            rf"2 \times {lettre} \times {k} = {2 * k}\,{lettre}",
        ),
        Etape(
            "Vérifier — le double produit confirme",
            f"Le terme du milieu de l'énoncé est bien "
            f"${sp.latex(2 * signe * k * v)}$. Sans cette vérification, on ne saurait "
            "pas distinguer une vraie identité d'un trinôme quelconque.",
            rf"({lettre} {'+' if signe > 0 else '-'} {k})^2 = {sp.latex(expression)}",
        ),
        Etape(
            "Interpréter",
            "L'intérêt de la forme factorisée est qu'elle est un **carré** : elle est "
            "donc toujours positive ou nulle, et nulle en un seul point. "
            f"Ici, l'expression s'annule uniquement pour ${lettre} = "
            f"{-signe * k}$. Cette lecture sera reprise pour l'étude du signe.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(k),
        etapes=etapes,
        libelle="Valeur de k",
        tolerance=1e-6,
        indice="Le terme constant est le carré de $k$. Vérifiez ensuite avec le "
        "terme du milieu, qui doit valoir le double produit.",
        pieges=[
            (
                float(k**2),
                "Vous avez donné le terme constant lui-même. $k$ en est la **racine "
                "carrée**.",
            ),
            (
                float(2 * k),
                "Vous avez donné le coefficient du double produit, qui vaut $2k$ et "
                "non $k$.",
            ),
        ],
    )


# --- 4. Différence de carrés : factoriser ----------------------------------


def gen_difference_carres() -> Exercice:
    lettre = random.choice(LETTRES)
    v = sp.Symbol(lettre)
    a = random.choice([1, 1, 2, 3])
    b = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
    ordre = random.choice(["variable_dabord", "constante_dabord"])

    if ordre == "constante_dabord":
        expression = sp.expand(b**2 - a**2 * v**2)
        reponse = sp.factor(expression)
        lecture = (
            f"C'est **la constante** qui vient en premier : ${b ** 2} - "
            f"({sp.latex(a * v)})^2$. L'identité s'applique dans le même sens, mais "
            "les deux facteurs changent d'allure — mieux vaut écrire $a^2 - b^2$ "
            "explicitement avant de conclure."
        )
        detail = (
            rf"{b}^2 - ({sp.latex(a * v)})^2 = ({sp.latex(b + a * v)})"
            rf"({sp.latex(b - a * v)})"
        )
    else:
        expression = sp.expand(a**2 * v**2 - b**2)
        reponse = sp.factor(expression)
        lecture = (
            f"Deux termes, un signe moins, et chacun est un carré : "
            f"${sp.latex(a ** 2 * v ** 2)} = ({sp.latex(a * v)})^2$ et "
            f"${b ** 2} = {b}^2$. C'est la troisième identité remarquable."
        )
        detail = (
            rf"({sp.latex(a * v)})^2 - {b}^2 = ({sp.latex(a * v + b)})"
            rf"({sp.latex(a * v - b)})"
        )

    enonce = f"""
> **Factorisez** l'expression suivante :
>
> $$ {sp.latex(expression)} $$
"""

    etapes = [
        Etape("Identifier — une différence de deux carrés", lecture),
        Etape(
            "Appliquer $a^2 - b^2 = (a+b)(a-b)$",
            "On identifie les deux carrés, puis on écrit directement le produit.",
            detail,
        ),
        Etape(
            "Vérifier — redévelopper",
            "En redéveloppant, les deux termes du milieu s'annulent : c'est "
            "précisément pourquoi il n'y a pas de double produit dans cette identité. "
            f"Contrôle à ${lettre} = 1$ : ${sp.latex(expression.subs(v, 1))}$ des "
            "deux côtés. ✓",
        ),
        Etape(
            "Interpréter",
            f"Sous forme factorisée, on voit immédiatement que l'expression s'annule "
            f"pour ${lettre} = {sp.latex(sp.Rational(b, a))}$ et "
            f"${lettre} = {sp.latex(-sp.Rational(b, a))}$ — information invisible dans "
            "la forme développée. Factoriser, c'est rendre les zéros lisibles.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        forme="factorisee",
        libelle="Forme factorisée",
        symboles=[lettre],
        indice="Deux carrés séparés par un signe moins : une seule identité "
        "correspond à cette forme.",
        pieges=[
            (
                (a * v - b) ** 2,
                "Vous avez utilisé $(a-b)^2$. Or il n'y a **pas** de terme du milieu "
                "dans l'énoncé : c'est la différence de carrés.",
            ),
        ],
    )


# --- 5. Facteur commun -----------------------------------------------------


def gen_facteur_commun() -> Exercice:
    lettre = random.choice(LETTRES)
    v = sp.Symbol(lettre)
    modele = random.choice(["numerique", "expression", "monome"])

    if modele == "numerique":
        k = random.choice([6, 8, 9, 12, 15])
        u = random.choice([2, 3, 4, 5])
        w = random.choice([3, 5, 7, 9])
        expression = sp.expand(k * u * v - k * w)
        enonce = f"""
> On souhaite factoriser l'expression suivante :
>
> $$ {sp.latex(expression)} $$
>
> **Donnez le plus grand facteur commun** aux deux termes — celui qu'il faut
> mettre en évidence.
"""
        etapes = [
            Etape(
                "Identifier — le plus grand diviseur commun",
                f"Les deux coefficients sont ${k * u}$ et ${k * w}$. Il faut sortir "
                "leur **plus grand** diviseur commun, et non un diviseur quelconque : "
                "une factorisation partielle laisse du travail à faire ensuite.",
            ),
            Etape(
                "Calculer — décomposer les deux coefficients",
                f"${k * u} = {k} \\times {u}$ et ${k * w} = {k} \\times {w}$. "
                f"Le plus grand facteur commun est donc ${k}$.",
                rf"{sp.latex(expression)} = {k}"
                rf"({sp.latex(sp.simplify(expression / k))})",
            ),
            Etape(
                "Vérifier — redistribuer",
                f"${k} \\times {u}{lettre} = {k * u}{lettre}$ et "
                f"${k} \\times ({-w}) = {-k * w}$. ✓ "
                "La vérification d'une factorisation est toujours un développement.",
            ),
            Etape(
                "Interpréter",
                "Factoriser au maximum n'est pas une coquetterie : c'est ce qui rend "
                "la suite lisible. Une expression à moitié factorisée cache encore "
                "l'information qu'on cherchait à faire apparaître.",
            ),
        ]
        return Exercice(
            enonce=enonce,
            reponse=float(k),
            etapes=etapes,
            libelle="Plus grand facteur commun",
            tolerance=1e-6,
            indice="Cherchez le plus grand nombre qui divise les deux coefficients.",
            pieges=[
                (
                    float(k * u),
                    "C'est le premier coefficient, pas le facteur commun : il ne "
                    f"divise pas ${k * w}$.",
                ),
                (
                    float(1),
                    "Tout nombre se divise par 1 : cela ne factorise rien. Cherchez le "
                    "plus grand diviseur commun.",
                ),
            ],
        )

    if modele == "monome":
        k = random.choice([2, 3, 4, 5])
        u = random.choice([2, 3, 4])
        w = random.choice([3, 5, 7])
        expression = sp.expand(k * u * v**2 + k * w * v)
        reponse = sp.factor(expression)
        enonce = f"""
> **Factorisez** l'expression suivante :
>
> $$ {sp.latex(expression)} $$
"""
        etapes = [
            Etape(
                "Identifier — le facteur commun contient la lettre",
                f"Les deux termes contiennent ${lettre}$, et leurs coefficients ont "
                f"${k}$ en commun. Le facteur commun est donc ${k}{lettre}$ — pas "
                "seulement un nombre. C'est le cas qu'on oublie le plus souvent.",
            ),
            Etape(
                "Mettre en évidence",
                "On sort le facteur commun complet, et l'on écrit entre parenthèses "
                "ce qui reste de chaque terme.",
                rf"{sp.latex(expression)} = {sp.latex(reponse)}",
            ),
            Etape(
                "Vérifier — redistribuer",
                f"En redistribuant ${k}{lettre}$ sur la parenthèse, on retrouve "
                "l'expression de départ. ✓",
            ),
            Etape(
                "Interpréter",
                f"Sous cette forme, on lit immédiatement que l'expression s'annule "
                f"pour ${lettre} = 0$ — un zéro que la forme développée ne montrait "
                "pas.",
            ),
        ]
        return Exercice(
            enonce=enonce,
            reponse=reponse,
            etapes=etapes,
            type_reponse="sym",
            forme="factorisee",
            libelle="Forme factorisée",
            symboles=[lettre],
            indice="Les deux termes ont-ils une lettre en commun, en plus d'un "
            "nombre ?",
            pieges=[
                (
                    sp.expand(k * (u * v**2 + w * v)),
                    f"Vous n'avez sorti que le nombre : il restait ${lettre}$ en "
                    "facteur dans les deux termes.",
                ),
            ],
        )

    a = random.choice([2, 3, 4])
    b = random.choice([-5, -3, 1, 3])
    c = random.choice([1, 2])
    d = random.choice([-4, 2, 4, 6])
    commun = v + b
    expression = sp.expand(commun * (a * v + 1) + commun * (c * v + d))
    reponse = sp.factor(expression)

    enonce = f"""
> **Factorisez** l'expression suivante :
>
> $$ ({sp.latex(commun)})({sp.latex(a * v + 1)}) + ({sp.latex(commun)})
>    ({sp.latex(c * v + d)}) $$
"""

    etapes = [
        Etape(
            "Identifier — le facteur commun est une expression",
            f"Le bloc $({sp.latex(commun)})$ apparaît dans les deux termes. Un facteur "
            "commun n'est pas nécessairement un nombre : ce peut être une parenthèse "
            "entière. C'est tout l'enjeu de la question.",
        ),
        Etape(
            "Mettre le bloc en évidence",
            "On écrit le bloc devant, et on additionne entre crochets ce qui reste.",
            rf"({sp.latex(commun)})\big[({sp.latex(a * v + 1)}) + "
            rf"({sp.latex(c * v + d)})\big]",
        ),
        Etape(
            "Réduire le crochet",
            "Seul le contenu du crochet se simplifie ; le facteur commun ne bouge "
            "plus.",
            rf"= {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — pourquoi ne pas développer d'abord",
            "Tout développer puis tenter de refactoriser fonctionne rarement : on perd "
            "de vue le bloc répété. Le réflexe est de **repérer avant de calculer** — "
            "c'est exactement ce qu'on fera devant une dérivée à factoriser.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        forme="factorisee",
        libelle="Forme factorisée",
        symboles=[lettre],
        indice="Ne développez pas. Cherchez ce qui est écrit deux fois à l'identique.",
        pieges=[],
    )


# --- 6. Fil rouge : comparer deux dispositifs ------------------------------


def gen_comparaison() -> Exercice:
    aide, beneficiaires = random.choice(CONTEXTES)
    lettre = random.choice(["n", "x", "q"])
    fixe_a = random.choice([80, 100, 120, 150]) * 1000
    unit_a = random.choice([15, 20, 25, 30])
    ecart_unit = random.choice([10, 15, 20])
    unit_b = unit_a + ecart_unit
    seuil = random.choice([2000, 3000, 4000, 5000])
    fixe_b = fixe_a - ecart_unit * seuil
    ecart_fixe = fixe_a - fixe_b
    presentation = random.choice(["tableau", "liste"])

    if presentation == "tableau":
        tableau = cx.tableau_latex(
            ["Dispositif", "Coût fixe", "Aide par bénéficiaire"],
            [
                ["**A**", f"{_fr(fixe_a, 0)} €", f"{_fr(unit_a, 0)} €"],
                ["**B**", f"{_fr(fixe_b, 0)} €", f"{_fr(unit_b, 0)} €"],
            ],
        )
        donnee = "\n".join("> " + ligne for ligne in tableau.splitlines())
    else:
        donnee = (
            f"> - **Dispositif A** : coût fixe {_fr(fixe_a, 0)} €, aide unitaire "
            f"{_fr(unit_a, 0)} €\n"
            f"> - **Dispositif B** : coût fixe {_fr(fixe_b, 0)} €, aide unitaire "
            f"{_fr(unit_b, 0)} €"
        )

    enonce = f"""
> **Villeneuve** met en place {aide}. Deux dispositifs sont envisagés, chacun avec un
> coût fixe de gestion et une aide unitaire versée à chacun des ${lettre}$
> {beneficiaires} :
>
{donnee}
>
> À partir de combien {_de(beneficiaires)} les deux dispositifs coûtent-ils
> exactement la même chose ?
"""

    etapes = [
        Etape(
            "Identifier — traduire l'énoncé en expressions",
            f"Un coût fixe ne dépend pas de ${lettre}$ ; une aide unitaire se "
            "multiplie par le nombre de bénéficiaires. Chaque dispositif donne donc "
            "une expression de la même forme.",
            rf"D_A({lettre}) = {L(fixe_a)} + {unit_a}\,{lettre} \qquad "
            rf"D_B({lettre}) = {L(fixe_b)} + {unit_b}\,{lettre}",
        ),
        Etape(
            "Calculer — développer et réduire l'écart",
            "Le signe moins porte sur **les deux** termes de la seconde parenthèse. "
            "C'est l'erreur la plus fréquente de cette question.",
            rf"D_A({lettre}) - D_B({lettre}) = ({L(fixe_a)} + {unit_a}\,{lettre}) - "
            rf"({L(fixe_b)} + {unit_b}\,{lettre}) = {L(ecart_fixe)} - "
            rf"{ecart_unit}\,{lettre}",
        ),
        Etape(
            "Annuler l'écart",
            "Les deux dispositifs coûtent la même chose quand leur écart est nul.",
            rf"{L(ecart_fixe)} - {ecart_unit}\,{lettre} = 0 \iff {lettre} = "
            rf"\frac{{{L(ecart_fixe)}}}{{{ecart_unit}}} = {L(seuil)}",
        ),
        Etape(
            "Vérifier — recalculer les deux coûts au seuil",
            f"$D_A({L(seuil)}) = {L(fixe_a + unit_a * seuil)}$ et "
            f"$D_B({L(seuil)}) = {L(fixe_b + unit_b * seuil)}$. Identiques. ✓",
        ),
        Etape(
            "Interpréter — le seuil de bascule",
            f"En dessous de {_fr(seuil, 0)} {beneficiaires}, le dispositif au coût "
            "fixe le plus faible (**B**) l'emporte ; au-delà, c'est **A**, dont l'aide "
            "unitaire plus basse finit par compenser son coût fixe plus élevé. "
            "Cette question « à partir de combien ? » est une des plus fréquentes en "
            "évaluation de politique publique.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(seuil),
        etapes=etapes,
        libelle=f"Nombre de {beneficiaires}",
        tolerance=1e-6,
        indice=f"Écrivez les deux dépenses, puis cherchez pour quel ${lettre}$ leur "
        "différence s'annule.",
        pieges=[
            (
                float(fixe_a + fixe_b) / (unit_a + unit_b),
                "Vous avez **additionné** au lieu de soustraire. On cherche l'égalité "
                "des deux coûts, donc l'annulation de leur différence.",
            ),
            (
                float(ecart_fixe) / (unit_a + unit_b),
                "Le dénominateur est l'écart entre les deux aides unitaires, pas leur "
                "somme.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Distributivité",
        "2️⃣ Double distributivité",
        "3️⃣ Identité remarquable",
        "4️⃣ Différence de carrés",
        "5️⃣ Facteur commun",
        "6️⃣ Deux dispositifs",
    ]
)

with onglets[0]:
    st.subheader("Distribuer sans perdre un signe")
    executer("p2_distrib", gen_distributivite)

with onglets[1]:
    st.subheader("Quatre produits, pas deux")
    executer("p2_double", gen_double_distributivite)

with onglets[2]:
    st.subheader("Reconnaître le double produit")
    executer("p2_identite", gen_identite)

with onglets[3]:
    st.subheader("Factoriser une différence de carrés")
    executer("p2_carres", gen_difference_carres)

with onglets[4]:
    st.subheader("Mettre un facteur commun en évidence")
    executer("p2_commun", gen_facteur_commun)

with onglets[5]:
    st.subheader("Application : le seuil de bascule")
    executer("p2_comparaison", gen_comparaison)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°2 — Développer et factoriser · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
