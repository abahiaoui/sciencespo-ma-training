"""Série P3 — Proportions et pourcentages."""

import random

import streamlit as st

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P3 | Proportions et pourcentages", page_icon="％", layout="wide")

st.title("％ P3 — Proportions et pourcentages")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Transformer une proportion en pourcentage et inversement, appliquer un taux à un
effectif, remonter d'une part au total, et surtout **distinguer un point de
pourcentage d'un pourcentage** — la confusion la plus coûteuse de tout le module.

### 🧠 La question à se poser avant chaque calcul
« Pourcentage **de quoi** ? » Un pourcentage n'existe jamais seul : il porte sur une
base. Identifier cette base est la moitié du travail, et c'est elle qui change entre
une hausse « de 2 points » et une hausse « de 2 % ».
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 3")
    st.latex(r"\text{proportion} = \frac{\text{partie}}{\text{total}}")
    st.latex(r"\text{pourcentage} = \frac{\text{partie}}{\text{total}} \times 100")
    st.latex(r"p\,\%\ \text{de}\ X = \frac{p}{100} \times X")
    st.latex(r"\text{total} = \frac{\text{partie}}{p} \times 100")
    st.error(
        "**Point de pourcentage ≠ pourcentage**\n\n"
        "Passer de 8 % à 10 %, c'est :\n\n"
        "- **+2 points** de pourcentage\n"
        "- **+25 %** en variation relative"
    )
    st.info(
        "**Le réflexe**\n\n"
        "Avant tout calcul, demandez-vous : *pourcentage de quoi ?* "
        "La base change le résultat."
    )

POPULATIONS = [
    ("les inscrits sur les listes électorales", "votants"),
    ("les salariés d'une entreprise", "cadres"),
    ("les ménages d'un quartier", "locataires"),
    ("les étudiants d'une promotion", "boursiers"),
    ("les communes d'un département", "communes rurales"),
]

RUBRIQUES = ["éducation", "action sociale", "transports", "culture", "sécurité"]


def _fr(x: float, n: int = 1) -> str:
    return f"{x:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Proportion vers pourcentage ----------------------------------------


def gen_proportion() -> Exercice:
    total_base, sous_groupe = random.choice(POPULATIONS)
    total = random.choice([250, 400, 500, 800, 1250, 1600, 2500])
    part = random.choice([0.12, 0.16, 0.24, 0.35, 0.44, 0.52, 0.68])
    effectif = int(round(total * part))
    reponse = 100 * effectif / total

    enonce = f"""
> Sur **{total:,} personnes** dans {total_base}, **{effectif:,}** sont des
> {sous_groupe}.
>
> Quel **pourcentage** cela représente-t-il ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — quelle est la base ?",
            f"La base est le **total** : {total:,} personnes. Le pourcentage cherché "
            f"répond à la question « quelle part de ce total les {sous_groupe} "
            "représentent-ils ? »".replace(",", "\u202f"),
        ),
        Etape(
            "Calculer — proportion puis multiplication par 100",
            "On divise la partie par le total, ce qui donne une proportion entre 0 et "
            "1, puis on multiplie par 100 pour l'exprimer en pourcentage.",
            rf"\frac{{{effectif}}}{{{total}}} = {effectif/total:.4f}"
            rf"\qquad\Rightarrow\qquad {effectif/total:.4f} \times 100 "
            rf"= {reponse:.1f}\,\%",
        ),
        Etape(
            "Vérifier — l'encadrement de bon sens",
            f"Le résultat doit être compris entre 0 et 100, et se situer du bon côté "
            f"de 50 : ici {effectif:,} est "
            f"{'inférieur' if effectif < total/2 else 'supérieur'} à la moitié de "
            f"{total:,}, donc le pourcentage doit être "
            f"{'inférieur' if effectif < total/2 else 'supérieur'} à 50 %. "
            f"C'est bien le cas ({_fr(reponse)} %).".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter",
            f"Dire « {effectif:,} {sous_groupe} » et dire « {_fr(reponse)} % » n'a pas "
            "le même usage : le premier chiffre décrit un **effectif**, le second "
            "permet de **comparer** avec une autre population de taille différente. "
            "C'est précisément pour cela que les pourcentages existent.".replace(",", "\u202f"),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Pourcentage",
        unite="%",
        tolerance=0.01,
        indice="Divisez la partie par le total, puis multipliez par 100.",
        pieges=[
            (100 * total / effectif,
             "Vous avez divisé le **total par la partie**. La partie va toujours au "
             "numérateur : un pourcentage de ce type ne peut pas dépasser 100."),
            (effectif / total,
             "Vous avez calculé la proportion mais oublié de multiplier par 100. "
             "C'est le bon nombre dans la mauvaise unité."),
        ],
    )


# --- 2. Appliquer un pourcentage -------------------------------------------


def gen_appliquer() -> Exercice:
    rubrique = random.choice(RUBRIQUES)
    budget = random.choice([120, 180, 240, 300, 360, 450])
    taux = random.choice([8, 12, 15, 18, 22, 25, 35])
    reponse = budget * taux / 100

    enonce = f"""
