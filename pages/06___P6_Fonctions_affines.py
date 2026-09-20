"""Série P6 — Fonctions et fonctions affines. Fil rouge C : le logement étudiant.

Variation sur trois axes (cf. `contextes.py`) : le contexte (marchés et coûts),
la notation (nom de fonction, variable) et la **forme** de la donnée — formule,
phrase, tableau de relevés, produit factorisé ou développable.
"""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P6 | Fonctions affines", page_icon="📐", layout="wide")

x, p_ = sp.symbols("x p")

st.title("📐 P6 — Fonctions et fonctions affines")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Distinguer **image** et **antécédent**, calculer et interpréter une **pente**,
trouver un **équilibre** entre offre et demande, et lire le **signe d'un produit de
fonctions affines**.

### 🧠 La lecture qui compte
Une pente n'est pas un objet géométrique abstrait : c'est **de combien $y$ varie
quand $x$ augmente d'une unité**, avec ses unités. Cette phrase deviendra la dérivée
au semestre.

### 🏠 Fil rouge C — Le marché du logement étudiant
Au loyer $p$ (en euros), les étudiants demandent $D(p) = 4\\,000 - 4p$ logements et
les propriétaires en offrent $O(p) = 200 + 2p$.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 6")
    st.markdown("**Fonction affine**")
    st.latex(r"f(x) = ax + b")
    st.markdown("$a$ : pente · $b$ : ordonnée à l'origine")
    st.markdown("**Pente à partir de deux points**")
    st.latex(r"a = \frac{f(x_B) - f(x_A)}{x_B - x_A}")
    st.markdown("**Image et antécédent**")
    st.markdown(
        "**Image** de $x$ : on remplace, c'est direct.\n\n"
        "**Antécédent** de $y$ : on résout une équation."
    )
    st.info(
        "**Interpréter la pente — toujours avec ses unités**\n\n"
        "« Si le loyer augmente de 1 €, 4 logements de moins sont demandés. »"
    )
    st.error(
        "**Signe et variations : deux lectures différentes**\n\n"
        "Le **signe** dit si $f(x)$ est au-dessus ou en dessous de zéro.\n\n"
        "Les **variations** disent si $f$ monte ou descend."
    )

#: (situation, unité de la variable, unité de l'image, singulier de la variable)
SITUATIONS = [
    ("le coût de fonctionnement d'un équipement", "usagers", "€", "usager"),
    ("la dépense de chauffage d'un bâtiment", "m²", "€", "m²"),
    ("le temps de traitement d'un dossier", "pièces jointes", "minutes", "pièce jointe"),
    ("la facture d'eau d'un logement", "m³ consommés", "€", "m³"),
    ("le coût d'impression d'un tirage", "affiches", "€", "affiche"),
]

