"""Série P5 — Pourcentages, indices et évolutions. Fil rouge C : le logement étudiant.

Variation sur trois axes (cf. `contextes.py`) : le contexte (loyers, budgets,
effectifs), la notation et la **forme** de la donnée — un effectif et un total,
deux effectifs dont il faut reconstituer la base, un taux, un coefficient
multiplicateur, ou un indice. La même question, posée de cinq manières.
"""

import random

import streamlit as st

from contextes import latex_nombre as L
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

### ⚠️ Repérez la base avant de calculer
Un énoncé peut vous donner un effectif et un total, **deux effectifs** dont la somme
fait le total, un taux, un coefficient ou un indice. La première question est
toujours la même : **sur quoi porte le pourcentage ?**
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

#: (population de référence, sous-groupe, complémentaire du sous-groupe)
POPULATIONS = [
    ("les inscrits sur les listes électorales", "votants", "abstentionnistes"),
    ("les ménages du quartier", "locataires", "propriétaires"),
    ("les étudiants de la promotion", "boursiers", "non-boursiers"),
    ("les logements du parc social", "logements rénovés", "logements anciens"),
    ("les usagers de la médiathèque", "abonnés annuels", "abonnés ponctuels"),
    ("les salariés de la collectivité", "agents titulaires", "agents contractuels"),
]

#: Grandeurs suivies dans le temps, pour les évolutions et les indices.
SUIVIES = [
    ("le loyer moyen d'un studio", "€", [560, 580, 600, 620, 650, 680]),
    ("le budget de la médiathèque", "k€", [120, 150, 180, 240]),
    ("le prix du ticket de bus", "€", [2, 3, 4]),
    ("la fréquentation de la piscine", "entrées", [8_000, 12_000, 15_000]),
    ("le montant de la bourse mensuelle", "€", [340, 420, 480]),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


# --- 1. Proportion, part, pourcentage ---------------------------------------


def gen_proportion() -> Exercice:
    base, groupe, complement = random.choice(POPULATIONS)
    total = random.choice([250, 400, 500, 800, 1250, 1600, 2500])
    part = random.choice([0.12, 0.16, 0.24, 0.35, 0.44, 0.52, 0.68])
    effectif = int(round(total * part))
    reponse = 100 * effectif / total
    presentation = random.choice(["effectif_total", "deux_groupes", "fraction"])

    if presentation == "effectif_total":
        enonce = f"""
> Sur **{_fr(total, 0)}** personnes parmi {base}, **{_fr(effectif, 0)}** sont des
> {groupe}.
>
> Quel **pourcentage** cela représente-t-il ?
"""
        reperage = (
            f"La base est le **total** : {_fr(total, 0)} personnes. Elle est donnée "
            "telle quelle."
        )
    elif presentation == "deux_groupes":
        enonce = f"""
> Parmi {base}, on compte **{_fr(effectif, 0)}** {groupe} et
> **{_fr(total - effectif, 0)}** {complement}.
>
> Quel **pourcentage** les {groupe} représentent-ils ?
"""
        reperage = (
            f"Le total n'est pas donné : il faut le **reconstituer** en additionnant "
            f"les deux groupes, soit {_fr(effectif, 0)} + "
            f"{_fr(total - effectif, 0)} = {_fr(total, 0)}. C'est l'erreur la plus "
            "fréquente de cet exercice : diviser par l'autre groupe au lieu du total."
        )
    else:
        enonce = f"""
> Parmi {base}, la part des {groupe} s'écrit
>
> $$ \\frac{{{effectif}}}{{{total}}} $$
>
> Exprimez cette part en **pourcentage**.
"""
        reperage = (
            f"La fraction est déjà écrite : son dénominateur ${total}$ **est** la "
            "base. Il ne reste qu'à convertir en pourcentage."
        )

    etapes = [
        Etape(
            "Identifier — pourcentage de quoi ?",
            f"{reperage} Un pourcentage n'existe jamais seul : il porte toujours sur "
            "une base, et identifier cette base est la moitié du travail.",
        ),
        Etape(
            "Calculer — proportion puis multiplication par 100",
            "La proportion est un nombre entre 0 et 1 ; le pourcentage est la même "
            "information exprimée sur 100.",
            rf"\frac{{{effectif}}}{{{total}}} = {L(round(effectif / total, 4))} "
            rf"\qquad\Rightarrow\qquad {L(round(reponse, 2))}\,\%",
        ),
        Etape(
            "Vérifier — l'encadrement de bon sens",
            f"Le résultat doit être compris entre 0 et 100, et se situer du bon côté "
            f"de 50 : ici {_fr(effectif, 0)} est "
            f"{'inférieur' if effectif < total / 2 else 'supérieur'} à la moitié de "
            f"{_fr(total, 0)}. ✓",
        ),
        Etape(
            "Interpréter — deux façons de dire la même chose",
            f"« {_fr(effectif, 0)} {groupe} » et « {_fr(reponse, 1)} % » décrivent le "
            "même fait, mais ne servent pas à la même chose : le premier chiffre "
            "donne un **effectif**, le second permet de **comparer** avec une "
            "population de taille différente.",
        ),
    ]

    pieges = [
        (
            100 * total / effectif,
            "Vous avez divisé le **total par la partie**. Un pourcentage de ce type "
            "ne peut pas dépasser 100.",
        ),
        (
            effectif / total,
            "Vous avez calculé la proportion sans la multiplier par 100 : bon nombre, "
            "mauvaise unité.",
        ),
    ]
    if presentation == "deux_groupes":
        pieges.append(
            (
                100 * effectif / (total - effectif),
                f"Vous avez divisé par l'**autre groupe** au lieu du total. La base "
                f"est l'ensemble des personnes, soit {_fr(total, 0)}.",
            )
        )

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Pourcentage",
        unite="%",
        tolerance=0.01,
        indice="Partie divisée par total, puis × 100. Mais quel est le total ?",
        pieges=pieges,
    )


