"""Série P5 — Variations et coefficients multiplicateurs."""

import random

import streamlit as st

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P5 | Variations et coefficients", page_icon="📈", layout="wide")

st.title("📈 P5 — Variations et coefficients multiplicateurs")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Traduire un taux d'évolution en **coefficient multiplicateur**, enchaîner plusieurs
évolutions, revenir en arrière, et calculer un taux de variation entre deux valeurs.

### 🧠 L'idée centrale
Les taux **ne s'additionnent pas**, les coefficients **se multiplient**. Une hausse de
20 % suivie d'une baisse de 20 % ne ramène pas au point de départ : elle fait perdre
4 %. Tout le module tient dans cette phrase, et c'est elle qu'on vérifiera ici
autant de fois que nécessaire.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 5")
    st.latex(r"CM = 1 + \frac{t}{100}")
    st.markdown("Hausse de $t\\,\\%$ : $CM > 1$ · Baisse : $CM < 1$")
    st.markdown("**Évolutions successives**")
    st.latex(r"CM_{\text{global}} = CM_1 \times CM_2 \times \cdots")
    st.markdown("**Évolution réciproque**")
    st.latex(r"CM_r = \frac{1}{CM}")
    st.markdown("**Taux de variation**")
    st.latex(r"t = \frac{V_{\text{arrivée}} - V_{\text{départ}}}{V_{\text{départ}}} \times 100")
    st.error(
        "**L'erreur interdite**\n\n"
        "Additionner les taux. $+20\\,\\%$ puis $-20\\,\\%$ ne fait pas $0$, "
        "mais $-4\\,\\%$."
    )

