"""Série P4 — Inéquations et systèmes. Fil rouge B : Vélocité (clôture de l'arc)."""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P4 | Inéquations et systèmes", page_icon="🔀", layout="wide")

x, y = sp.symbols("x y")

st.title("🔀 P4 — Inéquations et systèmes")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Résoudre une **inéquation** du premier degré — avec la seule règle qui change —,
résoudre un **système de deux équations à deux inconnues** par substitution ou
combinaison, et lire graphiquement ce que vaut un système.

### 🧠 Ce qui change par rapport à la séance 3
Une inéquation se manipule comme une équation, à une exception près : multiplier ou
diviser par un nombre **négatif renverse le sens** de l'inégalité. Et sa solution
n'est plus une valeur mais un **ensemble** de valeurs.

### 🚲 Fil rouge B — Vélocité (clôture)
Après simplification, la recette vaut $90q$ et le coût $40\\,000 + 87{,}5\\,q$.
Le budget annuel est de **420 000 €** et les stations offrent **500 emplacements**.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 4")
    st.markdown("**Inéquations : les opérations sûres**")
    st.latex(r"a < b \iff a + k < b + k")
    st.latex(r"a < b \iff ka < kb \quad (k > 0)")
    st.error(
        "**La seule règle qui change**\n\n"
        r"$a < b \iff ka > kb \quad (k < 0)$"
        "\n\nMultiplier ou diviser par un **négatif renverse** le sens."
    )
    st.markdown("**Notation des ensembles de solutions**")
    st.latex(r"S = \left]-\infty\,;\,s\right[ \qquad S = \left]s\,;\,+\infty\right[")
    st.markdown("**Systèmes 2×2 — deux méthodes**")
    st.markdown(
        "**Substitution** : isoler une inconnue dans une équation, la reporter "
        "dans l'autre.\n\n"
        "**Combinaison linéaire** : additionner les deux équations après les avoir "
        "multipliées pour éliminer une inconnue."
    )
    st.info(
        "**Trois cas possibles**\n\n"
        "Une solution unique (droites sécantes) · aucune solution (droites "
        "parallèles) · une infinité (droites confondues)."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Inéquation : la borne -----------------------------------------------


def gen_borne() -> Exercice:
    a = random.choice([-6, -5, -4, -3, -2, 3, 4, 5])
    sol = random.choice([-3, -2, 2, 3, 4, 6])
    b = random.choice([-6, -2, 3, 7])
    d = a * sol + b
    sens_final = "<" if a < 0 else ">"

    enonce = f"""
> On considère l'inéquation
>
> $$ {sp.latex(a*x + b)} \\;>\\; {d} $$
>
> Sa solution s'écrit $x < s$ ou $x > s$ selon le cas. **Donnez la valeur de $s$.**
>
> *(Le sens de l'inégalité fait l'objet de l'onglet suivant.)*
"""

    etapes = [
        Etape(
            "Identifier — même mécanique qu'une équation",
            "On isole $x$ exactement comme en séance 3 : on déplace la constante, "
            "puis on divise par le coefficient. Seul le traitement du sens diffère.",
        ),
        Etape(
            "Déplacer la constante",
            "Ajouter ou retrancher un nombre des deux côtés **ne change jamais** le "
            "sens d'une inégalité : cette opération est toujours sûre.",
            rf"{sp.latex(a*x + b)} > {d} \iff {sp.latex(a*x)} > {d - b}",
        ),
        Etape(
            "Diviser par le coefficient",
            f"Le coefficient vaut ${a}$, il est "
            f"**{'négatif' if a < 0 else 'positif'}** : la division "
            f"{'**renverse**' if a < 0 else 'conserve'} le sens.",
            rf"x {sens_final} \frac{{{d - b}}}{{{a}}} = {sol}",
        ),
        Etape(
            "Vérifier — tester une valeur de chaque côté",
            f"Avec $x = {sol - 1}$ : ${a} \\times {sol - 1} + ({b}) = "
            f"{a*(sol-1) + b}$, "
            f"{'bien' if a*(sol-1)+b > d else 'pas'} supérieur à ${d}$. "
            f"Avec $x = {sol + 1}$ : ${a*(sol+1) + b}$, "
            f"{'bien' if a*(sol+1)+b > d else 'pas'} supérieur. ✓ "
            "Deux tests confirment à la fois la borne et le sens.",
        ),
        Etape(
            "Interpréter",
            "Une inéquation ne donne pas une valeur mais un **ensemble** de valeurs. "
            "C'est la forme naturelle d'une condition d'éligibilité, d'un seuil de "
            "rentabilité ou d'un critère de soutenabilité.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="Valeur du seuil s",
        tolerance=1e-6,
        indice="La borne se calcule exactement comme dans une équation.",
        pieges=[
            (float(d + b) / a,
             "Erreur de signe en déplaçant la constante : on la **retranche** des "
             "deux membres."),
        ],
    )


# --- 2. Inéquation : le sens (QCM) -----------------------------------------


def gen_sens() -> Exercice:
    a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    seuil = random.choice([-2, 3, 4, 6, 8])
    sens_initial = random.choice(["<", ">"])
    if a > 0:
        sens_final = sens_initial
    else:
        sens_final = ">" if sens_initial == "<" else "<"

    reponse = f"S = ]{'-∞ ; ' + str(seuil) if sens_final == '<' else str(seuil) + ' ; +∞'}["
    autre = f"S = ]{'-∞ ; ' + str(seuil) if sens_final == '>' else str(seuil) + ' ; +∞'}["
    options = [reponse, autre, f"S = {{{seuil}}}"]
    random.shuffle(options)

    enonce = f"""
> Après calcul, on est arrivé à l'étape suivante :
>
> $$ {sp.latex(a*x)} \\;{sens_initial}\\; {a*seuil} $$
>
> Quel est l'**ensemble des solutions** ?
"""

    etapes = [
        Etape(
            "Identifier — regarder le signe du coefficient",
            f"Le coefficient de $x$ vaut ${a}$ : il est "
            f"**{'négatif' if a < 0 else 'positif'}**. C'est la seule information qui "
            "décide du sens final, et la question se pose **avant** de diviser.",
        ),
        Etape(
            "Appliquer la règle",
            f"Diviser par un nombre {'négatif renverse' if a < 0 else 'positif conserve'} "
            f"le sens : ${sens_initial}$ devient ${sens_final}$.",
            rf"{sp.latex(a*x)} {sens_initial} {a*seuil} \iff x {sens_final} {seuil}",
        ),
        Etape(
            "Vérifier — le test numérique tranche toujours",
            f"Testons $x = {seuil - 1 if sens_final == '<' else seuil + 1}$ : "
            f"${a} \\times {seuil - 1 if sens_final == '<' else seuil + 1} = "
            f"{a * (seuil - 1 if sens_final == '<' else seuil + 1)}$, "
            f"bien ${sens_initial}\\ {a*seuil}$. ✓ "
            "En cas de doute sur la règle, ce test de cinq secondes la remplace.",
        ),
        Etape(
            "Interpréter — pourquoi le sens se renverse",
            "Multiplier par un négatif retourne l'axe des nombres : ce qui était à "
            "droite passe à gauche. $2 < 3$, mais $-2 > -3$. La règle n'est pas une "
            "convention arbitraire, c'est une conséquence de cette symétrie.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Ensemble des solutions",
        indice="Le signe du coefficient de $x$ décide de tout.",
        pieges=[
            (autre,
             f"Le coefficient ${a}$ est **{'négatif' if a < 0 else 'positif'}** : "
             f"diviser par lui {'renverse' if a < 0 else 'conserve'} le sens."),
            (f"S = {{{seuil}}}",
             "Une inéquation n'a pas une solution unique mais un **intervalle** de "
             "solutions."),
        ],
    )


# --- 3. Système 2×2 ---------------------------------------------------------


def gen_systeme() -> Exercice:
    x0 = random.choice([-3, -2, 1, 2, 3, 4, 5])
    y0 = random.choice([-4, -1, 2, 3, 6])
    a1 = random.choice([1, 2, 3])
    b1 = random.choice([1, 2, -1, -2])
    a2 = random.choice([1, 2, 4, -1])
    b2 = random.choice([3, -3, 1, 5])
    while a1 * b2 - a2 * b1 == 0:
        b2 = random.choice([3, -3, 1, 5, 2])
    c1 = a1 * x0 + b1 * y0
    c2 = a2 * x0 + b2 * y0

    enonce = f"""
> Résolvez le système suivant :
>
> $$ \\begin{{cases}}
> {sp.latex(a1*x + b1*y)} = {c1} \\\\
> {sp.latex(a2*x + b2*y)} = {c2}
> \\end{{cases}} $$
>
> Donnez la valeur de $x$.
"""

    det = a1 * b2 - a2 * b1

    etapes = [
        Etape(
            "Identifier — deux inconnues, donc deux équations",
            "Une seule équation à deux inconnues a une infinité de solutions. "
            "Il en faut une seconde pour trancher. L'objectif de toute méthode est "
            "d'**éliminer une inconnue** pour se ramener au cas de la séance 3.",
        ),
        Etape(
            "Calculer — par combinaison linéaire",
            f"On multiplie la première équation par ${b2}$ et la seconde par "
            f"${-b1}$, puis on les additionne : les termes en $y$ disparaissent.",
            rf"({a1} \times {b2} - {a2} \times {b1})\,x = "
            rf"{b2} \times {c1} - {b1} \times {c2} "
            rf"\iff {det}x = {b2*c1 - b1*c2} \iff x = {x0}",
        ),
        Etape(
            "Trouver la seconde inconnue",
            f"On reporte $x = {x0}$ dans la première équation :",
            rf"{a1} \times {x0} + {b1}y = {c1} \iff y = {y0}",
        ),
        Etape(
            "Vérifier — dans les DEUX équations",
            f"Équation 1 : ${a1} \\times {x0} + ({b1}) \\times {y0} = {c1}$ ✓. "
            f"Équation 2 : ${a2} \\times {x0} + ({b2}) \\times {y0} = {c2}$ ✓. "
            "Vérifier une seule équation ne prouve rien : le couple doit satisfaire "
            "les deux simultanément.",
        ),
        Etape(
            "Interpréter — deux droites qui se croisent",
            "Chaque équation décrit une droite. La solution est leur **point "
            f"d'intersection**, ici $({x0}\\,;\\,{y0})$. Comme les deux pentes "
            "diffèrent, les droites sont sécantes et la solution est unique — c'est "
            "le cas général, mais pas le seul possible.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(x0),
        etapes=etapes,
        libelle="x =",
        tolerance=1e-6,
        indice="Éliminez une inconnue pour vous ramener à une équation simple.",
        pieges=[
            (float(y0),
             "Vous avez donné $y$ au lieu de $x$. Les deux valeurs sont justes mais "
             "l'énoncé demande l'abscisse."),
            (float(c1) / a1 if a1 != 0 else 0.0,
             "Vous avez résolu la première équation en ignorant $y$. Une équation à "
             "deux inconnues ne se résout pas seule."),
        ],
    )


# --- 4. Fil rouge : Vélocité bénéficiaire -----------------------------------


def gen_velocite_benefice() -> Exercice:
    fixe = 40_000
    variable = random.choice([87.5, 80.0, 75.0, 82.5])
    recette = 90
    marge = recette - variable
    reponse = fixe / marge

    enonce = f"""
> **Vélocité (clôture de l'arc).** Une fois la flotte ramenée au nombre
> d'abonnements, la recette vaut $90q$ et le coût
> $40\\,000 + {str(variable).replace('.', ',')}\\,q$, où $q$ est le nombre
> d'abonnements.
>
> Pour quels nombres d'abonnements le service est-il **bénéficiaire** ?
> Donnez la borne de l'ensemble des solutions.
"""

    etapes = [
        Etape(
            "Identifier — bénéficiaire signifie recette strictement supérieure au coût",
            "La question se traduit par une **inéquation**, pas une équation : on ne "
            "cherche pas un point d'équilibre mais un ensemble de situations "
            "favorables.",
            rf"90q > 40\,000 + {variable}q",
        ),
        Etape(
            "Rassembler les termes en $q$",
            f"On retranche ${variable}q$ des deux membres. Cette opération ne change "
            "pas le sens de l'inégalité.",
            rf"90q - {variable}q > 40\,000 \iff {marge}q > 40\,000",
        ),
        Etape(
            "Diviser — le coefficient est positif",
            f"Le coefficient ${marge}$ est **positif** : le sens est conservé. "
            "C'est ici qu'il fallait se poser la question, même si la réponse est "
            "rassurante.",
            rf"q > \frac{{40\,000}}{{{marge}}} \approx {reponse:.1f}",
        ),
        Etape(
            "Vérifier",
            f"Pour $q = {int(reponse) + 100}$ : recette "
            f"{90*(int(reponse)+100):,.0f} €, coût "
            f"{40000 + variable*(int(reponse)+100):,.0f} € — bénéficiaire. ✓ "
            f"Pour $q = {int(reponse) - 100}$, la situation s'inverse. ✓"
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — la marge unitaire",
            f"Le nombre ${marge}$ qui apparaît au dénominateur est la **marge par "
            f"abonnement** : ce que chaque abonnement laisse une fois son coût "
            f"variable couvert. Il faut environ {reponse:.0f} abonnements pour que "
            "ces marges cumulées absorbent les 40 000 € de coûts fixes. "
            "Cette lecture — coût fixe divisé par marge unitaire — est le calcul de "
            "seuil de rentabilité standard.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Borne (nombre d'abonnements)",
        tolerance=0.005,
        indice="Rassemblez les termes en $q$ d'un côté : que reste-t-il comme "
        "coefficient ?",
        pieges=[
            (float(fixe) / recette,
             "Vous avez divisé par la recette unitaire au lieu de la **marge**. "
             f"Chaque abonnement ne laisse que {marge} € une fois son coût variable "
             "payé."),
            (float(fixe) / variable,
             "Vous avez divisé par le coût variable unitaire. C'est l'écart entre "
             "recette et coût variable qui compte."),
            (float(fixe) / (recette + variable),
             "Les deux montants se **soustraient** : on cherche ce que rapporte "
             "chaque abonnement net de son coût."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Inéquation : la borne",
        "2️⃣ Inéquation : le sens",
        "3️⃣ Système 2×2",
        "4️⃣ Vélocité bénéficiaire",
    ]
)

with onglets[0]:
    st.subheader("Calculer la borne")
    executer("p4_borne", gen_borne)

with onglets[1]:
    st.subheader("Le sens se renverse-t-il ?")
    executer("p4_sens", gen_sens)

with onglets[2]:
    st.subheader("Deux équations, deux inconnues")
    executer("p4_systeme", gen_systeme)

with onglets[3]:
    st.subheader("Clôture de l'arc Vélocité")
    executer("p4_velocite", gen_velocite_benefice)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°4 — Inéquations et systèmes · Fil rouge B : Vélocité · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
