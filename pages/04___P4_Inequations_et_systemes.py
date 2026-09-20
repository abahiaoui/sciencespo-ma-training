"""Série P4 — Inéquations et systèmes. Fil rouge B : Vélocité (clôture de l'arc)."""

import random

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
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


#: L'inconnue change de lettre d'un énoncé à l'autre.
INCONNUES = ["x", "y", "t", "q", "n"]


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


# --- 1. Inéquation : la borne -----------------------------------------------


def gen_borne() -> Exercice:
    var = random.choice(INCONNUES)
    v = sp.Symbol(var)
    a = random.choice([-6, -5, -4, -3, -2, 3, 4, 5])
    sol = random.choice([-3, -2, 2, 3, 4, 6])
    b = random.choice([-6, -2, 3, 7])
    d = a * sol + b
    comparateur = random.choice([">", "<", r"\geq", r"\leq"])
    sens_final = (
        comparateur
        if a > 0
        else {">": "<", "<": ">", r"\geq": r"\leq", r"\leq": r"\geq"}[comparateur]
    )

    enonce = f"""
> On considère l'inéquation
>
> $$ {sp.latex(a * v + b)} \\;{comparateur}\\; {L(d)} $$
>
> Sa solution est un intervalle de borne $s$. **Donnez la valeur de $s$.**
>
> *(Le sens de l'inégalité fait l'objet de l'onglet suivant.)*
"""

    etapes = [
        Etape(
            "Identifier — même mécanique qu'une équation",
            f"On isole ${var}$ exactement comme en séance 3 : on déplace la constante, "
            "puis on divise par le coefficient. Seul le traitement du sens diffère — "
            "et la borne, elle, ne dépend pas du sens.",
        ),
        Etape(
            "Déplacer la constante",
            "Ajouter ou retrancher un nombre des deux côtés **ne change jamais** le "
            "sens d'une inégalité : cette opération est toujours sûre.",
            rf"{sp.latex(a * v + b)} {comparateur} {L(d)} \iff "
            rf"{sp.latex(a * v)} {comparateur} {L(d - b)}",
        ),
        Etape(
            "Diviser par le coefficient",
            f"Le coefficient vaut ${L(a)}$, il est "
            f"**{'négatif' if a < 0 else 'positif'}** : la division "
            f"{'**renverse**' if a < 0 else 'conserve'} le sens.",
            rf"{var} {sens_final} \frac{{{L(d - b)}}}{{{L(a)}}} = {L(sol)}",
        ),
        Etape(
            "Vérifier — tester une valeur de chaque côté",
            f"Avec ${var} = {L(sol - 1)}$ : ${L(a)} \\times {L(sol - 1)} + "
            f"({L(b)}) = {L(a * (sol - 1) + b)}$. Avec ${var} = {L(sol + 1)}$ : "
            f"${L(a * (sol + 1) + b)}$. L'un vérifie l'inégalité, l'autre non : la "
            "borne est bien là. ✓",
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
            (
                float(d + b) / a,
                "Erreur de signe en déplaçant la constante : on la **retranche** des "
                "deux membres.",
            ),
            (
                float(d - b) * a,
                "Vous avez multiplié par le coefficient au lieu de diviser.",
            ),
        ],
    )


# --- 2. Inéquation : le sens (QCM) -----------------------------------------


