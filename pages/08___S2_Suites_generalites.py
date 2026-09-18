"""Série S2 — Les suites : généralités. Fil rouge D : Mélodia."""

import random

import streamlit as st

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S2 | Suites : généralités", page_icon="🔢", layout="wide")

st.title("🔢 S2 — Les suites : généralités")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Lire une définition **par récurrence**, calculer des termes, passer à la **forme
explicite**, et déterminer les **variations** d'une suite.

### 🧠 Discret ou continu ?
Une suite n'est définie que pour des rangs **entiers** : elle se représente par un
nuage de points, jamais par une courbe continue. C'est la différence de nature avec
les fonctions de la séance 1, et elle a une conséquence pratique — on ne peut pas
« lire entre deux points ».

### 🎧 Fil rouge D — Mélodia
Mélodia comptait **12 400 abonnés** fin 2020. Deux scénarios sont envisagés :
**+900 abonnés par an**, ou **+8 % par an**.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 2")
    st.markdown("**Notation**")
    st.latex(r"u_n \quad \text{terme de rang } n")
    st.markdown("$n$ est le **rang**, $u_n$ est la **valeur**. Ne pas les confondre.")
    st.markdown("**Deux façons de définir une suite**")
    st.latex(r"\text{Récurrence : } u_{n+1} = f(u_n) \ \text{ et } \ u_0")
    st.latex(r"\text{Explicite : } u_n = g(n)")
    st.markdown("**Variations**")
    st.latex(r"u_{n+1} - u_n > 0 \;\Rightarrow\; \text{croissante}")
    st.info(
        "**Récurrence ou explicite ?**\n\n"
        "La récurrence donne le **mécanisme**, l'explicite donne l'**accès direct** "
        "à n'importe quel rang sans calculer les précédents."
    )
    st.error(
        "**Un nuage de points, pas une courbe**\n\n"
        "Une suite n'existe qu'aux rangs entiers. $u_{2{,}5}$ n'a pas de sens."
    )

