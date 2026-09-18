"""Série P5 — Pourcentages, indices et évolutions. Fil rouge C : le logement étudiant."""

import random

import streamlit as st

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P5 | Pourcentages et indices", page_icon="％", layout="wide")

st.title("％ P5 — Pourcentages, indices et évolutions")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Passer d'une proportion à un pourcentage, traduire un taux en **coefficient
multiplicateur**, enchaîner des évolutions, revenir en arrière, et lire un **indice
base 100**.

### 🧠 L'idée centrale
Les taux **ne s'additionnent pas**, les coefficients **se multiplient**. Une hausse de
7 % suivie d'une baisse de 2 % ne donne pas +5 %. Toute la séance tient dans cette
phrase, et les trois pièges qu'elle engendre.

### 🏠 Fil rouge C — Le logement étudiant
Le loyer moyen d'un studio à Villeneuve valait **620 €** en 2023. Il a évolué de
**+7 %** en 2024, puis de **−2 %** en 2025.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 5")
    st.latex(r"\text{pourcentage} = \frac{\text{partie}}{\text{total}} \times 100")
    st.markdown("**Coefficient multiplicateur**")
    st.latex(r"CM = 1 + \frac{t}{100} \qquad t = (CM - 1) \times 100")
    st.markdown("**Évolutions successives**")
    st.latex(r"CM_{\text{global}} = CM_1 \times CM_2")
    st.markdown("**Évolution réciproque**")
    st.latex(r"CM_r = \frac{1}{CM}")
    st.markdown("**Indice base 100**")
    st.latex(r"I = \frac{V_{\text{année}}}{V_{\text{référence}}} \times 100")
    st.error(
        "**Les trois pièges**\n\n"
        "1. Additionner les taux au lieu de multiplier les coefficients.\n\n"
        "2. Confondre **point de pourcentage** et **pourcentage**.\n\n"
        "3. Croire qu'une baisse de $t$ % annule une hausse de $t$ %."
    )