#: La fonction affine ne s'appelle pas toujours $f(x)$.
NOTATIONS = [
    cx.NotationFonction("f", "x"),
    cx.NotationFonction("g", "x"),
    cx.NotationFonction("h", "t"),
    cx.NotationFonction("C", "q"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


# --- 1. Image et antécédent -------------------------------------------------


def gen_image_antecedent() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    a = random.choice([-5, -3, -2, 2, 3, 4, 6])
    b = random.choice([-12, -7, 5, 10, 18])
    f = a * v + b
    demande_image = random.choice([True, False])
    presentation = random.choice(["formule", "phrase"])

    if presentation == "formule":
        donnee = f"> $$ {notation.de()} = {sp.latex(f)} $$"
        lecture = "La fonction est donnée sous forme algébrique."
    else:
        situation, unite_x, unite_y, singulier = random.choice(SITUATIONS)
        donnee = (
            f"> On modélise {situation} par une fonction affine : elle vaut "
            f"**{_fr(b, 0)} {unite_y}** pour ${var} = 0$, puis "
            f"**{'augmente' if a > 0 else 'diminue'} de {_fr(abs(a), 0)} {unite_y} "
            f"par {singulier}**."
        )
        lecture = (
            f"La phrase donne l'ordonnée à l'origine (${L(b)}$) et la pente "
            f"(${L(a)}$) : autrement dit ${notation.de()} = {sp.latex(f)}$. "
            "Traduire la phrase en formule est le premier geste."
        )

    if demande_image:
        x0 = random.choice([-3, -2, 2, 3, 5, 7])
        reponse = float(f.subs(v, x0))
        question = (
            f"Calculez l'**image** de ${x0}$ par ${notation.nom}$, c'est-à-dire "
            f"${notation.de(str(x0))}$."
        )
        libelle = f"{notation.nom}({x0}) ="
        calcul = (
            rf"{notation.de(str(x0))} = {L(a)} \times ({x0}) + ({L(b)}) "
            rf"= {L(reponse, 0)}"
        )
        commentaire = (
            f"Calculer une image est une **substitution** : on remplace ${var}$ par "
            "la valeur donnée, sans rien résoudre."
        )
        pieges = [
            (
                float(Fraction(x0 - b, a)),
                "Vous avez cherché un **antécédent** : vous avez résolu une équation "
                "là où une simple substitution suffisait.",
            ),
        ]
        interpretation = (
            f"${notation.de(str(x0))} = {L(reponse, 0)}$ signifie que le point "
            f"$({x0}\\,;\\,{L(reponse, 0)})$ appartient à la droite. Image et point "
            "de la courbe sont deux façons de dire la même chose."
        )
    else:
        sol = random.choice([-3, -1, 2, 4, 6])
        k = a * sol + b
        reponse = float(sol)
        question = (
            f"Quel est l'**antécédent** de ${L(k)}$ par ${notation.nom}$ ? Autrement "
            f"dit, pour quelle valeur de ${var}$ a-t-on "
            f"${notation.de()} = {L(k)}$ ?"
        )
        libelle = f"{var} ="
        calcul = (
            rf"{L(a)}{var} + ({L(b)}) = {L(k)} \iff {L(a)}{var} = {L(k - b)} \iff "
            rf"{var} = \frac{{{L(k - b)}}}{{{L(a)}}} = {L(sol)}"
        )
        commentaire = (
            "Chercher un antécédent, c'est **résoudre une équation** — le chemin "
            "inverse de l'image. C'est exactement la séance 3."
        )
        pieges = [
            (
                float(f.subs(v, k)),
                "Vous avez calculé l'**image** de la valeur donnée. Image et "
                "antécédent vont en sens inverse.",
            ),
            (
                float(k + b) / a,
                "Erreur de signe : on retranche l'ordonnée à l'origine des deux "
                "membres.",
            ),
        ]
        interpretation = (
            f"L'antécédent est unique ici parce que la fonction est affine et que sa "
            f"pente ${L(a)}$ n'est pas nulle. Au semestre, avec une parabole, une "
            "même image pourra avoir deux antécédents — ou aucun."
        )

    enonce = f"""
> Soit la fonction affine ${notation.nom}$ :
>
{donnee}
>
> {question}
"""

    etapes = [
        Etape(
            "Identifier — image ou antécédent ?",
            f"{lecture} C'est ensuite la distinction à faire **avant** tout calcul : "
            "une image se calcule, un antécédent se cherche. Les confondre revient à "
            "résoudre le problème inverse de celui qui est posé.",
        ),
        Etape("Calculer", commentaire, calcul),
        Etape(
            "Vérifier",
            "Dans les deux cas, le contrôle est le même : le couple obtenu "
            "doit satisfaire l'équation de la droite. Dix secondes, et la question "
            "est close.",
        ),
        Etape("Interpréter", interpretation),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=libelle,
        tolerance=1e-6,
        indice="Image : on remplace. Antécédent : on résout.",
        pieges=pieges,
    )


# --- 2. Pente et interprétation --------------------------------------------


def gen_pente() -> Exercice:
    situation, unite_x, unite_y, singulier = random.choice(SITUATIONS)
    xa = random.choice([0, 5, 10, 20])
    xb = xa + random.choice([5, 10, 15, 20])
    a = random.choice([-4, -3, -2, 2, 3, 5, 8])
    b = random.choice([40, 80, 150, 300])
    ya = a * xa + b
    yb = a * xb + b
    reponse = float(a)
    presentation = random.choice(["liste", "tableau", "phrase"])

    if presentation == "liste":
        donnee = (
            f"> - pour **{xa} {unite_x}** : **{_fr(ya, 0)} {unite_y}**\n"
            f"> - pour **{xb} {unite_x}** : **{_fr(yb, 0)} {unite_y}**"
        )
    elif presentation == "tableau":
        tableau = cx.tableau_latex(
            [unite_x.capitalize(), f"${xa}$", f"${xb}$"],
            [[f"{unite_y}", f"${L(ya)}$", f"${L(yb)}$"]],
        )
        donnee = "\n".join("> " + ligne for ligne in tableau.splitlines())
    else:
        donnee = (
            f"> Quand on passe de **{xa}** à **{xb} {unite_x}**, la grandeur passe de "
            f"**{_fr(ya, 0)}** à **{_fr(yb, 0)} {unite_y}**."
        )

    enonce = f"""
> On modélise {situation} par une fonction affine. On dispose de deux relevés :
>
{donnee}
>
> Calculez la **pente** de cette fonction.
"""

    etapes = [
        Etape(
            "Identifier — la pente est un rapport de variations",
            "Elle compare la variation verticale à la variation horizontale. "
            "L'ordre des deux points est libre, **à condition** de garder le même "
            "ordre en haut et en bas.",
        ),
        Etape(
            "Calculer",
            f"Variation verticale : ${L(yb)} - {L(ya)} = {L(yb - ya)}$ {unite_y}. "
            f"Variation horizontale : ${xb} - {xa} = {xb - xa}$ {unite_x}.",
            rf"a = \frac{{{L(yb)} - {L(ya)}}}{{{xb} - {xa}}} = "
            rf"\frac{{{L(yb - ya)}}}{{{xb - xa}}} = {L(reponse)}",
        ),
        Etape(
            "Vérifier — le signe correspond-il aux données ?",
            f"Quand la variable augmente, la grandeur "
            f"{'augmente' if yb > ya else 'diminue'} : la pente doit donc être "
            f"{'positive' if a > 0 else 'négative'}. ✓",
        ),
        Etape(
            "Interpréter — toujours avec les unités",
            f"Chaque {singulier} supplémentaire fait "
            f"{'augmenter' if a > 0 else 'diminuer'} {situation} de "
            f"${L(abs(reponse))}$ {unite_y}. C'est **cette phrase** — et non le "
            "nombre seul — qui constitue la réponse attendue à l'examen. "
            "Une pente sans unités n'est pas interprétable.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Pente",
        tolerance=1e-6,
        indice="Variation de la grandeur divisée par variation de la variable, dans "
        "le même ordre.",
        pieges=[
            (
                float(xb - xa) / (yb - ya) if yb != ya else 0.0,
                "Vous avez inversé le rapport : la variation verticale va au "
                "**numérateur**.",
            ),
            (
                float(yb - ya),
                "C'est la variation verticale seule : il reste à la rapporter à la "
                "variation horizontale.",
            ),
            (
                -reponse,
                "Erreur de signe : vérifiez que vous avez soustrait dans le même ordre "
                "en haut et en bas.",
            ),
        ],
    )


# --- 3. Équilibre offre / demande ------------------------------------------


def gen_equilibre() -> Exercice:
    ctx = cx.tirer(cx.MARCHES)
    nom_d, nom_o = random.choice([("D", "O"), ("D", "S"), ("Q_d", "Q_o")])
    var = random.choice(["p", "x"])
    pente_d = random.choice([3, 4, 5, 6])
    pente_o = random.choice([1, 2, 3])
    prix = random.choice([300, 400, 500, 600, 625])
    base_o = random.choice([100, 200, 300])
    base_d = base_o + (pente_d + pente_o) * prix
    quantite = base_d - pente_d * prix
    presentation = random.choice(["formules", "phrase"])

    demande = rf"{nom_d}({var}) = {L(base_d)} - {pente_d}{var}"
    offre = rf"{nom_o}({var}) = {L(base_o)} + {pente_o}{var}"

    if presentation == "formules":
        donnee = (
            f"> - la demande s'écrit $ {demande} $ ;\n"
            f"> - l'offre s'écrit $ {offre} $."
        )
        lecture = "Les deux fonctions sont données : il n'y a qu'à les égaliser."
    else:
        donnee = (
            f"> - la demande s'écrit $ {demande} $ ;\n"
            f"> - du côté de l'offre, on met sur le marché **{_fr(base_o, 0)} "
            f"{ctx.unite_quantite}** à prix nul, et **{pente_o} de plus par "
            f"{ctx.unite_prix} supplémentaire**."
        )
        lecture = (
            f"L'offre est décrite en français : une valeur de départ et une pente. "
            f"C'est exactement ce que signifie $ {offre} $."
        )

    enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}) :
>
{donnee}
>
> Quel est le **prix d'équilibre**, celui pour lequel offre et demande coïncident ?
"""

    etapes = [
        Etape(
            "Identifier — l'équilibre est une égalité",
            f"{lecture} Le marché est à l'équilibre quand la quantité demandée égale "
            "la quantité offerte : chercher l'équilibre revient donc à résoudre une "
            "équation du premier degré — exactement la séance 3.",
            rf"{nom_d}({var}) = {nom_o}({var}) \iff {L(base_d)} - {pente_d}{var} "
            rf"= {L(base_o)} + {pente_o}{var}",
        ),
        Etape(
            "Résoudre",
            f"On rassemble les termes en ${var}$ d'un côté : "
            f"${pente_d}{var} + {pente_o}{var} = {pente_d + pente_o}{var}$. Les deux "
            "pentes étant de signes contraires, leurs valeurs absolues s'additionnent.",
            rf"{L(base_d - base_o)} = {pente_d + pente_o}\,{var} \iff "
            rf"{var} = \frac{{{L(base_d - base_o)}}}{{{pente_d + pente_o}}} "
            rf"= {L(prix)}\ \text{{{ctx.unite_prix}}}",
        ),
        Etape(
            "Vérifier — les deux quantités coïncident-elles ?",
            f"${nom_d}({L(prix)}) = {L(quantite)}$ et "
            f"${nom_o}({L(prix)}) = {L(base_o + pente_o * prix)}$ "
            f"{ctx.unite_quantite}. Identiques. ✓ Vérifier une seule des deux ne "
            "prouverait rien.",
        ),
        Etape(
            "Interpréter — lire les deux pentes",
            f"La pente de la demande est $-{pente_d}$ : si le prix augmente de 1 "
            f"{ctx.unite_prix}, {pente_d} {ctx.unite_quantite} de moins sont "
            f"demandées. Celle de l'offre est $+{pente_o}$. Au prix de "
            f"{_fr(prix, 0)} {ctx.unite_prix}, {_fr(quantite, 0)} "
            f"{ctx.unite_quantite} changent de mains — au-dessus, des invendus ; en "
            "dessous, des acheteurs sans offre.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(prix),
        etapes=etapes,
        libelle="Prix d'équilibre",
        unite=ctx.unite_prix,
        tolerance=1e-6,
        indice="Offre égale demande : une équation du premier degré.",
        pieges=[
            (
                float(base_d - base_o) / (pente_d - pente_o)
                if pente_d != pente_o
                else 0.0,
                "Les deux pentes se **soustraient** dans l'équation, donc leurs "
                f"valeurs absolues s'**additionnent** : ${pente_d} + {pente_o} = "
                f"{pente_d + pente_o}$ au dénominateur.",
            ),
            (
                float(quantite),
                f"C'est la **quantité** échangée à l'équilibre, en "
                f"{ctx.unite_quantite}, pas le prix.",
            ),
            (
                float(base_d + base_o) / (pente_d + pente_o),
                "Les deux constantes se soustraient, elles ne s'additionnent pas.",
            ),
        ],
    )


# --- 4. Signe d'un produit de fonctions affines (QCM) ----------------------


def gen_signe_produit() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    forme = random.choice(["pentes_opposees", "pentes_positives", "developpable"])
    r1 = random.choice([-4, -2, 1, 3])
    r2 = r1 + random.choice([2, 3, 5])

    if forme == "pentes_positives":
        a1 = random.choice([1, 2])
        a2 = random.choice([1, 3])
        expression = (
            rf"{L(a1)}({var} {'-' if r1 >= 0 else '+'} {L(abs(r1))})"
            rf"\times {L(a2)}({var} {'-' if r2 >= 0 else '+'} {L(abs(r2))})"
        )
        positif_entre = False
        lecture_pentes = (
            f"Les deux facteurs ont des pentes **positives** (${L(a1)}$ et "
            f"${L(a2)}$) : chacun est négatif avant sa racine et positif après. Le "
            "produit est donc positif quand les deux sont du même signe, c'est-à-dire "
            "à l'**extérieur** des racines."
        )
    elif forme == "developpable":
        a1 = random.choice([1, 2])
        a2 = random.choice([-1, -2])
        expression = (
            rf"({L(a1)}{var} {'-' if a1 * r1 >= 0 else '+'} {L(abs(a1 * r1))})"
            rf"({L(a2)}{var} {'-' if a2 * r2 >= 0 else '+'} {L(abs(a2 * r2))})"
        )
        positif_entre = True
        lecture_pentes = (
            f"Les pentes sont de signes contraires (${L(a1)}$ et ${L(a2)}$). Les "
            f"racines ne se lisent pas directement : il faut annuler chaque facteur, "
            f"ce qui donne ${L(r1)}$ et ${L(r2)}$."
        )
    else:
        a1 = random.choice([1, 2, 3])
        a2 = random.choice([-1, -2, -3])
        expression = (
            rf"{L(a1)}({var} {'-' if r1 >= 0 else '+'} {L(abs(r1))})"
            rf"\times {L(a2)}({var} {'-' if r2 >= 0 else '+'} {L(abs(r2))})"
        )
        positif_entre = True
        lecture_pentes = (
            f"Le premier facteur, de pente ${L(a1)}$ (positive), est négatif avant "
            f"${L(r1)}$ et positif après. Le second, de pente ${L(a2)}$ (négative), "
            f"fait l'inverse autour de ${L(r2)}$. Le signe du produit suit la règle "
            "des signes."
        )

    f = sp.expand(a1 * (v - r1) * a2 * (v - r2))

    entre_positif = (
        f"{notation.nom}({var}) > 0 sur ]{r1} ; {r2}[ et "
        f"{notation.nom}({var}) < 0 à l'extérieur"
    )
    entre_negatif = (
        f"{notation.nom}({var}) < 0 sur ]{r1} ; {r2}[ et "
        f"{notation.nom}({var}) > 0 à l'extérieur"
    )
    toujours = f"{notation.nom}({var}) > 0 pour tout {var} sauf en {r1} et {r2}"
    signe_var = f"{notation.nom}({var}) a le même signe que {var} sur tout l'axe"
    bonne = entre_positif if positif_entre else entre_negatif
    options = [entre_positif, entre_negatif, toujours, signe_var]
    random.shuffle(options)

    enonce = f"""
> Soit la fonction produit
>
> $$ {notation.de()} = {expression} $$
>
> Quel est le **signe** de ${notation.de()}$ selon les valeurs de ${var}$ ?
"""

    milieu = (r1 + r2) / 2
    test_gauche = float(f.subs(v, r1 - 1))
    test_milieu = float(f.subs(v, milieu))
    test_droite = float(f.subs(v, r2 + 1))

    etapes = [
        Etape(
            "Identifier — surtout ne pas développer",
            f"La forme factorisée donne les **racines** : ${var} = {L(r1)}$ et "
            f"${var} = {L(r2)}$. Ce sont les seuls points où la fonction peut changer "
            "de signe, car un produit ne change de signe que si l'un de ses facteurs "
            "en change.",
        ),
        Etape("Étudier le signe de chaque facteur", lecture_pentes),
        Etape(
            "Vérifier — un test dans chaque zone",
            f"${notation.de(str(r1 - 1))} = {L(test_gauche, 0)}$ · "
            f"${notation.de(L(milieu))} = {L(test_milieu, 0)}$ · "
            f"${notation.de(str(r2 + 1))} = {L(test_droite, 0)}$. ✓ "
            "Trois calculs suffisent à confirmer tout le tableau de signe.",
        ),
        Etape(
            "Interpréter — signe et variations ne sont pas la même chose",
            "Le tableau de **signe** dit où la courbe est au-dessus de l'axe ; le "
            "tableau de **variations** dirait où elle monte. Les deux lectures ne "
            "coïncident pas, et une question de profit positif porte bien sur le "
            "**signe**.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Signe de la fonction",
        indice="Les racines se lisent sur la forme factorisée. Testez une valeur "
        "dans chaque zone.",
        pieges=[
            (
                entre_negatif if positif_entre else entre_positif,
                f"Vérifiez avec un test : ${notation.de(L(milieu))} = "
                f"{L(test_milieu, 0)}$.",
            ),
            (
                toujours,
                "Un produit de deux facteurs affines change bien de signe en "
                "traversant chaque racine : il ne peut pas rester positif partout.",
            ),
            (
                signe_var,
                f"Le signe du produit ne dépend pas de celui de ${var}$ mais de la "
                f"position de ${var}$ par rapport aux racines ${L(r1)}$ et "
                f"${L(r2)}$.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Image ou antécédent",
        "2️⃣ Calculer et lire une pente",
        "3️⃣ Équilibre offre-demande",
        "4️⃣ Signe d'un produit",
    ]
)

with onglets[0]:
    st.subheader("Les deux sens de lecture d'une fonction")
    executer("p6_image", gen_image_antecedent)

with onglets[1]:
    st.subheader("La pente, avec ses unités")
    executer("p6_pente", gen_pente)

with onglets[2]:
    st.subheader("Deux droites qui se croisent")
    executer("p6_equilibre", gen_equilibre)

with onglets[3]:
    st.subheader("Tableau de signe d'un produit")
    executer("p6_signe", gen_signe_produit)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°6 — Fonctions et fonctions affines · "
    "Fil rouge C : le logement étudiant · Sciences Po."
)
