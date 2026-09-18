"""Série S9 — Suites arithmétiques et géométriques."""

import math
import random

import streamlit as st

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S9 | Suites", page_icon="🔢", layout="wide")

st.title("🔢 S9 — Suites")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Distinguer une suite **arithmétique** d'une suite **géométrique**, calculer un terme
de rang quelconque sans itérer, et déterminer à partir de quel rang un seuil est
franchi.

### 🧠 La distinction qui organise tout
Une suite arithmétique **ajoute** toujours la même quantité ; une suite géométrique
**multiplie** toujours par le même nombre. C'est la même opposition qu'entre intérêts
simples et intérêts composés, entre croissance linéaire et exponentielle. Elle se
pose à chaque fois qu'une grandeur évolue par étapes.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 9")
    st.markdown("**Suite arithmétique** (raison $r$)")
    st.latex(r"u_{n+1} = u_n + r \qquad u_n = u_0 + n\,r")
    st.markdown("**Suite géométrique** (raison $q$)")
    st.latex(r"u_{n+1} = q\,u_n \qquad u_n = u_0 \times q^{\,n}")
    st.markdown("**Franchissement d'un seuil** (cas géométrique, $q > 1$)")
    st.latex(r"u_0\,q^{\,n} > S \iff n > \frac{\ln(S/u_0)}{\ln q}")
    st.error(
        "**Attention au rang initial**\n\n"
        "Si la suite commence à $u_0$, alors $u_n = u_0 + nr$.\n\n"
        "Si elle commence à $u_1$, alors $u_n = u_1 + (n-1)r$."
    )

