"""Série S9 — La fonction dérivée et les variations. Fil rouge G : l'atelier.

Variation sur trois axes (cf. `contextes.py`) : le contexte, la notation (nom de
fonction, variable) et la **forme** de la fonction à dériver — polynôme de degré
2 ou 3, somme comportant une exponentielle ou un logarithme, produit de deux
facteurs. Les règles sont les mêmes ; c'est la reconnaissance de la structure
qui est évaluée.
"""

import random

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S9 | Dérivée et variations", page_icon="↗️", layout="wide")

st.title("↗️ S9 — La fonction dérivée et les variations")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **fonction dérivée** avec les règles de combinaison, en étudier le
**signe**, dresser un **tableau de variations**, et trouver un extremum.

### 🧠 Le théorème central du chapitre
Le **signe** de $f'$ donne les **variations** de $f$. On ne regarde plus la valeur de
la dérivée mais seulement son signe : étudier une fonction revient donc à étudier le
signe d'une autre, souvent beaucoup plus simple — un trinôme, par exemple, dont on
sait tout depuis la séance 5.

### 🔧 Fil rouge G — L'atelier municipal
L'atelier facture **100 €** la réparation. Son résultat s'écrit
$\\pi(q) = 100q - \\left(40\\,000 + 35q + 0{,}02\\,q^2\\right)
= -0{,}02\\,q^2 + 65q - 40\\,000$.

### ⚠️ Repérez la structure avant de dériver
Somme, produit, exponentielle, logarithme : la première question n'est jamais
« quelle est la dérivée ? » mais « de quelle **structure** s'agit-il ? ». Les
énoncés tirés ici alternent volontairement entre ces formes.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 9")
    st.markdown("**Dérivées usuelles**")
    st.latex(r"(x^n)' = n x^{n-1} \qquad (k)' = 0")
    st.latex(r"(e^x)' = e^x \qquad (\ln x)' = \frac{1}{x}")
    st.markdown("**Règles de combinaison**")
    st.latex(r"(u+v)' = u' + v' \qquad (ku)' = k u'")
    st.latex(r"(uv)' = u'v + uv'")
    st.markdown("**Le théorème central**")
    st.latex(r"f' > 0 \Rightarrow f \nearrow \qquad f' < 0 \Rightarrow f \searrow")
    st.error(
        "**Dérivée nulle et extremum : attention**\n\n"
        "$f'(a) = 0$ ne suffit pas. Il faut que $f'$ **change de signe** en $a$."
    )
    st.info(
        "**La méthode en quatre étapes**\n\n"
        "1. Dériver · 2. Résoudre $f'(x) = 0$ · 3. Étudier le signe de $f'$ · "
        "4. Conclure sur $f$"
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
    cx.NotationFonction("B", "q"),
]


# --- 1. Dériver une somme ---------------------------------------------------


