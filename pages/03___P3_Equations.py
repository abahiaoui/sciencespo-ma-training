"""Série P3 — Équations à une variable. Fil rouge B : Vélocité."""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P3 | Équations", page_icon="⚖️", layout="wide")

x = sp.Symbol("x")

st.title("⚖️ P3 — Équations à une variable")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Résoudre une équation du premier degré, utiliser l'**équation produit nul**, et
**isoler une variable** dans une formule — la compétence la plus utile de tout le
module.

### 🧠 Le principe unique
Une équation est une balance : tout ce qu'on fait d'un côté, on le fait de l'autre.
Ajouter, retrancher, multiplier ou diviser par un nombre **non nul** ne change pas
l'ensemble des solutions. Tout le reste en découle.

### 🚲 Fil rouge B — Vélocité
Villeneuve lance *Vélocité*, un service de vélos en libre-service : **40 000 €** de
coûts fixes, **350 €** par vélo mis en circulation, et **90 €** de recette par
abonnement vendu.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 3")
    st.markdown("**Ce qu'on a le droit de faire à une égalité**")
    st.latex(r"a = b \iff a + k = b + k")
    st.latex(r"a = b \iff ka = kb \quad (k \neq 0)")
    st.markdown("**Équation du premier degré**")
    st.latex(r"ax + b = cx + d \iff x = \frac{d-b}{a-c}")
    st.markdown("**Équation produit nul**")
    st.latex(r"A \times B = 0 \iff A = 0 \ \text{ou} \ B = 0")
    st.info(
        "**Isoler une variable**\n\n"
        "Même méthode, mais les autres lettres sont traitées comme des nombres. "
        "C'est la compétence la plus utile du module."
    )
    st.error(
        "**Le réflexe obligatoire**\n\n"
        "Toute solution se vérifie en la réinjectant dans l'équation de départ."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


#: L'inconnue ne s'appelle pas toujours $x$ : à l'examen, ce sera $q$, $t$ ou $n$.
INCONNUES = ["x", "y", "t", "q", "n"]


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


# --- 1. Équation du premier degré ------------------------------------------


def gen_premier_degre() -> Exercice:
    var = random.choice(INCONNUES)
    v = sp.Symbol(var)
    forme = random.choice(["deux_membres", "parentheses", "fraction"])
    sol = random.choice([-4, -3, -2, 2, 3, 4, 5, 6])

    if forme == "parentheses":
        a = random.choice([2, 3, 4, 5])
        b = random.choice([-6, -3, 1, 4])
        c = a * (sol + b)
        equation = rf"{a}\,({var} {'+' if b >= 0 else '-'} {L(abs(b))}) = {L(c)}"
        strategie = (
            "L'inconnue est **enfermée dans une parenthèse**. Deux chemins : "
            f"développer, ou diviser d'abord les deux membres par ${a}$. Le second "
            "est plus court et évite les erreurs de distributivité."
        )
        resolution = (
            rf"{var} {'+' if b >= 0 else '-'} {L(abs(b))} = "
            rf"\frac{{{L(c)}}}{{{a}}} = {L(c // a)} \iff {var} = {L(sol)}"
        )
        pieges = [
            (
                float(c - b),
                f"Vous avez retranché ${L(b)}$ sans avoir divisé par ${a}$ : le "
                "facteur porte sur **toute** la parenthèse.",
            ),
            (
                float(c) / a + b,
                "Erreur de signe au moment de faire passer la constante de l'autre "
                "côté.",
            ),
        ]
    elif forme == "fraction":
        a = random.choice([2, 3, 4, 5])
        b = random.choice([-6, -2, 3, 7])
        # x/a + b = c
        c = sp.Rational(sol, a) + b
        equation = rf"\frac{{{var}}}{{{a}}} {'+' if b >= 0 else '-'} {L(abs(b))} = {sp.latex(c)}"
        strategie = (
            f"L'inconnue est **divisée** par ${a}$. On isole d'abord le quotient en "
            f"déplaçant la constante, puis on multiplie les deux membres par ${a}$ — "
            "l'opération qui défait une division."
        )
        resolution = (
            rf"\frac{{{var}}}{{{a}}} = {sp.latex(c - b)} \iff "
            rf"{var} = {a} \times {sp.latex(c - b)} = {L(sol)}"
        )
        pieges = [
            (
                float(c - b) / a,
                f"Vous avez **divisé** par ${a}$ alors que l'inconnue était déjà au "
                "dénominateur : c'est une multiplication qu'il fallait faire.",
            ),
            (
                float(c) * a,
                "Vous avez multiplié avant d'avoir déplacé la constante : le facteur "
                "porte alors sur elle aussi.",
            ),
        ]
    else:
        a = random.choice([2, 3, 4, 5, 6, 7])
        c = random.choice([-3, -2, -1, 1, 2, 3])
        while a == c:
            c = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.choice([-8, -5, -2, 1, 4, 7])
        d = (a - c) * sol + b
        equation = rf"{sp.latex(a * v + b)} = {sp.latex(c * v + d)}"
        strategie = (
            f"Il y a des ${var}$ des deux côtés et des constantes des deux côtés. "
            f"La stratégie est invariable : les ${var}$ d'un côté, les nombres de "
            "l'autre, puis une division."
        )
        resolution = (
            rf"{sp.latex((a - c) * v)} = {L(d - b)} \iff "
            rf"{var} = \frac{{{L(d - b)}}}{{{L(a - c)}}} = {L(sol)}"
        )
        pieges = [
            (
                float(d + b) / (a - c),
                "Erreur de signe : faire passer une constante de l'autre côté, c'est "
                "la **retrancher** des deux membres, pas l'ajouter.",
            ),
            (
                float(d - b) / (a + c) if a + c != 0 else 0.0,
                f"Erreur de signe en regroupant les ${var}$ : le coefficient devient "
                f"$a - c = {L(a - c)}$.",
            ),
        ]

    enonce = f"""
> Résolvez l'équation suivante, d'inconnue ${var}$ :
>
> $$ {equation} $$
"""

    etapes = [
        Etape(
            "Identifier — repérer où se trouve l'inconnue",
            strategie,
        ),
        Etape(
            "Calculer — défaire les opérations une à une",
            "Chaque opération porte sur les **deux** côtés de la balance. C'est la "
            "seule règle, et elle suffit pour toutes les formes d'équations du "
            "premier degré.",
            resolution,
        ),
        Etape(
            "Vérifier — réinjecter la solution",
            f"On remplace ${var}$ par ${L(sol)}$ dans l'équation de départ et l'on "
            "contrôle que les deux membres coïncident. Cette vérification est "
            "toujours possible et devrait être systématique.",
        ),
        Etape(
            "Interpréter",
            "Résoudre une équation, c'est répondre à : « pour quelle valeur ces deux "
            "quantités deviennent-elles égales ? ». Appliquée à deux dispositifs, "
            "cette valeur est un **seuil**.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle=f"{var} =",
        tolerance=1e-6,
        indice="Repérez ce qui entoure l'inconnue, et défaites chaque opération.",
        pieges=pieges,
    )


# --- 2. Équation produit nul ------------------------------------------------


def gen_produit_nul() -> Exercice:
    var = random.choice(INCONNUES)
    v = sp.Symbol(var)
    forme = random.choice(["deux_affines", "coefficient_devant", "facteur_variable"])

    if forme == "coefficient_devant":
        k = random.choice([2, 3, -2])
        r1 = random.choice([-6, -3, 1, 4])
        r2 = r1 + random.choice([2, 3, 5])
        expression = (
            rf"{L(k)}\,({var} {'-' if r1 >= 0 else '+'} {L(abs(r1))})"
            rf"\,({var} {'-' if r2 >= 0 else '+'} {L(abs(r2))})"
        )
        solutions = [Fraction(r1), Fraction(r2)]
        lecture = (
            f"Le facteur ${L(k)}$ placé devant ne s'annule jamais : il ne donne "
            "aucune solution. Seules les deux parenthèses comptent."
        )
        detail = (
            rf"{var} {'-' if r1 >= 0 else '+'} {L(abs(r1))} = 0 \quad\text{{ou}}\quad "
            rf"{var} {'-' if r2 >= 0 else '+'} {L(abs(r2))} = 0 \iff "
            rf"{var} = {L(r1)} \quad\text{{ou}}\quad {var} = {L(r2)}"
        )
        piege_developpe = float(k * r1 * r2)
    elif forme == "facteur_variable":
        a = random.choice([2, 3, 5])
        b = random.choice([-20, -12, 15, 24])
        expression = rf"{var}\,({sp.latex(a * v + b)})"
        solutions = [Fraction(0), Fraction(-b, a)]
        lecture = (
            "Le premier facteur est l'inconnue elle-même : elle s'annule en $0$. "
            "C'est une solution à part entière, qu'on oublie très souvent."
        )
        detail = (
            rf"{var} = 0 \quad\text{{ou}}\quad {sp.latex(a * v + b)} = 0 \iff "
            rf"{var} = 0 \quad\text{{ou}}\quad {var} = "
            rf"{sp.latex(sp.Rational(-b, a))}"
        )
        piege_developpe = 0.0
    else:
        a = random.choice([1, 2, 3, 4])
        b = random.choice([-12, -8, -6, 5, 9, 15])
        c = random.choice([1, 2, 5])
        d = random.choice([-20, -10, 4, 14])
        expression = rf"({sp.latex(a * v + b)})({sp.latex(c * v + d)})"
        solutions = [Fraction(-b, a), Fraction(-d, c)]
        lecture = (
            "Les deux facteurs sont affines : chacun s'annule pour une valeur, qu'on "
            "obtient par une division."
        )
        detail = (
            rf"{sp.latex(a * v + b)} = 0 \quad\text{{ou}}\quad "
            rf"{sp.latex(c * v + d)} = 0 \iff {var} = "
            rf"{sp.latex(sp.Rational(-b, a))} \quad\text{{ou}}\quad {var} = "
            rf"{sp.latex(sp.Rational(-d, c))}"
        )
        piege_developpe = float(b * d) / (a * c)

    reponse = float(max(solutions))

    enonce = f"""
> Résolvez l'équation produit nul suivante, d'inconnue ${var}$ :
>
> $$ {expression} = 0 $$
>
> Donnez la **plus grande** des deux solutions.
"""

    etapes = [
        Etape(
            "Identifier — surtout ne pas développer",
            f"Un produit est nul **si et seulement si** l'un de ses facteurs est nul. "
            f"La forme factorisée donne donc directement les solutions ; développer "
            f"détruirait cette information. {lecture}",
        ),
        Etape("Séparer en équations simples", "", detail),
        Etape(
            "Vérifier",
            f"En remplaçant ${var}$ par ${L(float(max(solutions)))}$, le facteur "
            "correspondant s'annule, donc le produit aussi — quelle que soit la valeur "
            "de l'autre facteur. ✓ C'est exactement ce que dit la règle.",
        ),
        Etape(
            "Interpréter",
            "Cette règle explique pourquoi la factorisation de la séance 2 était "
            "utile : une expression factorisée livre ses zéros immédiatement. Au "
            "semestre, c'est ainsi qu'on trouvera les racines d'une parabole.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Plus grande solution",
        tolerance=1e-6,
        indice="Un produit est nul si l'un des facteurs est nul. Deux équations "
        "simples, donc.",
        pieges=[
            (
                float(min(solutions)),
                "C'est la **plus petite** des deux solutions. L'énoncé demande la plus "
                "grande.",
            ),
            (
                piege_developpe,
                "Vous avez développé puis cherché autre chose. La forme factorisée "
                "donnait les solutions sans aucun calcul supplémentaire.",
            ),
        ],
    )


# --- 3. Isoler une variable -------------------------------------------------


def gen_isoler() -> Exercice:
    modele = random.choice(["affine", "produit", "moyenne", "pourcentage"])

    if modele == "affine":
        a = random.choice([2, 3, 5, 8])
        b = random.choice([10, 25, 40, 60])
        y0 = random.choice([50, 80, 120, 200])
        reponse = float(Fraction(y0 - b, a))
        formule = rf"y = {a}x + {b}"
        question = f"Sachant que $y = {y0}$, que vaut $x$ ?"
        etapes_calcul = (
            rf"{y0} = {a}x + {b} \iff {a}x = {L(y0 - b)} \iff "
            rf"x = \frac{{{L(y0 - b)}}}{{{a}}} = {L(reponse)}"
        )
        commentaire = (
            "Les autres lettres sont traitées exactement comme des nombres : la "
            "méthode ne change pas d'un iota par rapport à l'onglet 1."
        )
        pieges = [
            (
                float(y0 + b) / a,
                "Erreur de signe : on **retranche** la constante des deux membres.",
            ),
            (
                float(y0) / a,
                "Vous avez oublié la constante : elle doit d'abord être déplacée.",
            ),
        ]
    elif modele == "produit":
        prix = random.choice([12, 15, 20, 25])
        recette = random.choice([600, 900, 1200, 1500])
        reponse = float(Fraction(recette, prix))
        formule = r"R = p \times q"
        question = (
            f"Une recette totale de $R = {L(recette)}$ € est réalisée à un prix "
            f"unitaire de $p = {prix}$ €. Combien d'unités $q$ ont été vendues ?"
        )
        etapes_calcul = (
            rf"{L(recette)} = {prix} \times q \iff q = "
            rf"\frac{{{L(recette)}}}{{{prix}}} = {L(reponse)}"
        )
        commentaire = (
            "Isoler $q$ dans un produit demande une seule opération : diviser les deux "
            "membres par $p$, qui n'est pas nul."
        )
        pieges = [
            (
                float(recette * prix),
                "Vous avez multiplié au lieu de diviser. Pour défaire une "
                "multiplication, on divise.",
            ),
            (
                float(recette - prix),
                "Vous avez soustrait. L'opération à défaire ici est une "
                "multiplication, pas une addition.",
            ),
        ]
    elif modele == "pourcentage":
        taux = random.choice([5, 10, 20, 25])
        arrivee = random.choice([630, 840, 1_260, 2_100])
        coef = 1 + taux / 100
        reponse = arrivee / coef
        formule = r"V_{\text{arrivée}} = V_{\text{départ}} \times (1 + t)"
        question = (
            f"Après une hausse de **{taux} %**, une grandeur vaut "
            f"**{_fr(arrivee, 0)}**. Quelle était sa valeur de départ ?"
        )
        etapes_calcul = (
            rf"V_{{\text{{départ}}}} = \frac{{{L(arrivee)}}}{{{L(coef)}}} "
            rf"\approx {L(round(reponse, 2))}"
        )
        commentaire = (
            "La hausse est une **multiplication** par le coefficient : pour revenir "
            "en arrière, on divise. Retrancher le pourcentage donnerait un autre "
            "nombre, car il porterait sur la mauvaise base."
        )
        pieges = [
            (
                arrivee * (1 - taux / 100),
                f"Vous avez retranché {taux} % de la valeur d'**arrivée**. Le "
                "pourcentage portait sur la valeur de **départ**, qui est justement "
                "l'inconnue.",
            ),
            (
                arrivee - taux,
                "Vous avez soustrait le taux comme s'il s'agissait d'un montant.",
            ),
        ]
    else:
        n = random.choice([4, 5, 6, 8])
        m = random.choice([12, 15, 20, 25])
        autres = random.choice([40, 55, 70, 90])
        reponse = float(n * m - autres)
        formule = r"m = \frac{S}{n}"
        question = (
            f"La moyenne de ${n}$ valeurs vaut ${m}$. La somme des ${n - 1}$ "
            f"premières vaut ${autres}$. Que vaut la dernière ?"
        )
        etapes_calcul = (
            rf"S = n \times m = {n} \times {m} = {L(n * m)} \quad\Rightarrow\quad "
            rf"x = {L(n * m)} - {L(autres)} = {L(reponse)}"
        )
        commentaire = (
            "On isole d'abord la somme totale dans la formule de la moyenne, "
            "puis on en retranche ce que l'on connaît déjà."
        )
        pieges = [
            (
                float(m - autres),
                "Vous avez oublié de remonter à la **somme** : la moyenne doit d'abord "
                "être multipliée par l'effectif.",
            ),
            (
                float(n * m),
                "C'est la somme totale, pas la dernière valeur : il reste à retrancher "
                "les autres.",
            ),
        ]

    enonce = f"""
> On dispose de la relation
>
> $$ {formule} $$
>
> {question}
"""

    etapes = [
        Etape(
            "Identifier — isoler, c'est défaire les opérations",
            "On regarde ce qui « entoure » l'inconnue, et on défait chaque opération "
            "en remontant : une addition se défait par une soustraction, une "
            "multiplication par une division.",
        ),
        Etape("Calculer", commentaire, etapes_calcul),
        Etape(
            "Vérifier — reprendre la formule de départ",
            "On replace la valeur trouvée dans la relation initiale et on contrôle "
            "qu'elle est bien satisfaite. Ce contrôle prend dix secondes.",
        ),
        Etape(
            "Interpréter — pourquoi c'est la compétence la plus utile",
            "Toutes les formules que vous rencontrerez en sciences sociales — taux, "
            "indices, moyennes, élasticités — s'utilisent dans les deux sens. Savoir "
            "retourner une formule vaut mieux que d'en mémoriser plusieurs versions.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur cherchée",
        tolerance=0.005,
        indice="Repérez ce qui entoure l'inconnue, et défaites chaque opération.",
        pieges=pieges,
    )


# --- 4. Fil rouge : un seuil de rentabilité --------------------------------


def gen_velocite() -> Exercice:
    ctx, dispositif_1, _ = random.choice(cx.DISPOSITIFS)
    var = random.choice(["q", "n", "x"])
    fixe = random.choice([30_000, 40_000, 60_000])
    par_unite = random.choice([250, 350, 420])
    recette = random.choice([60, 90, 120])
    parc = random.choice([200, 280, 320, 400, 500])
    cout = fixe + par_unite * parc
    reponse = cout / recette
    presentation = random.choice(["phrase", "formules"])

    if presentation == "phrase":
        enonce = f"""
> **{_maj(ctx.acteur)}.** Le service supporte **{_fr(fixe, 0)} €** de coûts fixes,
> plus **{_fr(par_unite, 0)} €** par équipement mis en circulation. La collectivité
> en met **{parc}** en service.
>
> Chaque {dispositif_1.replace("l'", "").replace("le ", "").replace("la ", "")} vendu
> rapporte **{recette} €**.
>
> À partir de combien de ventes le service couvre-t-il ses coûts ?
> Donnez le nombre de ventes à l'équilibre (non entier accepté).
"""
    else:
        enonce = f"""
> **{_maj(ctx.acteur)}.** Le coût total et la recette s'écrivent
>
> $$ C = {L(fixe)} + {L(par_unite)} \\times {parc} \\qquad
>    R({var}) = {recette}\\,{var} $$
>
> où ${var}$ est le nombre de ventes.
>
> À partir de combien de ventes le service couvre-t-il ses coûts ?
> Donnez le nombre de ventes à l'équilibre (non entier accepté).
"""

    etapes = [
        Etape(
            "Identifier — traduire avant de calculer",
            f"Le coût ne dépend pas du nombre de ventes : avec {parc} équipements, il "
            f"est **fixé**. La recette, elle, dépend du nombre ${var}$ de ventes. "
            "L'équilibre est atteint quand les deux se rejoignent.",
            rf"C = {L(fixe)} + {L(par_unite)} \times {parc} = {L(cout)} "
            rf"\qquad R({var}) = {recette}\,{var}",
        ),
        Etape(
            "Poser l'équation",
            "Couvrir ses coûts signifie recette égale coût.",
            rf"{recette}\,{var} = {L(cout)}",
        ),
        Etape(
            "Résoudre",
            "",
            rf"{var} = \frac{{{L(cout)}}}{{{recette}}} \approx "
            rf"{L(round(reponse, 2))}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur est-il crédible ?",
            f"{_fr(reponse, 0)} ventes pour {parc} équipements, soit environ "
            f"{_fr(reponse / parc, 1)} par équipement. C'est plausible. Un résultat "
            "de 10 ou de 500 000 aurait signalé une erreur d'unité.",
        ),
        Etape(
            "Interpréter — ce que le seuil dit à la collectivité",
            f"En dessous de {_fr(reponse, 0)} ventes, le service est déficitaire et la "
            "différence est financée par le budget général. Le seuil ne dit pas si le "
            "service doit exister — un service public peut être délibérément "
            "subventionné — mais il chiffre exactement ce que coûte ce choix.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Nombre de ventes",
        tolerance=0.005,
        indice="Calculez d'abord le coût total, qui ne dépend pas du nombre de ventes.",
        pieges=[
            (
                float(fixe) / recette,
                f"Vous avez oublié le coût des {parc} équipements : seuls les coûts "
                "fixes ont été couverts.",
            ),
            (
                float(par_unite * parc) / recette,
                "Vous avez oublié les coûts fixes de gestion.",
            ),
            (
                float(cout),
                "C'est le coût total en euros, pas un nombre de ventes. "
                "Il reste à diviser par la recette unitaire.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Premier degré",
        "2️⃣ Équation produit nul",
        "3️⃣ Isoler une variable",
        "4️⃣ Vélocité : le seuil",
    ]
)

with onglets[0]:
    st.subheader("Résoudre une équation du premier degré")
    executer("p3_premier", gen_premier_degre)

with onglets[1]:
    st.subheader("Un produit nul livre ses solutions")
    executer("p3_produit", gen_produit_nul)

with onglets[2]:
    st.subheader("Retourner une formule")
    executer("p3_isoler", gen_isoler)

with onglets[3]:
    st.subheader("Le seuil de rentabilité de Vélocité")
    executer("p3_velocite", gen_velocite)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°3 — Équations à une variable · Fil rouge B : Vélocité · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