CONTEXTES = [
    ("le nombre de places en crèche", "places"),
    ("le parc de véhicules du service", "véhicules"),
    ("le nombre d'adhérents de l'association", "adhérents"),
    ("le stock de dossiers en attente", "dossiers"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Terme d'une suite arithmétique -------------------------------------


def gen_arithmetique() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    u0 = random.choice([120, 250, 400, 650, 900])
    r = random.choice([-40, -25, -15, 20, 35, 50])
    n = random.choice([6, 8, 10, 12, 15])
    reponse = float(u0 + n * r)

    enonce = f"""
> {grandeur.capitalize()} vaut **{u0:,} {unite}** l'année 0, et évolue de
> **{r:+} {unite} chaque année**, toujours du même montant.
>
> Combien vaudra-t-il l'année **{n}** ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — arithmétique, car on ajoute toujours la même quantité",
            f"Chaque année, on ajoute ${r}$ {unite}, indépendamment du niveau atteint. "
            "C'est la définition d'une suite arithmétique, et cela suffit à choisir "
            "la formule.",
        ),
        Etape(
            "Appliquer $u_n = u_0 + n\\,r$",
            f"Il n'est pas nécessaire de calculer les {n} termes un par un : la "
            "formule explicite donne directement le terme cherché.",
            rf"u_{{{n}}} = {u0} + {n} \times ({r}) = {u0} + ({n*r}) = {reponse:.0f}",
        ),
        Etape(
            "Vérifier — le sens de l'évolution",
            f"La raison est {'positive' if r > 0 else 'négative'}, donc la suite est "
            f"{'croissante' if r > 0 else 'décroissante'} : le résultat "
            f"({reponse:.0f}) doit être {'supérieur' if r > 0 else 'inférieur'} à "
            f"{u0}. ✓",
        ),
        Etape(
            "Interpréter — la croissance est linéaire",
            f"En représentant $u_n$ en fonction de $n$, on obtiendrait une **droite** "
            f"de pente ${r}$. Une suite arithmétique est l'équivalent discret d'une "
            "fonction affine — même formule, même lecture de la pente.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur l'année {n}",
        unite=unite,
        tolerance=1e-6,
        indice="Combien de fois la raison s'ajoute-t-elle entre l'année 0 et "
        f"l'année {n} ?",
        pieges=[
            (float(u0 + (n - 1) * r),
             f"Vous avez appliqué la raison {n-1} fois. La suite commençant à $u_0$, "
             f"il y a bien {n} pas entre l'année 0 et l'année {n}."),
            (float(u0 * r),
             "Vous avez **multiplié** par la raison : c'est la formule d'une suite "
             "géométrique, pas arithmétique."),
        ],
    )


# --- 2. Terme d'une suite géométrique --------------------------------------


def gen_geometrique() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    u0 = random.choice([200, 500, 800, 1500])
    taux = random.choice([-8, -5, 4, 6, 10, 12])
    raison = 1 + taux / 100
    n = random.choice([5, 7, 9, 12])
    reponse = u0 * raison**n

    enonce = f"""
> {grandeur.capitalize()} vaut **{u0:,} {unite}** l'année 0 et évolue de
> **{taux:+} % par an**, au même taux chaque année.
>
> Combien vaudra-t-il l'année **{n}** ? Arrondissez à l'unité.
""".replace(",", "\u202f")

    arithmetique = u0 + n * (u0 * taux / 100)

    etapes = [
        Etape(
            "Identifier — géométrique, car on multiplie toujours par le même nombre",
            f"Un pourcentage s'applique à la valeur **courante**, pas à la valeur "
            f"initiale : chaque année, on multiplie par le même coefficient "
            f"${raison}$. C'est une suite géométrique.",
        ),
        Etape(
            "Appliquer $u_n = u_0 \\times q^{\\,n}$",
            "",
            rf"u_{{{n}}} = {u0} \times ({raison})^{{{n}}} "
            rf"\approx {u0} \times {raison**n:.5f} \approx {reponse:.0f}",
        ),
        Etape(
            "Vérifier — comparer au cas arithmétique",
            f"Si la même variation absolue s'était répétée chaque année, on aurait "
            f"obtenu {arithmetique:,.0f} {unite}. Le résultat géométrique "
            f"({reponse:,.0f}) est "
            f"{'supérieur' if reponse > arithmetique else 'inférieur'} : "
            f"{'les hausses se cumulent sur des bases croissantes' if taux > 0 else 'les baisses portent sur des bases décroissantes, donc elles ralentissent'}. ✓"
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter",
            f"La croissance géométrique est le pendant discret de l'exponentielle "
            f"de la séance 7. Sur {n} ans l'écart avec le cas linéaire reste modeste ; "
            "sur plusieurs décennies il devient décisif. C'est pourquoi les "
            "projections de long terme sont si sensibles au taux retenu.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur l'année {n}",
        unite=unite,
        tolerance=0.004,
        indice="Le coefficient multiplicateur s'applique une fois par an.",
        pieges=[
            (float(arithmetique),
             "Vous avez répété la **même variation absolue** chaque année. Or un "
             "pourcentage porte sur la valeur courante : le montant ajouté change "
             "d'une année à l'autre."),
            (float(u0 * raison),
             "Vous n'avez appliqué le coefficient qu'une seule fois."),
        ],
    )


# --- 3. Reconnaître le type de suite (QCM) ---------------------------------


def gen_reconnaitre() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    est_geometrique = random.choice([True, False])
    u0 = random.choice([100, 200, 400])

    if est_geometrique:
        raison = random.choice([1.5, 2, 0.5])
        termes = [u0 * raison**k for k in range(4)]
        bonne = "Géométrique : on multiplie toujours par le même nombre"
    else:
        # Raison choisie pour qu'aucun terme ne s'annule : les rapports doivent
        # rester calculables, sinon le test « géométrique ? » est impossible à mener.
        r = random.choice([30, 60, 75, -25])
        termes = [u0 + k * r for k in range(4)]
        while min(termes) <= 0:
            r = random.choice([30, 60, 75])
            termes = [u0 + k * r for k in range(4)]
        bonne = "Arithmétique : on ajoute toujours la même quantité"

    options = [
        "Arithmétique : on ajoute toujours la même quantité",
        "Géométrique : on multiplie toujours par le même nombre",
        "Ni l'une ni l'autre",
    ]

    liste = " · ".join(f"$u_{k} = {t:,.0f}$".replace(",", "\u202f")
                       for k, t in enumerate(termes))

    enonce = f"""
> On relève les quatre premières valeurs de {grandeur} :
>
> {liste}
>
> De quel type de suite s'agit-il ?
"""

    diffs = [termes[k + 1] - termes[k] for k in range(3)]
    rapports = [termes[k + 1] / termes[k] for k in range(3)]

    etapes = [
        Etape(
            "Identifier — deux tests à faire dans l'ordre",
            "On calcule d'abord les **différences** entre termes consécutifs. "
            "Si elles sont constantes, la suite est arithmétique. Sinon, on calcule "
            "les **rapports** : s'ils sont constants, elle est géométrique.",
        ),
        Etape(
            "Tester les différences",
            "Différences successives : "
            + ", ".join(f"${d:,.0f}$".replace(",", "\u202f") for d in diffs)
            + (" — constantes." if not est_geometrique else " — non constantes."),
        ),
        Etape(
            "Tester les rapports",
            "Rapports successifs : "
            + ", ".join(f"${r:.3g}$" for r in rapports)
            + (" — constants." if est_geometrique else " — non constants."),
        ),
        Etape(
            "Interpréter — ce que chaque type implique",
            "Une suite arithmétique traduit un mécanisme **additif** : un contingent "
            "fixe attribué chaque année, un versement constant. Une suite géométrique "
            "traduit un mécanisme **proportionnel** : un taux appliqué à un stock, une "
            "contagion. Identifier le mécanisme est souvent plus important que "
            "calculer le terme.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Type de suite",
        indice="Calculez les différences, puis les rapports entre termes consécutifs.",
        pieges=[
            ("Arithmétique : on ajoute toujours la même quantité" if est_geometrique
             else "Géométrique : on multiplie toujours par le même nombre",
             "Refaites les deux tests : "
             + ("les différences ne sont pas constantes ici."
                if est_geometrique else "les rapports ne sont pas constants ici.")),
            ("Ni l'une ni l'autre",
             "L'un des deux tests est concluant : reprenez les calculs de "
             "différences et de rapports."),
        ],
    )


# --- 4. Franchissement d'un seuil ------------------------------------------


def gen_seuil() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    u0 = random.choice([300, 500, 800])
    taux = random.choice([4, 6, 8, 10])
    raison = 1 + taux / 100
    facteur = random.choice([1.5, 2, 3])
    seuil = u0 * facteur
    n_exact = math.log(facteur) / math.log(raison)
    reponse = float(math.ceil(n_exact))

    enonce = f"""
> {grandeur.capitalize()} vaut **{u0:,} {unite}** l'année 0 et croît de
> **{taux} % par an**.
>
> À partir de quelle année dépassera-t-il **{seuil:,.0f} {unite}** ?
> Donnez le **premier rang entier** pour lequel le seuil est franchi.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — l'inconnue est le rang, donc l'exposant",
            "On cherche le plus petit $n$ tel que $u_n > S$. L'inconnue étant en "
            "exposant, le logarithme est l'outil obligé — exactement comme en "
            "séance 7.",
            rf"{u0} \times ({raison})^n > {seuil:.0f}",
        ),
        Etape(
            "Isoler la puissance puis appliquer le logarithme",
            "",
            rf"({raison})^n > {facteur} \iff n \ln({raison}) > \ln({facteur}) "
            rf"\iff n > \frac{{{math.log(facteur):.4f}}}{{{math.log(raison):.4f}}} "
            rf"\approx {n_exact:.3f}",
        ),
        Etape(
            "Conclure — passer au premier entier",
            f"Le rang doit être entier : le seuil est franchi à partir de "
            f"**n = {reponse:.0f}**. On arrondit **vers le haut**, puisque "
            f"$n = {reponse - 1:.0f}$ ne suffit pas encore.",
        ),
        Etape(
            "Vérifier — encadrer par les deux valeurs",
            f"$u_{{{reponse - 1:.0f}}} = {u0 * raison**(reponse-1):,.0f}$ "
            f"(sous le seuil) et $u_{{{reponse:.0f}}} = "
            f"{u0 * raison**reponse:,.0f}$ (au-dessus). ✓ "
            "Cette double vérification est indispensable : elle seule confirme le "
            "sens de l'arrondi.".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter",
            f"Il faut {reponse:.0f} ans pour que {grandeur} soit multiplié par "
            f"{facteur}. Ce type de question — « à partir de quand ? » — est la forme "
            "que prend le plus souvent une projection dans un débat de politique "
            "publique, plus parlante qu'un taux annuel.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Premier rang n",
        unite="ans",
        tolerance=1e-6,
        indice="Écrivez l'inéquation, appliquez le logarithme, puis arrondissez "
        "dans le bon sens.",
        pieges=[
            (float(math.floor(n_exact)),
             "Vous avez arrondi **vers le bas**. À ce rang, le seuil n'est pas encore "
             "franchi : pour un dépassement, on arrondit vers le haut."),
            (float(facteur - 1) * 100 / taux,
             "Vous avez raisonné en évolution linéaire. Le taux s'applique chaque "
             "année à la valeur courante, d'où le passage par le logarithme."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Suite arithmétique",
        "2️⃣ Suite géométrique",
        "3️⃣ Reconnaître le type",
        "4️⃣ Franchir un seuil",
    ]
)

with onglets[0]:
    st.subheader("Ajouter toujours la même quantité")
    executer("s9_arithmetique", gen_arithmetique)

with onglets[1]:
    st.subheader("Multiplier toujours par le même nombre")
    executer("s9_geometrique", gen_geometrique)

with onglets[2]:
    st.subheader("Arithmétique ou géométrique ?")
    executer("s9_reconnaitre", gen_reconnaitre)

with onglets[3]:
    st.subheader("À partir de quelle année ?")
    executer("s9_seuil", gen_seuil)

st.markdown("---")
st.caption(
    "Semestre — séance n°9 : Suites · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