def gen_sens() -> Exercice:
    var = random.choice(INCONNUES)
    v = sp.Symbol(var)
    a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    seuil = random.choice([-2, 3, 4, 6, 8])
    presentation = random.choice(["coefficient", "fraction"])
    sens_initial = random.choice(["<", ">"])
    sens_final = sens_initial if a > 0 else (">" if sens_initial == "<" else "<")

    if presentation == "fraction":
        # x/a  <  seuil/a  :  même règle, écriture différente.
        membre_gauche = rf"\frac{{{var}}}{{{L(a)}}}"
        membre_droit = sp.latex(sp.Rational(seuil, a))
        lecture = (
            f"Diviser par ${L(a)}$ ou multiplier par ${L(a)}$ pose la même question : "
            "seul le **signe** du nombre par lequel on multiplie ou divise compte."
        )
    else:
        membre_gauche = sp.latex(a * v)
        membre_droit = L(a * seuil)
        lecture = (
            f"Le coefficient de ${var}$ vaut ${L(a)}$ : il est "
            f"**{'négatif' if a < 0 else 'positif'}**. C'est la seule information qui "
            "décide du sens final, et la question se pose **avant** de diviser."
        )

    bonne = f"S = ]{'-∞ ; ' + str(seuil) if sens_final == '<' else str(seuil) + ' ; +∞'}["
    autre = f"S = ]{'-∞ ; ' + str(seuil) if sens_final == '>' else str(seuil) + ' ; +∞'}["
    unique = f"S = {{{seuil}}}"
    options = [bonne, autre, unique]
    random.shuffle(options)

    enonce = f"""
> Après calcul, on est arrivé à l'étape suivante :
>
> $$ {membre_gauche} \\;{sens_initial}\\; {membre_droit} $$
>
> Quel est l'**ensemble des solutions** ?
"""

    etapes = [
        Etape("Identifier — regarder le signe du coefficient", lecture),
        Etape(
            "Appliquer la règle",
            f"Passer de cette écriture à ${var}$ seul demande une division par "
            f"${L(a)}$, {'négatif : le sens se renverse' if a < 0 else 'positif : le sens est conservé'}. "
            f"${sens_initial}$ devient ${sens_final}$.",
            rf"{membre_gauche} {sens_initial} {membre_droit} \iff "
            rf"{var} {sens_final} {L(seuil)}",
        ),
        Etape(
            "Vérifier — le test numérique tranche toujours",
            f"Testons ${var} = {L(seuil - 1 if sens_final == '<' else seuil + 1)}$ "
            "dans l'inéquation de départ : elle est vérifiée. ✓ En cas de doute sur "
            "la règle, ce test de cinq secondes la remplace intégralement.",
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
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Ensemble des solutions",
        indice="Le signe du nombre par lequel on divise décide de tout.",
        pieges=[
            (
                autre,
                f"Le coefficient ${L(a)}$ est **{'négatif' if a < 0 else 'positif'}** : "
                f"diviser par lui {'renverse' if a < 0 else 'conserve'} le sens.",
            ),
            (
                unique,
                "Une inéquation n'a pas une solution unique mais un **intervalle** de "
                "solutions.",
            ),
        ],
    )


# --- 3. Système 2×2 ---------------------------------------------------------


def gen_systeme() -> Exercice:
    couple = random.choice([("x", "y"), ("x", "y"), ("p", "q"), ("a", "b")])
    var1, var2 = couple
    v1, v2 = sp.Symbol(var1), sp.Symbol(var2)
    presentation = random.choice(["algebrique", "contextuel"])
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
    det = a1 * b2 - a2 * b1

    if presentation == "contextuel":
        # Deux achats groupés : mêmes équations, énoncé en français.
        x0, y0 = abs(x0) + 2, abs(y0) + 3
        a1, b1 = random.choice([2, 3]), random.choice([4, 5])
        a2, b2 = random.choice([5, 6]), random.choice([2, 3])
        while a1 * b2 - a2 * b1 == 0:
            b2 = random.choice([2, 3, 7])
        c1 = a1 * x0 + b1 * y0
        c2 = a2 * x0 + b2 * y0
        det = a1 * b2 - a2 * b1
        enonce = f"""
> Un service achète deux types de fournitures, au prix unitaire ${var1}$ et ${var2}$
> (en euros).
>
> - {a1} unités du premier type et {b1} du second coûtent **{L(c1)} €** ;
> - {a2} unités du premier et {b2} du second coûtent **{L(c2)} €**.
>
> Quel est le prix unitaire ${var1}$ ?
"""
        mise_en_place = (
            "Premier geste : traduire les deux phrases en équations. « {a} unités à "
            f"${var1}$ et {b1} à ${var2}$ » s'écrit "
            f"${a1}{var1} + {b1}{var2} = {L(c1)}$."
        ).replace("{a}", str(a1))
    else:
        enonce = f"""
> Résolvez le système suivant :
>
> $$ \\begin{{cases}}
> {sp.latex(a1 * v1 + b1 * v2)} = {L(c1)} \\\\
> {sp.latex(a2 * v1 + b2 * v2)} = {L(c2)}
> \\end{{cases}} $$
>
> Donnez la valeur de ${var1}$.
"""
        mise_en_place = "Le système est déjà posé : il reste à éliminer une inconnue."

    etapes = [
        Etape(
            "Identifier — deux inconnues, donc deux équations",
            f"{mise_en_place} Une seule équation à deux inconnues a une infinité de "
            "solutions ; il en faut une seconde pour trancher. L'objectif de toute "
            "méthode est d'**éliminer une inconnue** pour se ramener au cas de la "
            "séance 3.",
        ),
        Etape(
            "Calculer — par combinaison linéaire",
            f"On multiplie la première équation par ${L(b2)}$ et la seconde par "
            f"${L(-b1)}$, puis on les additionne : les termes en ${var2}$ "
            "disparaissent.",
            rf"({L(a1)} \times {L(b2)} - {L(a2)} \times {L(b1)})\,{var1} = "
            rf"{L(b2)} \times {L(c1)} - {L(b1)} \times {L(c2)} "
            rf"\iff {L(det)}\,{var1} = {L(b2 * c1 - b1 * c2)} "
            rf"\iff {var1} = {L(x0)}",
        ),
        Etape(
            "Trouver la seconde inconnue",
            f"On reporte ${var1} = {L(x0)}$ dans la première équation :",
            rf"{L(a1)} \times {L(x0)} + {L(b1)}\,{var2} = {L(c1)} \iff "
            rf"{var2} = {L(y0)}",
        ),
        Etape(
            "Vérifier — dans les DEUX équations",
            f"Équation 1 : ${L(a1)} \\times {L(x0)} + ({L(b1)}) \\times {L(y0)} = "
            f"{L(c1)}$ ✓. Équation 2 : ${L(a2)} \\times {L(x0)} + ({L(b2)}) \\times "
            f"{L(y0)} = {L(c2)}$ ✓. Vérifier une seule équation ne prouve rien : le "
            "couple doit satisfaire les deux simultanément.",
        ),
        Etape(
            "Interpréter — deux droites qui se croisent",
            f"Chaque équation décrit une droite. La solution est leur **point "
            f"d'intersection**, ici $({L(x0)}\\,;\\,{L(y0)})$. Comme les deux pentes "
            "diffèrent, les droites sont sécantes et la solution est unique — c'est "
            "le cas général, mais pas le seul possible.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(x0),
        etapes=etapes,
        libelle=f"{var1} =",
        tolerance=1e-6,
        indice="Éliminez une inconnue pour vous ramener à une équation simple.",
        pieges=[
            (
                float(y0),
                f"Vous avez donné ${var2}$ au lieu de ${var1}$. Les deux valeurs sont "
                "justes, mais l'énoncé demande la première.",
            ),
            (
                float(c1) / a1 if a1 != 0 else 0.0,
                "Vous avez résolu la première équation en ignorant la seconde "
                "inconnue. Une équation à deux inconnues ne se résout pas seule.",
            ),
        ],
    )


# --- 4. Fil rouge : un service bénéficiaire ---------------------------------


def gen_velocite_benefice() -> Exercice:
    ctx, dispositif, _ = random.choice(cx.DISPOSITIFS)
    var = random.choice(["q", "n", "x"])
    fixe = random.choice([30_000, 40_000, 55_000])
    recette = random.choice([90, 120, 150])
    variable = recette - random.choice([2.5, 5, 7.5, 10])
    marge = recette - variable
    reponse = fixe / marge

    enonce = f"""
> **{_maj(ctx.acteur)} (clôture de l'arc).** La recette vaut ${recette}\\,{var}$ et le
> coût ${L(fixe)} + {L(variable)}\\,{var}$, où ${var}$ est le nombre de ventes.
>
> Pour quels nombres de ventes le service est-il **bénéficiaire** ?
> Donnez la borne de l'ensemble des solutions.
"""

    etapes = [
        Etape(
            "Identifier — « bénéficiaire » signifie recette strictement supérieure au coût",
            "La question se traduit par une **inéquation**, pas une équation : on ne "
            "cherche pas un point d'équilibre mais un ensemble de situations "
            "favorables.",
            rf"{recette}\,{var} > {L(fixe)} + {L(variable)}\,{var}",
        ),
        Etape(
            f"Rassembler les termes en ${var}$",
            f"On retranche ${L(variable)}\\,{var}$ des deux membres. Cette opération "
            "ne change pas le sens de l'inégalité.",
            rf"{recette}\,{var} - {L(variable)}\,{var} > {L(fixe)} \iff "
            rf"{L(marge)}\,{var} > {L(fixe)}",
        ),
        Etape(
            "Diviser — le coefficient est positif",
            f"Le coefficient ${L(marge)}$ est **positif** : le sens est conservé. "
            "C'est ici qu'il fallait se poser la question, même si la réponse est "
            "rassurante.",
            rf"{var} > \frac{{{L(fixe)}}}{{{L(marge)}}} \approx "
            rf"{L(round(reponse, 1))}",
        ),
        Etape(
            "Vérifier",
            f"Pour ${var} = {L(int(reponse) + 100)}$ : recette "
            f"{_fr(recette * (int(reponse) + 100), 0)} €, coût "
            f"{_fr(fixe + variable * (int(reponse) + 100), 0)} € — bénéficiaire. ✓ "
            f"Pour ${var} = {L(int(reponse) - 100)}$, la situation s'inverse. ✓",
        ),
        Etape(
            "Interpréter — la marge unitaire",
            f"Le nombre ${L(marge)}$ qui apparaît au dénominateur est la **marge "
            f"unitaire** : ce que chaque vente laisse une fois son coût variable "
            f"couvert. Il faut environ {_fr(reponse, 0)} ventes pour que ces marges "
            f"cumulées absorbent les {_fr(fixe, 0)} € de coûts fixes. Cette lecture — "
            "coût fixe divisé par marge unitaire — est le calcul de seuil de "
            "rentabilité standard.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Borne (nombre de ventes)",
        tolerance=0.005,
        indice=f"Rassemblez les termes en ${var}$ d'un côté : que reste-t-il comme "
        "coefficient ?",
        pieges=[
            (
                float(fixe) / recette,
                "Vous avez divisé par la recette unitaire au lieu de la **marge**. "
                f"Chaque vente ne laisse que {_fr(marge)} € une fois son coût variable "
                "payé.",
            ),
            (
                float(fixe) / variable,
                "Vous avez divisé par le coût variable unitaire. C'est l'écart entre "
                "recette et coût variable qui compte.",
            ),
            (
                float(fixe) / (recette + variable),
                "Les deux montants se **soustraient** : on cherche ce que rapporte "
                "chaque vente net de son coût.",
            ),
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