def gen_derivee() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    forme = random.choice(
        ["degre2", "degre3", "exponentielle", "logarithme"]
    )
    b = random.choice([-6, -4, -2, 3, 5])
    c = random.choice([-8, -3, 2, 7])
    d = random.choice([-5, 0, 4, 9])

    if forme == "degre3":
        a = random.choice([1, 2, 3, -2])
        f = a * v**3 + b * v**2 + c * v + d
        lecture = (
            "Une somme se dérive terme à terme, et chaque puissance perd un degré. "
            "Le terme constant disparaît : une grandeur qui ne varie pas n'a pas de "
            "pente."
        )
        controle = (
            f"$ {notation.nom} $ est de degré $3$, sa dérivée de degré $2$. ✓ "
            "Ce contrôle détecte immédiatement un exposant oublié."
        )
    elif forme == "exponentielle":
        a = random.choice([2, 3, 5])
        f = a * sp.exp(v) + b * v**2 + d
        lecture = (
            "La somme comporte une **exponentielle** : sa dérivée est elle-même, et "
            f"le coefficient ${L(a)}$ reste en facteur. Le reste se dérive comme un "
            "polynôme ordinaire."
        )
        controle = (
            f"Le terme ${L(a)}e^{{{var}}}$ est intact après dérivation — c'est la "
            "propriété caractéristique de l'exponentielle, et le meilleur contrôle "
            "de cette question. ✓"
        )
    elif forme == "logarithme":
        a = random.choice([2, 4, 6])
        f = a * sp.log(v) + b * v + d
        lecture = (
            f"La somme comporte un **logarithme** : $(\\ln {var})' = "
            f"\\frac{{1}}{{{var}}}$, donc le terme ${L(a)}\\ln {var}$ donne "
            f"$\\frac{{{L(a)}}}{{{var}}}$. Le reste est affine."
        )
        controle = (
            f"La dérivée comporte un terme en $\\frac{{1}}{{{var}}}$ : c'est la "
            "signature du logarithme. Si ce terme a disparu, c'est qu'il a été dérivé "
            "comme un polynôme. ✓"
        )
    else:
        a = random.choice([1, 2, 3, 4, -2])
        f = a * v**2 + c * v + d
        lecture = (
            "La dérivée d'une somme est la somme des dérivées, et un coefficient "
            "constant se conserve. Ces deux règles suffisent pour tout polynôme — "
            "elles ne valent ni pour un produit ni pour un quotient."
        )
        controle = (
            f"$ {notation.nom} $ est de degré $2$, sa dérivée de degré $1$. ✓ "
            "Le degré baisse toujours d'une unité."
        )

    reponse = sp.expand(sp.diff(f, v))
    # SymPy note le logarithme népérien « log » : le cours écrit « ln ».
    affichage = sp.latex(f).replace(r"\log", r"\ln")

    enonce = f"""
> Soit la fonction ${notation.nom}$ définie par
>
> $$ {notation.de()} = {affichage} $$
>
> Calculez la **fonction dérivée** ${notation.derivee()}$.
"""

    etapes = [
        Etape(
            "Identifier — reconnaître la structure",
            lecture,
        ),
        Etape(
            "Dériver terme à terme",
            "Chaque terme se traite séparément, puis on recolle. Écrire les termes "
            "les uns sous les autres évite la quasi-totalité des oublis.",
            rf"{notation.derivee()} = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier",
            controle,
        ),
        Etape(
            "Interpréter — $f'$ est une fonction, pas un nombre",
            "C'est le changement de statut décisif de cette séance : en séance 8, on "
            "calculait un nombre dérivé en un point. Ici on obtient une **fonction** "
            "qui donne la pente partout — donc un objet qu'on peut à son tour "
            "étudier, notamment en signe.",
        ),
    ]

    pieges = [
        (
            sp.expand(reponse + d) if d != 0 else sp.expand(reponse + 1),
            "Vous avez conservé le terme constant : sa dérivée est **nulle**.",
        )
    ]
    if forme == "exponentielle":
        pieges.append(
            (
                sp.expand(reponse - a * sp.exp(v)),
                "Vous avez fait disparaître l'exponentielle. $(e^{x})' = e^{x}$ : "
                "elle reste, inchangée.",
            )
        )
    if forme == "logarithme":
        pieges.append(
            (
                sp.expand(reponse - a / v + a),
                f"Vous avez dérivé $\\ln {var}$ comme un polynôme. Sa dérivée est "
                f"$\\frac{{1}}{{{var}}}$.",
            )
        )

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle=f"{notation.nom}'({var}) =",
        symboles=[var],
        indice="Dérivez chaque terme séparément. Que devient la constante ?",
        pieges=pieges,
    )


# --- 2. Règle du produit ----------------------------------------------------