# --- 2. Point de pourcentage ou pourcentage ? ------------------------------


def gen_points() -> Exercice:
    base, groupe, _ = random.choice(POPULATIONS)
    t1 = random.choice([4, 5, 6, 8, 10, 12, 15, 20])
    ecart = random.choice([1, 2, 3, 4, 5])
    t2 = t1 + ecart
    reponse = 100 * ecart / t1
    presentation = random.choice(["deux_taux", "taux_et_points"])

    if presentation == "deux_taux":
        enonce = f"""
> La part des {groupe} parmi {base} est passée de **{t1} %** à **{t2} %** en cinq
> ans.
>
> De combien cette part a-t-elle augmenté **en pourcentage** (variation relative) ?
>
> *La question ne porte pas sur la variation en points de pourcentage.*
"""
        lecture = (
            f"L'écart brut vaut ${t2} - {t1} = {ecart}$ **points de pourcentage**. "
            "Mais la variation **relative** rapporte cet écart à la valeur de départ : "
            f"la base n'est plus 100, c'est **{t1}**."
        )
    else:
        enonce = f"""
> La part des {groupe} parmi {base} était de **{t1} %**. Elle a gagné
> **{ecart} point{'s' if ecart > 1 else ''} de pourcentage** en cinq ans.
>
> De combien cette part a-t-elle augmenté **en pourcentage** (variation relative) ?
"""
        lecture = (
            f"L'énoncé donne directement l'écart en points : ${ecart}$. La part "
            f"d'arrivée vaut donc ${t1} + {ecart} = {t2}$ %. La variation "
            f"**relative**, elle, rapporte l'écart à la valeur de départ, soit "
            f"**{t1}** — et non à 100."
        )

    etapes = [
        Etape("Identifier — deux façons de mesurer le même écart", lecture),
        Etape(
            "Calculer la variation relative",
            "",
            rf"\frac{{{t2} - {t1}}}{{{t1}}} \times 100 = "
            rf"\frac{{{ecart}}}{{{t1}}} \times 100 = {L(round(reponse, 2))}\,\%",
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
            (
                float(ecart),
                "Vous avez donné la variation en **points de pourcentage**. La "
                f"question portait sur la variation relative, dont la base est {t1} %.",
            ),
            (
                100 * ecart / t2,
                "Vous avez divisé par la valeur d'**arrivée**. Une variation se "
                "rapporte toujours à la valeur de départ.",
            ),
        ],
    )


# --- 3. Évolutions successives ----------------------------------------------