GRANDEURS = [
    ("le nombre de bénéficiaires du dispositif", "bénéficiaires"),
    ("le budget de la rubrique culture", "milliers d'euros"),
    ("le nombre de logements sociaux", "logements"),
    ("la fréquentation des médiathèques", "visites"),
    ("les effectifs de l'école primaire", "élèves"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Taux vers coefficient multiplicateur -------------------------------


def gen_coefficient() -> Exercice:
    sens = random.choice(["hausse", "baisse"])
    taux = random.choice([3, 5, 8, 12, 15, 20, 25, 30, 40])
    signe = 1 if sens == "hausse" else -1
    cm = 1 + signe * taux / 100
    grandeur, _ = random.choice(GRANDEURS)

    enonce = f"""
> En un an, {grandeur} a connu une **{sens} de {taux} %**.
>
> Quel est le **coefficient multiplicateur** correspondant ?
> *(Donnez le coefficient lui-même, pas un pourcentage.)*
"""

    etapes = [
        Etape(
            "Identifier — pourquoi un coefficient plutôt qu'un taux",
            "Un taux décrit une évolution *relative* ; un coefficient dit par combien "
            "**multiplier** la valeur de départ. Le second se manipule beaucoup mieux, "
            "car il s'enchaîne par multiplication.",
        ),
        Etape(
            "Calculer — appliquer $CM = 1 + \\frac{t}{100}$",
            f"Une {sens} correspond à un taux "
            f"{'positif' if signe > 0 else 'négatif'} : $t = {signe * taux}$.",
            rf"CM = 1 + \frac{{{signe * taux}}}{{100}} = 1 {'+' if signe > 0 else '-'} "
            rf"{taux/100} = {cm:.4g}",
        ),
        Etape(
            "Vérifier — le coefficient est-il du bon côté de 1 ?",
            f"Une **{sens}** doit donner un coefficient "
            f"{'supérieur' if signe > 0 else 'inférieur'} à 1. "
            f"Ici ${cm:.4g}$, c'est cohérent. ✓ Un coefficient négatif, ou supérieur à "
            "2 pour une hausse modeste, signale toujours une erreur.",
        ),
        Etape(
            "Interpréter",
            f"Concrètement : multiplier par ${cm:.4g}$, c'est "
            f"{'conserver les 100 % initiaux et en ajouter ' + str(taux) if signe > 0 else 'ne garder que ' + str(100 - taux)} "
            "% de la valeur de départ. Le coefficient contient à la fois ce qui "
            "reste et ce qui change — c'est pourquoi il est plus complet que le taux.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=cm,
        etapes=etapes,
        libelle="Coefficient multiplicateur",
        tolerance=0.001,
        indice="Le coefficient vaut $1 + t/100$, avec $t$ négatif pour une baisse.",
        pieges=[
            (taux / 100,
             "Vous avez oublié le **1 +**. Sans lui, vous ne gardez que la variation "
             "et vous perdez la valeur initiale."),
            (1 - signe * taux / 100,
             f"Le sens est inversé : une {sens} donne un coefficient "
             f"{'supérieur' if signe > 0 else 'inférieur'} à 1."),
            (1 + signe * taux,
             "Le taux doit être divisé par 100 avant d'être ajouté à 1."),
        ],
    )


# --- 2. Évolutions successives ---------------------------------------------


def gen_successives() -> Exercice:
    t1 = random.choice([5, 10, 15, 20, 25, 30])
    t2 = random.choice([5, 10, 15, 20, 25])
    s1 = random.choice([1, -1])
    s2 = random.choice([1, -1])
    cm1, cm2 = 1 + s1 * t1 / 100, 1 + s2 * t2 / 100
    cm = cm1 * cm2
    reponse = (cm - 1) * 100
    grandeur, _ = random.choice(GRANDEURS)

    def mot(s):
        return "hausse" if s > 0 else "baisse"

    enonce = f"""
> {grandeur.capitalize()} a connu une **{mot(s1)} de {t1} %** la première année,
> puis une **{mot(s2)} de {t2} %** la seconde.
>
> Quel est le **taux d'évolution global** sur les deux années, en pourcentage ?
"""

    etapes = [
        Etape(
            "Identifier — les taux ne s'additionnent pas",
            f"La tentation est d'écrire ${s1*t1} + ({s2*t2}) = {s1*t1 + s2*t2}$ %. "
            "C'est faux : la seconde évolution ne porte pas sur la valeur initiale, "
            "mais sur la valeur **déjà modifiée** par la première.",
        ),
        Etape(
            "Passer par les coefficients",
            "Chaque évolution donne un coefficient ; l'évolution globale est leur "
            "**produit**.",
            rf"CM_1 = {cm1:.4g} \qquad CM_2 = {cm2:.4g} \qquad "
            rf"CM_{{\text{{global}}}} = {cm1:.4g} \times {cm2:.4g} = {cm:.5g}",
        ),
        Etape(
            "Revenir au taux",
            "On applique la relation inverse : $t = (CM - 1) \\times 100$.",
            rf"t = ({cm:.5g} - 1) \times 100 = {reponse:.2f}\,\%",
        ),
        Etape(
            "Vérifier — l'écart avec la somme naïve",
            f"La somme des taux donnerait ${s1*t1 + s2*t2}$ %, alors que le vrai "
            f"résultat est ${_fr(reponse)}$ %. L'écart vaut "
            f"${_fr(abs(reponse - (s1*t1 + s2*t2)))}$ point(s) : c'est exactement le "
            "terme croisé que l'addition oublie.",
        ),
        Etape(
            "Interpréter",
            "Cet écart est faible sur deux années et sur de petits taux, mais il "
            "s'accumule. Sur une série longue — une dette, un effectif, un prix — "
            "l'addition des taux finit par produire des conclusions franchement "
            "fausses.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux global",
        unite="%",
        tolerance=0.01,
        indice="Convertissez chaque évolution en coefficient, multipliez, puis "
        "revenez au taux.",
        pieges=[
            (float(s1 * t1 + s2 * t2),
             "Vous avez **additionné les taux**. C'est l'erreur centrale de la séance : "
             "la seconde évolution porte sur une valeur déjà modifiée."),
            (cm,
             "Vous avez donné le **coefficient global**, pas le taux. Il reste à "
             "retrancher 1 et à multiplier par 100."),
        ],
    )


# --- 3. Évolution réciproque -----------------------------------------------


def gen_reciproque() -> Exercice:
    sens = random.choice(["hausse", "baisse"])
    taux = random.choice([10, 20, 25, 40, 50])
    signe = 1 if sens == "hausse" else -1
    cm = 1 + signe * taux / 100
    cm_r = 1 / cm
    reponse = (cm_r - 1) * 100
    grandeur, _ = random.choice(GRANDEURS)

    enonce = f"""
> {grandeur.capitalize()} a connu une **{sens} de {taux} %**.
>
> Quel taux d'évolution faudrait-il appliquer ensuite pour **revenir exactement à la
> valeur de départ** ? Donnez ce taux en pourcentage (négatif pour une baisse).
"""

    etapes = [
        Etape(
            "Identifier — l'évolution réciproque n'est pas le taux opposé",
            f"Après une {sens} de {taux} %, appliquer "
            f"{'−' if signe > 0 else '+'}{taux} % ne ramène **pas** au point de départ, "
            "parce que le second taux s'applique à une base différente de la première.",
        ),
        Etape(
            "Utiliser $CM_r = \\dfrac{1}{CM}$",
            "Revenir en arrière, c'est annuler la multiplication : le coefficient "
            "réciproque est l'inverse du coefficient initial.",
            rf"CM = {cm:.4g} \qquad CM_r = \frac{{1}}{{{cm:.4g}}} = {cm_r:.5g}",
        ),
        Etape(
            "Revenir au taux",
            "",
            rf"t_r = ({cm_r:.5g} - 1) \times 100 = {reponse:.2f}\,\%",
        ),
        Etape(
            "Vérifier — enchaîner les deux coefficients",
            f"${cm:.4g} \\times {cm_r:.5g} = 1$ : on retrouve bien la valeur initiale. "
            "✓ C'est la définition même de la réciproque, et la seule vérification "
            "qui vaille.",
        ),
        Etape(
            "Interpréter",
            f"Une {sens} de {taux} % s'annule par une évolution de "
            f"${_fr(reponse)}$ %, et non de ${-signe*taux}$ %. L'asymétrie surprend, "
            "mais elle a des conséquences très concrètes : une baisse de budget de "
            "20 % demande une hausse de 25 % pour être rattrapée.",
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
             "Vous avez pris le **taux opposé**. Or les deux taux ne s'appliquent pas "
             "à la même base : il faut passer par l'inverse du coefficient."),
            (cm_r,
             "Vous avez donné le **coefficient réciproque**, pas le taux. "
             "Il reste $(CM_r - 1) \\times 100$."),
        ],
    )


# --- 4. Taux de variation entre deux valeurs -------------------------------


def gen_taux_variation() -> Exercice:
    grandeur, unite = random.choice(GRANDEURS)
    depart = random.choice([240, 320, 450, 600, 750, 1200])
    variation = random.choice([-0.25, -0.15, -0.08, 0.06, 0.12, 0.2, 0.35])
    arrivee = int(round(depart * (1 + variation)))
    reponse = 100 * (arrivee - depart) / depart

    enonce = f"""
> {grandeur.capitalize()} est passé de **{depart:,} {unite}** à
> **{arrivee:,} {unite}**.
>
> Quel est le **taux de variation** entre ces deux valeurs, en pourcentage ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — la base est la valeur de départ",
            "Un taux de variation se rapporte **toujours** à la situation initiale. "
            "Se tromper de base est l'erreur la plus fréquente, et elle produit un "
            "résultat plausible — donc difficile à repérer.",
        ),
        Etape(
            "Calculer la variation absolue, puis la rapporter",
            f"La variation absolue vaut ${arrivee} - {depart} = {arrivee - depart}$ "
            f"{unite}.",
            rf"t = \frac{{{arrivee} - {depart}}}{{{depart}}} \times 100 "
            rf"= \frac{{{arrivee - depart}}}{{{depart}}} \times 100 "
            rf"= {reponse:.2f}\,\%",
        ),
        Etape(
            "Vérifier — repasser par le coefficient",
            f"Le coefficient vaut $\\frac{{{arrivee}}}{{{depart}}} = "
            f"{arrivee/depart:.4g}$, donc un taux de "
            f"$({arrivee/depart:.4g} - 1) \\times 100 = {_fr(reponse)}$ %. ✓ "
            "Les deux chemins doivent donner le même nombre.",
        ),
        Etape(
            "Interpréter",
            f"Le signe porte l'essentiel de l'information : "
            f"{'une hausse' if reponse > 0 else 'une baisse'} de "
            f"${_fr(abs(reponse))}$ %. Notez qu'un même écart absolu donne un taux "
            "très différent selon la taille de la population de départ — c'est "
            "pourquoi les taux permettent de comparer ce que les effectifs ne "
            "permettent pas.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux de variation",
        unite="%",
        tolerance=0.02,
        indice="Variation divisée par la valeur de **départ**, puis × 100.",
        pieges=[
            (100 * (arrivee - depart) / arrivee,
             "Vous avez divisé par la valeur d'**arrivée**. La base d'un taux de "
             "variation est toujours la valeur de départ."),
            (100 * arrivee / depart,
             "Vous avez calculé le rapport des deux valeurs, pas la variation : "
             "il manque le retranchement de la situation initiale."),
            (float(arrivee - depart),
             "C'est la variation **absolue**, exprimée en "
             f"{unite}. La question demande un pourcentage."),
        ],
    )


# --- 5. Évolution sur n années ----------------------------------------------


def gen_evolution_longue() -> Exercice:
    grandeur, unite = random.choice(GRANDEURS)
    depart = random.choice([200, 400, 500, 800, 1000])
    taux = random.choice([2, 3, 4, 5, 6])
    annees = random.choice([5, 8, 10, 12])
    cm = 1 + taux / 100
    reponse = depart * cm**annees

    enonce = f"""
> {grandeur.capitalize()} vaut aujourd'hui **{depart:,} {unite}** et progresse de
> **{taux} % par an**, au même rythme chaque année.
>
> Quelle sera sa valeur dans **{annees} ans** ?
""".replace(",", "\u202f")

    lineaire = depart * (1 + annees * taux / 100)

    etapes = [
        Etape(
            "Identifier — une même évolution répétée est une puissance",
            f"Chaque année, la valeur est multipliée par le même coefficient "
            f"${cm}$. Après {annees} ans, elle a été multipliée {annees} fois par ce "
            "coefficient : c'est la définition d'une puissance.",
        ),
        Etape(
            "Poser le calcul",
            "",
            rf"V_{{{annees}}} = {depart} \times ({cm})^{{{annees}}}",
        ),
        Etape(
            "Calculer",
            f"$({cm})^{{{annees}}} \\approx {cm**annees:.4f}$.",
            rf"V_{{{annees}}} \approx {depart} \times {cm**annees:.4f} "
            rf"\approx {reponse:.1f}\ \text{{{unite}}}",
        ),
        Etape(
            "Vérifier — comparer à l'évolution linéaire",
            f"Si le même taux s'appliquait chaque année à la valeur **initiale**, on "
            f"obtiendrait {_fr(lineaire, 1)} {unite}. Le résultat correct "
            f"({_fr(reponse, 1)}) doit être **supérieur**, puisque la progression "
            "porte chaque année sur un montant plus élevé. ✓",
        ),
        Etape(
            "Interpréter",
            f"L'écart entre les deux calculs atteint déjà "
            f"{_fr(reponse - lineaire, 1)} {unite} en {annees} ans. C'est le mécanisme "
            "de l'intérêt composé, et c'est aussi celui de la dette publique : ce qui "
            "paraît négligeable sur un an devient structurant sur une décennie.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur dans {annees} ans",
        unite=unite,
        tolerance=0.004,
        indice="Le coefficient s'applique une fois par an : combien de fois au total ?",
        pieges=[
            (lineaire,
             f"Vous avez appliqué le taux {annees} fois à la valeur **initiale** "
             "(évolution linéaire). Or chaque année, le taux porte sur la valeur de "
             "l'année précédente — d'où une puissance."),
            (depart * cm,
             "Vous n'avez appliqué le coefficient qu'**une seule fois**."),
            (depart * (taux / 100) ** annees,
             "Le coefficient est $1 + t/100$, pas $t/100$ : sans le $1 +$, la valeur "
             "s'effondre au lieu de croître."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Taux → coefficient",
        "2️⃣ Évolutions successives",
        "3️⃣ Revenir en arrière",
        "4️⃣ Taux de variation",
        "5️⃣ Sur plusieurs années",
    ]
)

with onglets[0]:
    st.subheader("Du taux au coefficient multiplicateur")
    executer("p5_coefficient", gen_coefficient)

with onglets[1]:
    st.subheader("Enchaîner deux évolutions")
    executer("p5_successives", gen_successives)

with onglets[2]:
    st.subheader("L'évolution réciproque")
    executer("p5_reciproque", gen_reciproque)

with onglets[3]:
    st.subheader("Calculer un taux entre deux valeurs")
    executer("p5_variation", gen_taux_variation)

with onglets[4]:
    st.subheader("Répéter la même évolution")
    executer("p5_longue", gen_evolution_longue)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°5 — Variations et coefficients multiplicateurs · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