> Le budget annuel d'une collectivité s'élève à **{budget} millions d'euros**.
> La rubrique **{rubrique}** en représente **{taux} %**.
>
> Quel montant, en millions d'euros, cette rubrique représente-t-elle ?
"""

    etapes = [
        Etape(
            "Identifier — un pourcentage est une multiplication",
            f"« {taux} % de » signifie « multiplié par $\\frac{{{taux}}}{{100}}$ ». "
            "Appliquer un taux n'est jamais une addition ni une division.",
        ),
        Etape(
            "Calculer",
            "",
            rf"\frac{{{taux}}}{{100}} \times {budget} = {taux/100} \times {budget} "
            rf"= {reponse:.2f}\ \text{{M€}}",
        ),
        Etape(
            "Vérifier — l'ancrage à 10 %",
            f"10 % de {budget} vaut {budget/10:g}. Comme {taux} % est "
            f"{'inférieur' if taux < 10 else 'supérieur'} à 10 %, le résultat doit "
            f"être {'inférieur' if taux < 10 else 'supérieur'} à {budget/10:g}. "
            f"C'est le cas ({_fr(reponse, 2)}). Ce repère mental détecte "
            "immédiatement une erreur de facteur 10.",
        ),
        Etape(
            "Interpréter",
            f"Les {_fr(reponse, 2)} M€ de la rubrique {rubrique} ne prennent leur sens "
            "qu'en comparaison : avec l'an dernier, avec une autre collectivité, ou "
            "rapportés au nombre d'habitants. Un montant seul ne dit presque rien.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Montant de la rubrique",
        unite="M€",
        tolerance=0.005,
        indice=f"« {taux} % de X » veut dire « X multiplié par {taux}/100 ».",
        pieges=[
            (budget * taux,
             "Vous avez multiplié par le taux sans le diviser par 100. Un pourcentage "
             "s'applique toujours divisé par 100."),
            (budget / taux,
             "Vous avez divisé au lieu de multiplier. Appliquer un taux, c'est "
             "multiplier."),
            (budget - budget * taux / 100,
             "Vous avez calculé ce qui **reste** une fois la rubrique retirée. "
             "L'énoncé demande la rubrique elle-même."),
        ],
    )


# --- 3. Points de pourcentage contre pourcentage ---------------------------


def gen_points_contre_pourcents() -> Exercice:
    base, sous_groupe = random.choice(POPULATIONS)
    t1 = random.choice([4, 5, 6, 8, 10, 12, 15, 20])
    ecart = random.choice([1, 2, 3, 4, 5])
    t2 = t1 + ecart
    reponse = 100 * ecart / t1

    enonce = f"""