CONTEXTES = [
    ("le nombre d'abonnés de Mélodia", "abonnés"),
    ("le nombre de dossiers en attente", "dossiers"),
    ("l'effectif des adhérents", "adhérents"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Lire une définition par récurrence ---------------------------------


def gen_recurrence() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    u0 = random.choice([12_400, 8_000, 15_000, 20_000])
    modele = random.choice(["affine", "multiplicatif"])
    rang = random.choice([3, 4, 5])

    if modele == "multiplicatif":
        coef = random.choice([1.05, 1.08, 1.12, 0.95])
        ajout = 0
        regle = rf"u_{{n+1}} = {coef} \times u_n"
        description = f"multiplié par ${coef}$"
    else:
        coef = 1
        ajout = random.choice([900, 1200, -600, 1500])
        regle = rf"u_{{n+1}} = u_n + {ajout}"
        description = f"augmenté de ${ajout}$"

    valeurs = [float(u0)]
    for _ in range(rang):
        valeurs.append(valeurs[-1] * coef + ajout)
    reponse = valeurs[rang]

    enonce = f"""
> On modélise {grandeur} par une suite définie **par récurrence** :
>
> $$ u_0 = {u0:,} \\qquad {regle} $$
>
> Calculez $u_{{{rang}}}$.
""".replace(",", "\u202f")

    detail = " · ".join(
        f"$u_{k} = {valeurs[k]:,.0f}$".replace(",", "\u202f")
        for k in range(rang + 1)
    )

    etapes = [
        Etape(
            "Identifier — une récurrence se déroule pas à pas",
            f"La définition ne donne pas $u_{{{rang}}}$ directement : elle dit comment "
            f"passer d'un terme au suivant. Chaque terme est le précédent "
            f"{description}. Il faut donc dérouler, dans l'ordre.",
        ),
        Etape(
            "Calculer les termes successifs",
            detail,
        ),
        Etape(
            "Vérifier — le sens de l'évolution",
            f"La suite est "
            f"**{'croissante' if reponse > u0 else 'décroissante'}**, ce qui est "
            f"cohérent avec la règle : "
            + ("le coefficient est supérieur à 1." if modele == "multiplicatif" and coef > 1
               else "le coefficient est inférieur à 1." if modele == "multiplicatif"
               else "on ajoute un nombre positif." if ajout > 0
               else "on ajoute un nombre négatif.")
            + " ✓",
        ),
        Etape(
            "Interpréter — la limite de la récurrence",
            f"Pour $u_{{{rang}}}$, dérouler quatre ou cinq lignes reste faisable. "
            "Pour $u_{40}$, ce serait absurde. C'est précisément la raison d'être de "
            "la **forme explicite**, objet de l'onglet suivant : elle donne "
            "n'importe quel rang sans calculer les précédents.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"u_{rang} =",
        unite=unite,
        tolerance=0.002,
        indice="Déroulez terme après terme, en partant de $u_0$.",
        pieges=[
            (valeurs[rang - 1],
             f"Vous vous êtes arrêté un cran trop tôt : c'est $u_{{{rang - 1}}}$. "
             f"Attention, il y a bien {rang} pas entre $u_0$ et $u_{{{rang}}}$."),
            (float(u0 * coef + ajout) if rang > 1 else 0.0,
             "Vous n'avez appliqué la règle qu'**une seule fois**."),
        ],
    )


# --- 2. Passer de la récurrence à l'explicite ------------------------------


def gen_explicite() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    u0 = random.choice([12_400, 9_000, 15_000])
    modele = random.choice(["arithmetique", "geometrique"])
    rang = random.choice([12, 15, 20, 25])

    if modele == "geometrique":
        taux = random.choice([5, 8, 10])
        coef = 1 + taux / 100
        regle = rf"u_{{n+1}} = {coef} \times u_n"
        explicite = rf"u_n = {u0} \times ({coef})^{{\,n}}"
        reponse = u0 * coef**rang
        naif = u0 + rang * (u0 * taux / 100)
        message_naif = (
            f"Vous avez ajouté {rang} fois la variation de la **première** année. "
            "Or un pourcentage porte chaque année sur la valeur courante."
        )
        commentaire = (
            f"Chaque année multiplie par le même coefficient ${coef}$. Après $n$ "
            f"années, on a multiplié $n$ fois : c'est une puissance. Le coefficient "
            "multiplicateur de la pré-rentrée réapparaît ici tel quel."
        )
    else:
        raison = random.choice([900, 1200, 1500])
        regle = rf"u_{{n+1}} = u_n + {raison}"
        explicite = rf"u_n = {u0} + {raison}\,n"
        reponse = float(u0 + rang * raison)
        naif = float(u0 + (rang - 1) * raison)
        message_naif = (
            f"Vous avez compté {rang - 1} pas. La suite commençant au rang 0, il y a "
            f"bien {rang} pas pour atteindre $u_{{{rang}}}$."
        )
        commentaire = (
            f"Chaque année ajoute la même quantité ${raison}$. Après $n$ années, on "
            "a ajouté $n$ fois cette quantité."
        )

    enonce = f"""
> {grandeur.capitalize()} suit la récurrence
>
> $$ u_0 = {u0:,} \\qquad {regle} $$
>
> Sans dérouler tous les termes, calculez **$u_{{{rang}}}$**.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — repérer le mécanisme",
            commentaire,
        ),
        Etape(
            "Écrire la forme explicite",
            "La forme explicite exprime $u_n$ **directement en fonction de $n$**, "
            "sans passer par les termes précédents.",
            explicite,
        ),
        Etape(
            "Substituer",
            "",
            rf"u_{{{rang}}} \approx {reponse:,.0f}".replace(",", "\\,"),
        ),
        Etape(
            "Vérifier — sur un petit rang",
            f"La formule doit redonner les premiers termes : pour $n = 0$, elle donne "
            f"bien ${u0:,}$. ✓ Tester la formule sur un rang connu est la seule "
            "vérification fiable d'un passage à l'explicite.".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — pourquoi les deux écritures coexistent",
            "La récurrence dit **ce qui se passe** d'une année à l'autre ; l'explicite "
            "permet de **projeter** à n'importe quel horizon. Une projection à 40 ans "
            "n'est possible que sous la seconde forme.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"u_{rang} =",
        unite=unite,
        tolerance=0.002,
        indice="Combien de fois la règle s'applique-t-elle entre le rang 0 et le "
        f"rang {rang} ?",
        pieges=[(naif, message_naif)],
    )


# --- 3. Variations d'une suite (QCM) ---------------------------------------


def gen_variations() -> Exercice:
    modele = random.choice(["croissante", "decroissante", "alternee"])
    u0 = random.choice([500, 800, 1000])

    if modele == "croissante":
        r = random.choice([40, 75, 120])
        termes = [u0 + k * r for k in range(5)]
        bonne = "La suite est croissante"
        justification = (
            f"La différence $u_{{n+1}} - u_n$ vaut ${r}$, constante et **positive** : "
            "chaque terme dépasse le précédent."
        )
    elif modele == "decroissante":
        r = random.choice([-40, -75, -120])
        termes = [u0 + k * r for k in range(5)]
        bonne = "La suite est décroissante"
        justification = (
            f"La différence $u_{{n+1}} - u_n$ vaut ${r}$, constante et **négative** : "
            "chaque terme est inférieur au précédent."
        )
    else:
        r = random.choice([150, 200])
        termes = [u0 + (r if k % 2 else -r) for k in range(5)]
        bonne = "La suite n'est ni croissante ni décroissante"
        justification = (
            "Les différences successives changent de signe : la suite monte, puis "
            "descend, puis remonte. Aucun des deux qualificatifs ne s'applique."
        )

    options = [
        "La suite est croissante",
        "La suite est décroissante",
        "La suite n'est ni croissante ni décroissante",
    ]

    liste = " · ".join(
        f"$u_{k} = {t:,.0f}$".replace(",", "\u202f") for k, t in enumerate(termes)
    )
    diffs = [termes[k + 1] - termes[k] for k in range(4)]

    enonce = f"""
> On relève les cinq premiers termes d'une suite :
>
> {liste}
>
> Que peut-on dire de ses **variations** ?
"""

    etapes = [
        Etape(
            "Identifier — la définition passe par la différence",
            "Une suite est croissante si $u_{n+1} - u_n > 0$ **pour tout $n$**. "
            "Le mot « pour tout » est essentiel : il ne suffit pas que ce soit vrai "
            "une fois.",
        ),
        Etape(
            "Calculer les différences successives",
            "Différences : "
            + ", ".join(f"${d:,.0f}$".replace(",", "\u202f") for d in diffs)
            + ".",
        ),
        Etape(
            "Vérifier — le signe est-il constant ?",
            justification,
        ),
        Etape(
            "Interpréter — attention aux mots",
            "« Croissante » ne veut pas dire « qui augmente beaucoup », mais « qui "
            "n'a jamais diminué ». Une suite qui gagne un abonné par an est "
            "croissante ; une suite qui en gagne mille puis en perd un ne l'est pas.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Variations",
        indice="Calculez les différences entre termes consécutifs et regardez "
        "leur signe.",
        pieges=[
            (o, "Recalculez les différences entre termes consécutifs : "
                + ", ".join(f"${d:,.0f}$".replace(",", "\u202f") for d in diffs) + ".")
            for o in options if o != bonne
        ],
    )


# --- 4. Rang ou valeur ? (QCM) ---------------------------------------------


def gen_notation() -> Exercice:
    u0 = random.choice([12_400, 9_500, 15_200])
    taux = random.choice([5, 8, 10])
    coef = 1 + taux / 100
    rang = random.choice([4, 6, 7])
    valeur = u0 * coef**rang
    annee = 2020 + rang

    bonne = (
        f"{rang} est le rang, soit l'année {annee} ; la valeur associée est "
        f"environ {valeur:,.0f} abonnés."
    ).replace(",", "\u202f")
    options = [
        bonne,
        f"{rang} est le nombre d'abonnés ; le rang est environ {valeur:,.0f}."
        .replace(",", "\u202f"),
        f"{rang} désigne l'année {rang}.",
        f"u_{rang} est la somme des {rang} premiers termes.",
    ]
    random.shuffle(options)

    enonce = f"""
> **Mélodia** comptait **{u0:,} abonnés fin 2020**, effectif noté $u_0$. La suite
> progresse de **{taux} % par an**.
>
> Que désignent respectivement **{rang}** et **$u_{{{rang}}}$** ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — deux objets de nature différente",
            "Le **rang** $n$ compte les étapes : c'est un entier sans unité. "
            "La **valeur** $u_n$ est la grandeur mesurée : ici un nombre d'abonnés. "
            "Les confondre rend toute la suite illisible.",
        ),
        Etape(
            "Situer le rang dans le temps",
            f"$u_0$ correspond à fin 2020. Le rang {rang} correspond donc à "
            f"**{annee}**, soit {rang} années plus tard.",
        ),
        Etape(
            "Calculer la valeur associée",
            "",
            rf"u_{{{rang}}} = {u0} \times ({coef})^{{{rang}}} "
            rf"\approx {valeur:,.0f}".replace(",", "\\,"),
        ),
        Etape(
            "Interpréter — pourquoi la convention compte",
            "Si l'on avait posé $u_1$ pour 2020, tous les rangs seraient décalés d'un "
            "cran et la formule changerait. Aucune convention n'est meilleure que "
            "l'autre, mais il faut dire laquelle on adopte — et s'y tenir jusqu'au "
            "bout du calcul.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation",
        indice="Lequel des deux nombres est un compteur, lequel est une grandeur ?",
        pieges=[
            (f"{rang} est le nombre d'abonnés ; le rang est environ {valeur:,.0f}."
             .replace(",", "\u202f"),
             "Les rôles sont inversés : le rang est le petit entier, la valeur est "
             "l'effectif."),
            (f"{rang} désigne l'année {rang}.",
             f"Le rang compte les années **depuis** $u_0$, qui correspond à 2020. "
             f"Le rang {rang} désigne donc {annee}."),
            (f"u_{rang} est la somme des {rang} premiers termes.",
             "$u_n$ est un **terme**, pas une somme. Les sommes de suites seront "
             "vues en séance 3."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Lire une récurrence",
        "2️⃣ Passer à l'explicite",
        "3️⃣ Variations",
        "4️⃣ Rang ou valeur ?",
    ]
)

with onglets[0]:
    st.subheader("Dérouler une suite pas à pas")
    executer("s2_recurrence", gen_recurrence)

with onglets[1]:
    st.subheader("Atteindre n'importe quel rang directement")
    executer("s2_explicite", gen_explicite)

with onglets[2]:
    st.subheader("Croissante, décroissante, ou ni l'un ni l'autre")
    executer("s2_variations", gen_variations)

with onglets[3]:
    st.subheader("Vocabulaire et notation")
    executer("s2_notation", gen_notation)

st.markdown("---")
st.caption(
    "Semestre — séance n°2 : Les suites, généralités · Fil rouge D : Mélodia · "
    "Sciences Po."
)