POPULATIONS = [
    ("les inscrits sur les listes électorales", "votants"),
    ("les ménages du quartier", "locataires"),
    ("les étudiants de la promotion", "boursiers"),
    ("les logements du parc social", "logements rénovés"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Proportion, part, pourcentage ---------------------------------------


def gen_proportion() -> Exercice:
    base, sous_groupe = random.choice(POPULATIONS)
    total = random.choice([250, 400, 500, 800, 1250, 1600, 2500])
    part = random.choice([0.12, 0.16, 0.24, 0.35, 0.44, 0.52, 0.68])
    effectif = int(round(total * part))
    reponse = 100 * effectif / total

    enonce = f"""
> Sur **{total:,}** personnes parmi {base}, **{effectif:,}** sont des {sous_groupe}.
>
> Quel **pourcentage** cela représente-t-il ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — pourcentage de quoi ?",
            f"La base est le **total** : {total:,} personnes. Un pourcentage n'existe "
            "jamais seul, il porte toujours sur une base, et identifier cette base "
            "est la moitié du travail.".replace(",", "\u202f"),
        ),
        Etape(
            "Calculer — proportion puis multiplication par 100",
            "La proportion est un nombre entre 0 et 1 ; le pourcentage est la même "
            "information exprimée sur 100.",
            rf"\frac{{{effectif}}}{{{total}}} = {effectif/total:.4f} "
            rf"\qquad\Rightarrow\qquad {reponse:.2f}\,\%",
        ),
        Etape(
            "Vérifier — l'encadrement de bon sens",
            f"Le résultat doit être compris entre 0 et 100, et se situer du bon côté "
            f"de 50 : ici {effectif:,} est "
            f"{'inférieur' if effectif < total/2 else 'supérieur'} à la moitié de "
            f"{total:,}. ✓".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — deux façons de dire la même chose",
            f"« {effectif:,} {sous_groupe} » et « {_fr(reponse, 1)} % » décrivent le "
            "même fait, mais ne servent pas à la même chose : le premier chiffre "
            "donne un **effectif**, le second permet de **comparer** avec une "
            "population de taille différente.".replace(",", "\u202f"),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Pourcentage",
        unite="%",
        tolerance=0.01,
        indice="Partie divisée par total, puis × 100.",
        pieges=[
            (100 * total / effectif,
             "Vous avez divisé le **total par la partie**. Un pourcentage de ce type "
             "ne peut pas dépasser 100."),
            (effectif / total,
             "Vous avez calculé la proportion sans la multiplier par 100 : bon nombre, "
             "mauvaise unité."),
        ],
    )


# --- 2. Point de pourcentage ou pourcentage ? ------------------------------


def gen_points() -> Exercice:
    base, sous_groupe = random.choice(POPULATIONS)
    t1 = random.choice([4, 5, 6, 8, 10, 12, 15, 20])
    ecart = random.choice([1, 2, 3, 4, 5])
    t2 = t1 + ecart
    reponse = 100 * ecart / t1

    enonce = f"""
> La part des {sous_groupe} est passée de **{t1} %** à **{t2} %** en cinq ans.
>
> De combien cette part a-t-elle augmenté **en pourcentage** (variation relative) ?
>
> *La question ne porte pas sur la variation en points de pourcentage.*
"""

    etapes = [
        Etape(
            "Identifier — deux façons de mesurer le même écart",
            f"L'écart brut vaut ${t2} - {t1} = {ecart}$ **points de pourcentage**. "
            "Mais la variation **relative** rapporte cet écart à la valeur de départ : "
            f"la base n'est plus 100, c'est **{t1}**.",
        ),
        Etape(
            "Calculer la variation relative",
            "",
            rf"\frac{{{t2} - {t1}}}{{{t1}}} \times 100 = "
            rf"\frac{{{ecart}}}{{{t1}}} \times 100 = {reponse:.2f}\,\%",
        ),
        Etape(
            "Vérifier — l'écart entre les deux nombres est normal",
            f"Une hausse de {ecart} points sur une base de {t1} % donne "
            f"**{_fr(reponse, 1)} %** d'augmentation relative. Le fossé entre les deux "
            "chiffres est précisément ce qui rend la distinction importante.",
        ),
        Etape(
            "Interpréter — pourquoi les deux chiffres circulent",
            f"Un communiqué qui veut minimiser dira « +{ecart} points » ; un "
            f"communiqué qui veut alerter dira « +{_fr(reponse, 1)} % ». Les deux "
            "sont exacts. Savoir lequel est employé, et sur quelle base, relève de "
            "la lecture critique autant que du calcul.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Variation relative",
        unite="%",
        tolerance=0.01,
        indice="La base de comparaison est la valeur de départ, pas 100.",
        pieges=[
            (float(ecart),
             "Vous avez donné la variation en **points de pourcentage**. La question "
             f"portait sur la variation relative, dont la base est {t1} %."),
            (100 * ecart / t2,
             "Vous avez divisé par la valeur d'**arrivée**. Une variation se rapporte "
             "toujours à la valeur de départ."),
        ],
    )


# --- 3. Évolutions successives (fil rouge) ---------------------------------


def gen_successives() -> Exercice:
    loyer = random.choice([560, 580, 600, 620, 650, 680])
    t1 = random.choice([3, 5, 7, 9])
    t2 = random.choice([-4, -2, 2, 4])
    cm1, cm2 = 1 + t1 / 100, 1 + t2 / 100
    cm = cm1 * cm2
    reponse = loyer * cm
    taux_global = (cm - 1) * 100

    enonce = f"""
> **Logement étudiant.** Le loyer moyen d'un studio à Villeneuve valait
> **{loyer} €** en 2023. Il a évolué de **{t1:+} %** en 2024, puis de
> **{t2:+} %** en 2025.
>
> Quel est le loyer moyen en 2025 ? Arrondissez au centime.
"""

    etapes = [
        Etape(
            "Identifier — les taux ne s'additionnent pas",
            f"La tentation est d'écrire ${t1} + ({t2}) = {t1 + t2}$ %. C'est faux : "
            "la seconde évolution ne porte pas sur le loyer de 2023, mais sur celui "
            "de 2024, **déjà modifié** par la première.",
        ),
        Etape(
            "Passer par les coefficients",
            "Chaque taux devient un coefficient, et les coefficients se multiplient.",
            rf"CM_1 = {cm1:.4g} \qquad CM_2 = {cm2:.4g} \qquad "
            rf"CM_{{\text{{global}}}} = {cm1:.4g} \times {cm2:.4g} = {cm:.6g}",
        ),
        Etape(
            "Appliquer au loyer de départ",
            "",
            rf"{loyer} \times {cm:.6g} \approx {reponse:.2f}\ \text{{€}}",
        ),
        Etape(
            "Vérifier — année par année",
            f"2024 : ${loyer} \\times {cm1:.4g} = {loyer*cm1:.2f}$ €. "
            f"2025 : ${loyer*cm1:.2f} \\times {cm2:.4g} \\approx {reponse:.2f}$ €. ✓ "
            "Les deux chemins donnent le même résultat, ce qui est la meilleure "
            "confirmation que la multiplication était la bonne opération.",
        ),
        Etape(
            "Interpréter — le taux global",
            f"L'évolution globale vaut ${_fr(taux_global)}$ %, et non "
            f"${t1 + t2}$ %. L'écart est faible sur deux ans, mais il ne s'annule "
            "jamais et s'accumule : sur une série longue, additionner les taux "
            "conduit à des conclusions franchement fausses.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Loyer en 2025",
        unite="€",
        tolerance=0.002,
        indice="Convertissez chaque taux en coefficient, puis multipliez.",
        pieges=[
            (loyer * (1 + (t1 + t2) / 100),
             "Vous avez **additionné les taux**. La seconde évolution porte sur un "
             "loyer déjà modifié par la première."),
            (loyer * cm1,
             "Vous vous êtes arrêté à 2024 : il reste une évolution à appliquer."),
        ],
    )


# --- 4. Évolution réciproque -----------------------------------------------


def gen_reciproque() -> Exercice:
    sens = random.choice(["hausse", "baisse"])
    taux = random.choice([10, 20, 25, 40, 50])
    signe = 1 if sens == "hausse" else -1
    cm = 1 + signe * taux / 100
    cm_r = 1 / cm
    reponse = (cm_r - 1) * 100

    enonce = f"""
> Le loyer moyen a connu une **{sens} de {taux} %**.
>
> Quel taux faudrait-il appliquer ensuite pour **revenir exactement au loyer de
> départ** ? Donnez ce taux en pourcentage (négatif pour une baisse).
"""

    etapes = [
        Etape(
            "Identifier — la réciproque n'est pas le taux opposé",
            f"Après une {sens} de {taux} %, appliquer "
            f"{'−' if signe > 0 else '+'}{taux} % ne ramène **pas** au point de "
            "départ : le second taux s'appliquerait à une base différente de la "
            "première.",
        ),
        Etape(
            "Utiliser $CM_r = \\dfrac{1}{CM}$",
            "Revenir en arrière, c'est annuler la multiplication : le coefficient "
            "réciproque est l'inverse.",
            rf"CM = {cm:.4g} \qquad CM_r = \frac{{1}}{{{cm:.4g}}} = {cm_r:.6g}",
        ),
        Etape(
            "Revenir au taux",
            "",
            rf"t_r = ({cm_r:.6g} - 1) \times 100 \approx {reponse:.2f}\,\%",
        ),
        Etape(
            "Vérifier — enchaîner les deux coefficients",
            f"${cm:.4g} \\times {cm_r:.6g} = 1$ : on retrouve exactement la valeur "
            "initiale. ✓ C'est la définition même de la réciproque.",
        ),
        Etape(
            "Interpréter — une asymétrie aux effets concrets",
            f"Une {sens} de {taux} % s'annule par une évolution de "
            f"${_fr(reponse)}$ %, et non de ${-signe*taux}$ %. Une baisse de budget "
            "de 20 % exige une hausse de 25 % pour être rattrapée : l'asymétrie n'est "
            "pas une curiosité mathématique, c'est un argument de négociation.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux de retour",
        unite="%",
        tolerance=0.01,
        indice="Le coefficient qui annule une multiplication est son inverse.",
        pieges=[
            (float(-signe * taux),
             "Vous avez pris le **taux opposé**. Les deux taux ne s'appliquent pas à "
             "la même base : il faut passer par l'inverse du coefficient."),
            (cm_r,
             "Vous avez donné le **coefficient** réciproque, pas le taux. "
             "Il reste $(CM_r - 1) \\times 100$."),
        ],
    )


# --- 5. Indice base 100 -----------------------------------------------------


def gen_indice() -> Exercice:
    ref = random.choice([520, 580, 620, 700, 750])
    annee_ref = random.choice([2015, 2018, 2020])
    annee = annee_ref + random.choice([3, 5, 8, 10])
    variation = random.choice([-0.12, -0.05, 0.08, 0.15, 0.23, 0.34])
    valeur = round(ref * (1 + variation))
    reponse = 100 * valeur / ref

    enonce = f"""
> Le loyer moyen d'un studio valait **{ref} €** en **{annee_ref}**, année choisie
> comme **référence (indice 100)**. En **{annee}**, il vaut **{valeur} €**.
>
> Quel est l'**indice** du loyer en {annee} ? Arrondissez au dixième.
"""

    etapes = [
        Etape(
            "Identifier — un indice est un rapport ramené à 100",
            f"L'année de référence reçoit l'indice 100 par convention. Toute autre "
            "année est comparée à elle, et l'indice exprime ce rapport sur une base "
            "de 100 — jamais sur la valeur elle-même.",
            r"I = \frac{V_{\text{année}}}{V_{\text{référence}}} \times 100",
        ),
        Etape(
            "Calculer",
            "",
            rf"I_{{{annee}}} = \frac{{{valeur}}}{{{ref}}} \times 100 "
            rf"\approx {reponse:.1f}",
        ),
        Etape(
            "Vérifier — lire l'indice comme une évolution",
            f"Un indice de ${_fr(reponse, 1)}$ signifie une évolution de "
            f"**{_fr(reponse - 100, 1)} %** depuis {annee_ref}. C'est la lecture "
            "directe de l'indice : il suffit de retrancher 100. "
            f"Contrôle : ${ref} \\times {reponse/100:.4f} \\approx {valeur}$ €. ✓",
        ),
        Etape(
            "Interpréter — pourquoi les sciences sociales utilisent des indices",
            "Un indice permet de comparer des séries exprimées dans des unités "
            "différentes — un loyer en euros, une fréquentation en visites, un salaire "
            "en euros courants — en les ramenant toutes à une même base. "
            "C'est la seule façon de mettre plusieurs évolutions sur un même "
            "graphique sans que l'échelle écrase les plus petites.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Indice en {annee}",
        tolerance=0.002,
        indice="Rapport à l'année de référence, multiplié par 100.",
        pieges=[
            (100 * ref / valeur,
             "Vous avez inversé le rapport : la valeur de l'**année étudiée** va au "
             "numérateur, celle de l'année de référence au dénominateur."),
            (reponse - 100,
             "Vous avez donné l'**évolution en pourcentage**, qui est l'indice moins "
             "100. L'indice lui-même est proche de 100, pas de 0."),
            (float(valeur - ref),
             "C'est l'écart en euros, pas un indice. Un indice est sans unité."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Proportion et pourcentage",
        "2️⃣ Points ou pourcents ?",
        "3️⃣ Évolutions successives",
        "4️⃣ Revenir en arrière",
        "5️⃣ Indices base 100",
    ]
)

with onglets[0]:
    st.subheader("Exprimer une part en pourcentage")
    executer("p5_proportion", gen_proportion)

with onglets[1]:
    st.subheader("Point de pourcentage contre variation relative")
    executer("p5_points", gen_points)

with onglets[2]:
    st.subheader("Enchaîner deux évolutions")
    executer("p5_successives", gen_successives)

with onglets[3]:
    st.subheader("L'évolution réciproque")
    executer("p5_reciproque", gen_reciproque)

with onglets[4]:
    st.subheader("Lire et calculer un indice")
    executer("p5_indice", gen_indice)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°5 — Pourcentages, indices et évolutions · "
    "Fil rouge C : le logement étudiant · Sciences Po."
)