def gen_produit() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    forme = random.choice(["affine_carre", "affine_affine", "affine_exp"])
    a = random.choice([1, 2, 3])
    b = random.choice([-4, -2, 3, 5])

    if forme == "affine_carre":
        c = random.choice([1, 2])
        d = random.choice([-6, -1, 4])
        u, w = a * v + b, c * v**2 + d
        remarque = (
            "Ici les deux chemins étaient possibles : on pouvait aussi développer "
            "puis dériver terme à terme. Avec une exponentielle ou un logarithme, "
            "seule la règle du produit fonctionnera."
        )
    elif forme == "affine_affine":
        c = random.choice([2, 3, 5])
        d = random.choice([-7, -3, 6])
        u, w = a * v + b, c * v + d
        remarque = (
            "Le produit de deux fonctions affines est un trinôme : la dérivée obtenue "
            "doit donc être **affine**. C'est un contrôle de cohérence gratuit."
        )
    else:
        u, w = a * v + b, sp.exp(v)
        remarque = (
            "Avec une exponentielle, développer est impossible : la règle du produit "
            "n'est plus un raccourci, c'est le seul chemin. Et l'on peut factoriser "
            f"le résultat par $e^{{{var}}}$, ce qui rendra l'étude du signe immédiate."
        )

    reponse = sp.expand(sp.diff(u * w, v))
    up, wp = sp.diff(u, v), sp.diff(w, v)

    enonce = f"""
> Soit la fonction définie par le **produit**
>
> $$ {notation.de()} = ({sp.latex(u)})({sp.latex(w)}) $$
>
> Calculez ${notation.derivee()}$.
"""

    etapes = [
        Etape(
            "Identifier — reconnaître la structure avant de calculer",
            "C'est un produit de deux fonctions : la règle $(uv)' = u'v + uv'$ "
            "s'applique. Et $(uv)'$ n'est **jamais** $u'v'$ — c'est la même erreur de "
            "structure que $(a+b)^2 \\neq a^2 + b^2$.",
        ),
        Etape(
            "Poser $u$, $v$, $u'$ et $v'$",
            "Écrire ces quatre éléments séparément avant d'assembler évite la "
            "quasi-totalité des fautes.",
            rf"u = {sp.latex(u)},\ u' = {sp.latex(up)} \qquad "
            rf"v = {sp.latex(w)},\ v' = {sp.latex(wp)}",
        ),
        Etape(
            "Assembler",
            "",
            rf"{notation.derivee()} = ({sp.latex(up)})({sp.latex(w)}) + "
            rf"({sp.latex(u)})({sp.latex(wp)}) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier",
            remarque,
        ),
        Etape(
            "Interpréter",
            "La règle dit qu'un produit varie pour **deux** raisons : parce que le "
            "premier facteur bouge, et parce que le second bouge. D'où les deux "
            "termes. Cette lecture — un effet total est la somme de plusieurs "
            "canaux — se retrouvera partout.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle=f"{notation.nom}'({var}) =",
        symboles=[var],
        indice="Posez $u$, $v$, $u'$ et $v'$ avant d'assembler.",
        pieges=[
            (
                sp.expand(up * wp),
                "Vous avez calculé $u'v'$. La dérivée d'un produit n'est **jamais** le "
                "produit des dérivées : il faut deux termes.",
            ),
            (
                sp.expand(up * w),
                "Il manque le second terme $uv'$ : le facteur $v$ varie lui aussi.",
            ),
        ],
    )


# --- 3. Tableau de variations : le point critique --------------------------


def gen_variations() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    forme = random.choice(["developpee", "factorisee", "degre3"])

    if forme == "degre3":
        # f' est un trinôme à deux racines : on demande la plus petite.
        r1 = random.choice([-4, -2, 1])
        r2 = r1 + random.choice([2, 4, 6])
        a = random.choice([1, 2])
        # f'(x) = 3a(x - r1)(x - r2) ; on intègre pour obtenir f.
        f = sp.expand(
            a * (v**3 - sp.Rational(3, 2) * (r1 + r2) * v**2 + 3 * r1 * r2 * v)
        )
        derivee = sp.expand(sp.diff(f, v))
        sol = min(r1, r2)
        enonce = f"""
> Soit la fonction ${notation.nom}$ définie par
>
> $$ {notation.de()} = {sp.latex(f)} $$
>
> Sa dérivée s'annule en **deux** valeurs. Donnez la **plus petite**.
"""
        resolution = (
            f"${notation.derivee()} = {sp.latex(derivee)}$ est un trinôme : on le "
            f"factorise, ce qui donne les racines ${L(min(r1, r2))}$ et "
            f"${L(max(r1, r2))}$. C'est la séance 5, réemployée telle quelle."
        )
        signe = (
            f"La dérivée est du signe de son coefficient dominant hors des racines, "
            f"donc positive avant ${L(min(r1, r2))}$, négative entre les deux racines, "
            f"positive après. La fonction croît, décroît, puis croît : deux extrema, "
            f"un **maximum** en ${L(min(r1, r2))}$ et un **minimum** en "
            f"${L(max(r1, r2))}$."
        )
        pieges = [
            (
                float(max(r1, r2)),
                "C'est la **plus grande** des deux valeurs où la dérivée s'annule.",
            ),
            (
                float(r1 + r2),
                "Vous avez additionné les deux racines au lieu d'en choisir une.",
            ),
        ]
    elif forme == "factorisee":
        a = random.choice([1, 2, -1, -2])
        sol = random.choice([-4, -2, 1, 3, 5])
        decalage = random.choice([2, 4, 6])
        # f(x) = a (x - sol)^2 + k : sommet en sol, donc f'(sol) = 0.
        f = sp.expand(a * (v - sol) ** 2 + decalage)
        derivee = sp.expand(sp.diff(f, v))
        enonce = f"""
> Soit la fonction ${notation.nom}$ définie sous forme canonique par
>
> $$ {notation.de()} = {L(a)}\\,({var} {'-' if sol >= 0 else '+'} {L(abs(sol))})^2
>    + {L(decalage)} $$
>
> En quelle valeur de ${var}$ sa dérivée s'annule-t-elle ?
"""
        resolution = (
            f"On peut développer puis dériver, mais la forme canonique donne la "
            f"réponse immédiatement : le sommet est en ${var} = {L(sol)}$, et c'est "
            f"exactement là que la tangente est horizontale. En dérivant, "
            f"${notation.derivee()} = {sp.latex(derivee)}$, qui s'annule bien en "
            f"${L(sol)}$."
        )
        signe = (
            f"${notation.derivee()}$ est affine de pente ${L(2 * a)}$ : elle change "
            f"de signe en ${L(sol)}$, du "
            f"{'négatif au positif' if a > 0 else 'positif au négatif'}. C'est donc "
            f"un **{'minimum' if a > 0 else 'maximum'}**. ✓"
        )
        pieges = [
            (
                float(-sol),
                f"Signe inversé : dans $({var} {'-' if sol >= 0 else '+'} "
                f"{L(abs(sol))})^2$, le carré s'annule en ${var} = {L(sol)}$.",
            ),
            (
                float(decalage),
                "C'est l'ordonnée du sommet, pas son abscisse.",
            ),
        ]
    else:
        a = random.choice([1, 2, 3, -1, -2])
        sol = random.choice([-4, -2, 1, 3, 5, 6])
        b = -2 * a * sol
        c = random.choice([-6, 0, 4, 10])
        f = a * v**2 + b * v + c
        derivee = sp.diff(f, v)
        enonce = f"""
> Soit la fonction ${notation.nom}$ définie par
>
> $$ {notation.de()} = {sp.latex(f)} $$
>
> En quelle valeur de ${var}$ sa dérivée s'annule-t-elle ?
"""
        resolution = (
            f"${notation.derivee()} = {sp.latex(derivee)}$, et l'on résout "
            f"${sp.latex(derivee)} = 0$ : c'est une équation du premier degré, la "
            "pré-rentrée 3 appliquée telle quelle."
        )
        signe = (
            f"${notation.derivee()}({L(sol - 1)}) = "
            f"{L(float(derivee.subs(v, sol - 1)), 0)}$ et "
            f"${notation.derivee()}({L(sol + 1)}) = "
            f"{L(float(derivee.subs(v, sol + 1)), 0)}$ : la dérivée passe du "
            f"{'négatif au positif' if a > 0 else 'positif au négatif'}. C'est donc "
            f"un **{'minimum' if a > 0 else 'maximum'}**. ✓ S'annuler ne suffisait "
            "pas : il fallait ce changement de signe."
        )
        pieges = [
            (
                float(-c / b) if b != 0 else 0.0,
                "Vous avez annulé la fonction plutôt que sa **dérivée**.",
            ),
            (float(b), "Vous avez donné un coefficient, pas la solution de l'équation."),
        ]

    etapes = [
        Etape(
            "Identifier — pourquoi chercher où la dérivée s'annule",
            "Ce sont les seuls points où la fonction peut changer de sens de "
            "variation. Ailleurs, la dérivée garde un signe constant et la fonction "
            "varie de façon monotone. Les points critiques découpent donc l'axe en "
            "zones homogènes.",
        ),
        Etape("Dériver puis résoudre", resolution),
        Etape("Vérifier — étudier le signe autour du point", signe),
        Etape(
            "Interpréter — ce que la dérivation généralise",
            "Pour une parabole, l'abscisse du sommet était donnée par "
            "$-\\frac{b}{2a}$ ; la dérivation retrouve ce résultat, mais s'applique "
            "à **toute** fonction dérivable. Ce qui n'était qu'une formule devient "
            "une méthode.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle=f"{var} =",
        tolerance=1e-6,
        indice="Dérivez, puis résolvez « dérivée = 0 ».",
        pieges=pieges,
    )


# --- 4. Fil rouge : maximiser un résultat ----------------------------------


def gen_atelier() -> Exercice:
    ctx = cx.tirer(cx.PRODUCTIONS)
    var = random.choice(["q", "x"])
    nom = random.choice(["\\pi", "B", "P"])
    prix = random.choice([100, 120, 80])
    fixe = random.choice([30_000, 40_000, 50_000])
    lineaire = random.choice([25, 35, 40])
    quad = random.choice([0.01, 0.02, 0.025])
    marge = prix - lineaire
    q_star = marge / (2 * quad)
    reponse = float(q_star)
    pi_max = -quad * q_star**2 + marge * q_star - fixe
    presentation = random.choice(["profit_donne", "cout_et_prix"])

    cout_latex = rf"{L(fixe)} + {L(lineaire)}\,{var} + {L(quad)}\,{var}^2"
    profit_latex = rf"-{L(quad)}\,{var}^2 + {L(marge)}\,{var} - {L(fixe)}"

    if presentation == "profit_donne":
        enonce = f"""
> **{_maj(ctx.acteur)}.** Son résultat, en euros, s'écrit
>
> $$ {nom}({var}) = {profit_latex} $$
>
> où ${var}$ est le nombre {_de(ctx.unite_quantite)}.
>
> Combien {_de(ctx.unite_quantite)} maximisent le résultat ?
"""
        mise_en_place = (
            "La fonction objectif est déjà écrite. Il reste à dériver, annuler, "
            "étudier le signe, conclure — la séquence de la séance, sans raccourci."
        )
    else:
        enonce = f"""
> **{_maj(ctx.acteur)}.** Son coût total est
>
> $$ C({var}) = {cout_latex} $$
>
> et chaque {ctx.singulier} est facturé **{prix} €**.
>
> Combien {_de(ctx.unite_quantite)} maximisent le résultat ?
"""
        mise_en_place = (
            f"Premier geste : écrire la fonction à maximiser. Le résultat est la "
            f"recette moins le coût : ${nom}({var}) = {prix}\\,{var} - "
            f"({cout_latex}) = {profit_latex}$. Tant que cette expression n'est pas "
            "écrite, il n'y a rien à dériver."
        )

    etapes = [
        Etape(
            "Identifier — appliquer la méthode en quatre étapes",
            mise_en_place,
        ),
        Etape(
            "Dériver et annuler",
            f"${nom}'({var}) = -{L(2 * quad)}\\,{var} + {L(marge)}$. Annuler cette "
            f"expression revient à égaliser la **recette marginale** ({prix} €) et le "
            f"**coût marginal** ($C'({var}) = {L(lineaire)} + {L(2 * quad)}\\,{var}$) "
            "— c'est la même équation, lue autrement.",
            rf"-{L(2 * quad)}\,{var} + {L(marge)} = 0 \iff "
            rf"{var} = \frac{{{L(marge)}}}{{{L(2 * quad)}}} = {L(reponse, 0)}",
        ),
        Etape(
            "Étudier le signe de la dérivée",
            f"${nom}'$ est affine de pente $-{L(2 * quad)}$, donc **décroissante** : "
            f"elle est positive avant {_fr(reponse, 0)} et négative après. Le résultat "
            "croît puis décroît : c'est bien un **maximum**, et il est global.",
        ),
        Etape(
            "Vérifier",
            f"${nom}({L(reponse - 200, 0)}) = "
            f"{L(-quad * (q_star - 200) ** 2 + marge * (q_star - 200) - fixe, 0)}$ € "
            f"et ${nom}({L(reponse + 200, 0)}) = "
            f"{L(-quad * (q_star + 200) ** 2 + marge * (q_star + 200) - fixe, 0)}$ €, "
            f"tous deux inférieurs à ${nom}({L(reponse, 0)}) = {L(pi_max, 0)}$ €. ✓",
        ),
        Etape(
            "Interpréter — la règle de décision",
            f"Au-delà de {_fr(reponse, 0)} {ctx.unite_quantite}, chaque "
            f"{ctx.singulier} supplémentaire coûte plus de {prix} € à produire : il "
            "détruit du résultat, alors même que le chiffre d'affaires continue "
            "d'augmenter. C'est pourquoi la décision se lit sur la **marge**, jamais "
            f"sur le total. Le résultat maximal vaut ici {_fr(pi_max, 0)} €.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Nombre {_de(ctx.unite_quantite)}",
        tolerance=0.002,
        indice="Écrivez la fonction à maximiser, dérivez, annulez, vérifiez le signe.",
        pieges=[
            (
                float(marge / quad),
                "Vous avez oublié le facteur 2 : la dérivée de $q^2$ est $2q$, pas $q$.",
            ),
            (
                float(pi_max),
                "C'est le **montant** du résultat maximal, pas la quantité qui le "
                "réalise. L'énoncé demande un nombre d'unités.",
            ),
            (
                float(fixe / marge),
                "Vous avez calculé un seuil de rentabilité, pas un optimum. "
                "Couvrir ses coûts et maximiser le résultat sont deux questions "
                "différentes.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dériver une somme",
        "2️⃣ Règle du produit",
        "3️⃣ Tableau de variations",
        "4️⃣ Maximiser un résultat",
    ]
)

with onglets[0]:
    st.subheader("La fonction dérivée")
    executer("s9_derivee", gen_derivee)

with onglets[1]:
    st.subheader("Dériver un produit")
    executer("s9_produit", gen_produit)

with onglets[2]:
    st.subheader("Du signe de f' aux variations de f")
    executer("s9_variations", gen_variations)

with onglets[3]:
    st.subheader("Maximiser le résultat d'un atelier")
    executer("s9_atelier", gen_atelier)

st.markdown("---")
st.caption(
    "Semestre — séance n°9 : La fonction dérivée et les variations · "
    "Fil rouge G : l'atelier municipal · Sciences Po."
)