> La part des {sous_groupe} est passée de **{t1} %** à **{t2} %** en cinq ans.
>
> De combien cette part a-t-elle augmenté, **en pourcentage** (variation relative) ?
>
> *Attention : la question ne demande pas la variation en points de pourcentage.*
"""

    etapes = [
        Etape(
            "Identifier — deux façons de mesurer le même écart",
            f"L'écart brut vaut ${t2} - {t1} = {ecart}$ **points de pourcentage**. "
            "Mais la question porte sur la variation **relative** : de combien la part "
            "a-t-elle augmenté par rapport à ce qu'elle valait au départ ? La base "
            f"n'est plus 100, c'est **{t1}**.",
        ),
        Etape(
            "Calculer la variation relative",
            "On divise l'écart par la valeur de départ, puis on multiplie par 100.",
            rf"\frac{{{t2} - {t1}}}{{{t1}}} \times 100 = \frac{{{ecart}}}{{{t1}}} "
            rf"\times 100 = {reponse:.1f}\,\%",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur doit surprendre",
            f"Une hausse de {ecart} points sur une base de {t1} % donne "
            f"**{_fr(reponse)} %** d'augmentation relative. L'écart entre les deux "
            "nombres est normal, et c'est exactement ce qui rend la distinction "
            "importante : le même fait se raconte de deux manières très différentes.",
        ),
        Etape(
            "Interpréter — pourquoi les deux chiffres circulent",
            f"Un communiqué qui veut minimiser dira « +{ecart} points » ; un "
            f"communiqué qui veut alerter dira « +{_fr(reponse)} % ». Les deux sont "
            "exacts. Savoir lequel est employé, et sur quelle base, est une compétence "
            "de lecture critique autant que de calcul.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Variation relative",
        unite="%",
        tolerance=0.01,
        indice="La base de comparaison n'est pas 100, c'est la valeur de départ.",
        pieges=[
            (float(ecart),
             "Vous avez donné la variation en **points de pourcentage**. La question "
             "demandait la variation relative, dont la base est la valeur de départ "
             f"({t1} %), et non 100."),
            (100 * ecart / t2,
             "Vous avez divisé par la valeur d'**arrivée**. Une variation se rapporte "
             "toujours à la valeur de **départ**."),
            (100 * t2 / t1,
             "Vous avez calculé le rapport des deux valeurs, pas la variation. "
             "Il faut retrancher la situation initiale."),
        ],
    )


# --- 4. Remonter au total ---------------------------------------------------


def gen_remonter_total() -> Exercice:
    base, sous_groupe = random.choice(POPULATIONS)
    taux = random.choice([4, 5, 8, 10, 12, 15, 20, 25])
    total = random.choice([600, 800, 1200, 1500, 2400, 3000])
    effectif = int(round(total * taux / 100))
    reponse = float(total)

    enonce = f"""
> Dans une population, les {sous_groupe} représentent **{taux} %** de l'ensemble,
> soit **{effectif:,} personnes**.
>
> Quel est l'effectif **total** de cette population ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — l'inconnue est la base, pas la partie",
            "C'est le calcul inverse du précédent. On connaît la partie et le taux, on "
            "cherche le total. Écrire l'égalité de départ évite de se tromper de sens.",
            rf"\frac{{{taux}}}{{100}} \times T = {effectif}",
        ),
        Etape(
            "Calculer — isoler le total",
            f"On divise par $\\frac{{{taux}}}{{100}}$, ce qui revient à multiplier par "
            f"$\\frac{{100}}{{{taux}}}$.",
            rf"T = \frac{{{effectif}}}{{{taux}}} \times 100 = {total}",
        ),
        Etape(
            "Vérifier — refaire le calcul direct",
            f"${taux}$ % de ${total:,}$ vaut ${effectif:,}$. ✓ "
            "Toute remontée au total se vérifie en redescendant.".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter",
            "Ce calcul est celui qu'on fait à partir d'un chiffre de presse : un "
            "communiqué donne souvent un effectif et un taux sans le total, alors que "
            "c'est le total qui permet de comparer avec une autre source.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Effectif total",
        unite="personnes",
        tolerance=0.005,
        indice="Écrivez l'égalité avec le total comme inconnue, puis isolez-le.",
        pieges=[
            (effectif * taux / 100,
             "Vous avez appliqué le taux **à la partie**. Le taux porte sur le total, "
             "qui est justement l'inconnue."),
            (effectif * taux,
             "Vous avez multiplié par le taux sans diviser par 100 — et dans le "
             "mauvais sens."),
            (effectif / taux,
             "Il manque la multiplication par 100 : diviser par un pourcentage revient "
             "à multiplier par $\\frac{100}{p}$."),
        ],
    )