def gen_successives() -> Exercice:
    grandeur, unite, valeurs = random.choice(SUIVIES)
    depart = random.choice(valeurs)
    t1 = random.choice([3, 5, 7, 9])
    t2 = random.choice([-4, -2, 2, 4])
    cm1, cm2 = 1 + t1 / 100, 1 + t2 / 100
    presentation = random.choice(["deux_taux", "taux_et_coefficient", "trois_taux"])

    if presentation == "trois_taux":
        t3 = random.choice([-3, 1, 6])
        cm3 = 1 + t3 / 100
        cm = cm1 * cm2 * cm3
        description = (
            f"**{t1:+} %** la première année, **{t2:+} %** la deuxième, puis "
            f"**{t3:+} %** la troisième"
        )
        coefficients = (
            rf"CM_1 = {L(cm1)} \quad CM_2 = {L(cm2)} \quad CM_3 = {L(cm3)} "
            rf"\quad CM_{{\text{{global}}}} = {L(round(cm, 6))}"
        )
        somme_naive = t1 + t2 + t3
    elif presentation == "taux_et_coefficient":
        cm = cm1 * cm2
        description = (
            f"**{t1:+} %** la première année, puis une évolution de coefficient "
            f"multiplicateur **{L(cm2)}** la deuxième"
        )
        coefficients = (
            rf"CM_1 = {L(cm1)} \quad CM_2 = {L(cm2)} "
            rf"\quad CM_{{\text{{global}}}} = {L(cm1)} \times {L(cm2)} "
            rf"= {L(round(cm, 6))}"
        )
        somme_naive = t1 + t2
    else:
        cm = cm1 * cm2
        description = f"**{t1:+} %** la première année, puis **{t2:+} %** la deuxième"
        coefficients = (
            rf"CM_1 = {L(cm1)} \quad CM_2 = {L(cm2)} "
            rf"\quad CM_{{\text{{global}}}} = {L(cm1)} \times {L(cm2)} "
            rf"= {L(round(cm, 6))}"
        )
        somme_naive = t1 + t2

    reponse = depart * cm
    taux_global = (cm - 1) * 100

    enonce = f"""
> Au départ, {grandeur} s'élevait à **{_fr(depart, 0)} {unite}**. Les
> évolutions constatées sont ensuite de {description}.
>
> Quelle est sa valeur à l'arrivée ? Arrondissez au centième.
"""

    etapes = [
        Etape(
            "Identifier — les taux ne s'additionnent pas",
            f"La tentation est d'écrire une somme de taux (${somme_naive:+}$ %). "
            "C'est faux : chaque évolution porte sur la valeur **déjà modifiée** par "
            "la précédente, pas sur la valeur de départ.",
        ),
        Etape(
            "Passer par les coefficients",
            "Chaque taux devient un coefficient ($CM = 1 + t/100$), et les "
            "coefficients se **multiplient**. Un coefficient déjà donné se reporte "
            "tel quel.",
            coefficients,
        ),
        Etape(
            "Appliquer à la valeur de départ",
            "",
            rf"{L(depart)} \times {L(round(cm, 6))} \approx {L(round(reponse, 2))}"
            rf"\ \text{{{unite}}}",
        ),
        Etape(
            "Vérifier — année par année",
            f"Première année : ${L(depart)} \\times {L(cm1)} = "
            f"{L(round(depart * cm1, 2))}$. Puis on repart de ce montant pour "
            "l'évolution suivante. ✓ Les deux chemins donnent le même résultat, ce qui "
            "est la meilleure confirmation que la multiplication était la bonne "
            "opération.",
        ),
        Etape(
            "Interpréter — le taux global",
            f"L'évolution globale vaut ${L(round(taux_global, 2))}$ %, et non "
            f"${somme_naive:+}$ %. L'écart est faible sur deux ou trois ans, mais il "
            "ne s'annule jamais et s'accumule : sur une série longue, additionner les "
            "taux conduit à des conclusions franchement fausses.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur à l'arrivée",
        unite=unite,
        tolerance=0.002,
        indice="Convertissez chaque taux en coefficient, puis multipliez.",
        pieges=[
            (
                depart * (1 + somme_naive / 100),
                "Vous avez **additionné les taux**. Chaque évolution porte sur une "
                "valeur déjà modifiée par la précédente.",
            ),
            (
                depart * cm1,
                "Vous vous êtes arrêté à la première évolution : il en reste au moins "
                "une à appliquer.",
            ),
        ],
    )


# --- 4. Évolution réciproque -----------------------------------------------


def gen_reciproque() -> Exercice:
    grandeur, unite, _ = random.choice(SUIVIES)
    sens = random.choice(["hausse", "baisse"])
    taux = random.choice([10, 20, 25, 40, 50])
    signe = 1 if sens == "hausse" else -1
    cm = 1 + signe * taux / 100
    cm_r = 1 / cm
    reponse = (cm_r - 1) * 100
    presentation = random.choice(["taux", "coefficient"])

    if presentation == "taux":
        description = f"une **{sens} de {taux} %**"
    else:
        description = (
            f"une évolution de **coefficient multiplicateur {L(cm)}** "
            f"(soit une {sens} de {taux} %)"
        )

    enonce = f"""
> {_maj(grandeur)} a connu {description}.
>
> Quel taux faudrait-il appliquer ensuite pour **revenir exactement à la valeur de
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
            rf"CM = {L(cm)} \qquad CM_r = \frac{{1}}{{{L(cm)}}} "
            rf"= {L(round(cm_r, 6))}",
        ),
        Etape(
            "Revenir au taux",
            "",
            rf"t_r = ({L(round(cm_r, 6))} - 1) \times 100 \approx "
            rf"{L(round(reponse, 2))}\,\%",
        ),
        Etape(
            "Vérifier — enchaîner les deux coefficients",
            f"${L(cm)} \\times {L(round(cm_r, 6))} = 1$ : on retrouve exactement la "
            "valeur initiale. ✓ C'est la définition même de la réciproque.",
        ),
        Etape(
            "Interpréter — une asymétrie aux effets concrets",
            f"Une {sens} de {taux} % s'annule par une évolution de "
            f"${L(round(reponse, 2))}$ %, et non de ${-signe * taux}$ %. Une baisse de budget "
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
            (
                float(-signe * taux),
                "Vous avez pris le **taux opposé**. Les deux taux ne s'appliquent pas "
                "à la même base : il faut passer par l'inverse du coefficient.",
            ),
            (
                cm_r,
                "Vous avez donné le **coefficient** réciproque, pas le taux. "
                "Il reste $(CM_r - 1) \\times 100$.",
            ),
        ],
    )


# --- 5. Indice base 100 -----------------------------------------------------


def gen_indice() -> Exercice:
    grandeur, unite, valeurs = random.choice(
        [suivie for suivie in SUIVIES if max(suivie[2]) >= 100]
    )
    ref = random.choice(valeurs)
    annee_ref = random.choice([2015, 2018, 2020])
    annee = annee_ref + random.choice([3, 5, 8, 10])
    variation = random.choice([-0.12, -0.05, 0.08, 0.15, 0.23, 0.34])
    valeur = round(ref * (1 + variation))
    reponse = 100 * valeur / ref
    presentation = random.choice(["deux_valeurs", "evolution"])

    if presentation == "deux_valeurs":
        enonce = f"""
> En **{annee_ref}**, année choisie comme **référence (indice 100)**,
> {grandeur} s'élevait à **{_fr(ref, 0)} {unite}**. En **{annee}**, sa valeur
> est de **{_fr(valeur, 0)} {unite}**.
>
> Quel est l'**indice** en {annee} ? Arrondissez au dixième.
"""
        lecture = (
            "Les deux valeurs sont données : l'indice est leur rapport, ramené à 100."
        )
    else:
        evolution = 100 * (valeur / ref - 1)
        enonce = f"""
> Entre **{annee_ref}** (année de référence, indice 100) et **{annee}**,
> {grandeur} a évolué de **{_fr(evolution, 1)} %**.
>
> Quel est l'**indice** en {annee} ? Arrondissez au dixième.
"""
        lecture = (
            f"Aucune valeur en {unite} n'est nécessaire : une évolution de "
            f"{_fr(evolution, 1)} % correspond au coefficient "
            f"${L(round(valeur / ref, 4))}$, et l'indice est ce coefficient "
            "multiplié par 100. C'est la lecture directe : indice = 100 + évolution "
            "en pourcentage."
        )

    etapes = [
        Etape(
            "Identifier — un indice est un rapport ramené à 100",
            f"{lecture} L'année de référence reçoit l'indice 100 par convention ; "
            "toute autre année est comparée à elle.",
            r"I = \frac{V_{\text{année}}}{V_{\text{référence}}} \times 100",
        ),
        Etape(
            "Calculer",
            "",
            rf"I_{{{annee}}} = \frac{{{L(valeur)}}}{{{L(ref)}}} \times 100 "
            rf"\approx {L(round(reponse, 1))}",
        ),
        Etape(
            "Vérifier — lire l'indice comme une évolution",
            f"Un indice de ${L(round(reponse, 1))}$ signifie une évolution de "
            f"**{_fr(reponse - 100, 1)} %** depuis {annee_ref}. C'est la lecture "
            "directe de l'indice : il suffit de retrancher 100. "
            f"Contrôle : ${L(ref)} \\times {L(round(reponse / 100, 4))} \\approx "
            f"{L(valeur)}$. ✓",
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
            (
                100 * ref / valeur,
                "Vous avez inversé le rapport : la valeur de l'**année étudiée** va au "
                "numérateur, celle de l'année de référence au dénominateur.",
            ),
            (
                reponse - 100,
                "Vous avez donné l'**évolution en pourcentage**, qui est l'indice "
                "moins 100. L'indice lui-même est proche de 100, pas de 0.",
            ),
            (
                float(valeur - ref),
                "C'est l'écart en valeur absolue, pas un indice. Un indice est sans "
                "unité.",
            ),
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
    st.subheader("Enchaîner des évolutions")
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