# --- 5. Part manquante d'une répartition -----------------------------------


def gen_part_manquante() -> Exercice:
    parts = random.sample([12, 15, 18, 20, 22, 25, 28], 3)
    while sum(parts) >= 95:
        parts = random.sample([12, 15, 18, 20, 22, 25, 28], 3)
    rubriques = random.sample(RUBRIQUES, 4)
    budget = random.choice([200, 250, 300, 400])
    taux_manquant = 100 - sum(parts)
    reponse = budget * taux_manquant / 100

    lignes = "\n".join(
        f"> - {r} : {p} %" for r, p in zip(rubriques[:3], parts)
    )

    enonce = f"""
> Le budget d'une collectivité, de **{budget} M€**, se répartit en quatre rubriques
> qui couvrent l'intégralité des dépenses :
>
{lignes}
> - {rubriques[3]} : **?**
>
> Quel montant, en millions d'euros, la rubrique **{rubriques[3]}** représente-t-elle ?
"""

    etapes = [
        Etape(
            "Identifier — une répartition complète fait 100 %",
            "Les quatre rubriques couvrent l'intégralité du budget : leurs parts "
            "s'additionnent donc à 100 %. C'est cette contrainte qui donne la part "
            "manquante, sans information supplémentaire.",
        ),
        Etape(
            "Calculer la part manquante",
            f"On additionne les trois parts connues, puis on complète à 100.",
            rf"100 - ({parts[0]} + {parts[1]} + {parts[2]}) = 100 - {sum(parts)} "
            rf"= {taux_manquant}\,\%",
        ),
        Etape(
            "Appliquer cette part au budget",
            "",
            rf"\frac{{{taux_manquant}}}{{100}} \times {budget} = {reponse:.2f}"
            rf"\ \text{{M€}}",
        ),
        Etape(
            "Vérifier — la somme des quatre montants",
            f"Les quatre montants valent "
            f"{', '.join(_fr(budget*p/100, 1) for p in parts)} et {_fr(reponse, 1)} "
            f"M€, dont la somme fait bien {budget} M€. ✓ "
            "Une répartition se vérifie toujours par sa somme.",
        ),
        Etape(
            "Interpréter",
            "Ce raisonnement — déduire l'inconnu d'une contrainte de total — est "
            "omniprésent dans la lecture de comptes publics, où les documents "
            "officiels omettent fréquemment une ligne que le lecteur doit reconstituer.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Montant « {rubriques[3]} »",
        unite="M€",
        tolerance=0.005,
        indice="Les quatre parts couvrent tout le budget : que doit valoir leur somme ?",
        pieges=[
            (float(taux_manquant),
             "Vous avez donné la **part en pourcentage**, pas le montant. Il reste à "
             f"l'appliquer aux {budget} M€."),
            (budget * sum(parts) / 100,
             "C'est le montant des trois rubriques **connues**, pas celui de la "
             "quatrième."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Proportion → pourcentage",
        "2️⃣ Appliquer un taux",
        "3️⃣ Points ou pourcents ?",
        "4️⃣ Remonter au total",
        "5️⃣ Part manquante",
    ]
)

with onglets[0]:
    st.subheader("Exprimer une part en pourcentage")
    executer("p3_proportion", gen_proportion)

with onglets[1]:
    st.subheader("Appliquer un taux à un montant")
    executer("p3_appliquer", gen_appliquer)

with onglets[2]:
    st.subheader("Points de pourcentage contre variation relative")
    executer("p3_points", gen_points_contre_pourcents)

with onglets[3]:
    st.subheader("Retrouver le total à partir d'une part")
    executer("p3_total", gen_remonter_total)

with onglets[4]:
    st.subheader("Compléter une répartition")
    executer("p3_manquante", gen_part_manquante)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°3 — Proportions et pourcentages · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
