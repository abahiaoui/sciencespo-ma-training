"""Série S1 — Reprise : fonctions affines, offre et demande. Fil rouge D : Mélodia."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S1 | Offre et demande", page_icon="🎧", layout="wide")

p_, q = sp.symbols("p q")

st.title("🎧 S1 — Reprise : fonctions affines, offre et demande")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Retrouver un **équilibre** entre offre et demande, lire les deux pentes avec leurs
unités, distinguer un **déplacement sur la courbe** d'un **déplacement de la courbe**,
et étudier le **signe d'un produit de fonctions affines**.

### 🧠 La distinction la plus importante de la séance
Un changement de prix fait **glisser le long** de la courbe de demande. Un changement
d'autre chose — le catalogue, les revenus, un concurrent — **déplace la courbe
entière**. Confondre les deux conduit à attribuer au prix des effets qui n'en viennent
pas, ce qui est l'erreur d'analyse la plus commune en économie appliquée.

### 🎧 Fil rouge D — Mélodia
Plateforme de streaming musical. Au prix mensuel $p$ (en euros) : les utilisateurs
demandent $D(p) = 900 - 60p$ abonnements (en milliers), les plateformes sont prêtes à
en offrir $O(p) = 100 + 40p$. Le profit s'écrit
$\\pi(q) = (q - 200)(50 - 0{,}1q)$, en milliers d'euros.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 1")
    st.latex(r"f(p) = ap + b")
    st.markdown("**Équilibre**")
    st.latex(r"D(p) = O(p)")
    st.markdown("**Signe d'un produit**")
    st.markdown(
        "Un produit ne change de signe qu'en une **racine** d'un de ses facteurs. "
        "On repère les racines, puis on teste une valeur par zone."
    )
    st.error(
        "**Sur la courbe ou de la courbe ?**\n\n"
        "Le **prix** change → on se déplace **le long** de la courbe.\n\n"
        "Autre chose change → la **courbe se déplace**."
    )
    st.info(
        "**Lire une pente**\n\n"
        "« Si le prix augmente de 1 €, la demande baisse de 60 milliers "
        "d'abonnements. »"
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Équilibre offre / demande ------------------------------------------


def gen_equilibre() -> Exercice:
    d1 = random.choice([40, 50, 60, 75])
    o1 = random.choice([20, 30, 40])
    p_eq = random.choice([5, 6, 8, 10])
    o0 = random.choice([100, 150, 200])
    d0 = o0 + (d1 + o1) * p_eq
    reponse = float(p_eq)
    q_eq = d0 - d1 * p_eq

    enonce = f"""
> **Mélodia.** Au prix mensuel $p$ (en euros) :
>
> - les utilisateurs demandent $D(p) = {d0:,} - {d1}p$ abonnements (en milliers) ;
> - les plateformes sont prêtes à en offrir $O(p) = {o0} + {o1}p$.
>
> Quel est le **prix d'équilibre** ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — l'équilibre égalise les deux quantités",
            "Ce n'est pas une notion nouvelle : c'est l'intersection de deux droites, "
            "donc une équation du premier degré. Toute la pré-rentrée suffit à la "
            "résoudre.",
            rf"{d0} - {d1}p = {o0} + {o1}p",
        ),
        Etape(
            "Résoudre",
            f"Les termes en $p$ passent du même côté : ${d1}p + {o1}p = {d1 + o1}p$.",
            rf"{d0 - o0} = {d1 + o1}p \iff p = \frac{{{d0 - o0}}}{{{d1 + o1}}} "
            rf"= {p_eq}\ \text{{€}}",
        ),
        Etape(
            "Vérifier — les deux quantités coïncident",
            f"$D({p_eq}) = {q_eq}$ et $O({p_eq}) = {o0 + o1*p_eq}$ milliers "
            "d'abonnements. Identiques. ✓",
        ),
        Etape(
            "Interpréter — ce que l'équilibre décrit",
            f"À {p_eq} €, {q_eq} milliers d'abonnements sont échangés : ni pénurie ni "
            "invendus. Au-dessus de ce prix, l'offre excède la demande ; en dessous, "
            "c'est l'inverse. L'équilibre n'est pas un prix « juste », c'est "
            "simplement le seul où les deux plans sont compatibles.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Prix d'équilibre",
        unite="€",
        tolerance=1e-6,
        indice="Égalisez les deux expressions et résolvez.",
        pieges=[
            (float(d0 - o0) / (d1 - o1) if d1 != o1 else 0.0,
             "Les pentes sont de signes contraires : en les déplaçant du même côté, "
             f"leurs valeurs absolues s'**additionnent** (${d1} + {o1}$)."),
            (float(q_eq),
             "C'est la **quantité** d'équilibre, pas le prix. L'énoncé demande un "
             "prix, en euros."),
        ],
    )


# --- 2. Lire les deux pentes (QCM) -----------------------------------------


def gen_pentes() -> Exercice:
    d1 = random.choice([40, 60, 75])
    o1 = random.choice([20, 30, 40])

    bonne = (
        f"Si le prix augmente de 1 €, la demande baisse de {d1} milliers "
        f"d'abonnements et l'offre augmente de {o1} milliers."
    )
    options = [
        bonne,
        f"Si le prix augmente de 1 €, la demande baisse de {d1} % et l'offre "
        f"augmente de {o1} %.",
        f"La demande vaut {d1} milliers d'abonnements en moyenne, l'offre {o1}.",
        f"Si la demande baisse de 1 millier, le prix augmente de {d1} €.",
    ]
    random.shuffle(options)

    enonce = f"""
> **Mélodia.** La demande s'écrit $D(p) = 900 - {d1}p$ et l'offre
> $O(p) = 100 + {o1}p$, les quantités étant en milliers d'abonnements et le prix
> en euros.
>
> Quelle est la bonne lecture des **deux pentes** ?
"""

    etapes = [
        Etape(
            "Identifier — une pente est une variation par unité",
            "La pente répond à : « de combien la quantité varie-t-elle quand le prix "
            "augmente d'**un euro** ? ». Ni un niveau, ni un pourcentage : une "
            "variation, avec deux unités.",
        ),
        Etape(
            "Lire chaque pente avec son signe",
            f"Demande : pente $-{d1}$, donc une **baisse** de {d1} milliers "
            f"d'abonnements par euro supplémentaire. Offre : pente $+{o1}$, donc une "
            f"**hausse** de {o1} milliers. Les signes opposés sont exactement ce qui "
            "fait que les deux courbes se croisent.",
        ),
        Etape(
            "Vérifier — l'unité de la pente",
            f"La pente s'exprime en **milliers d'abonnements par euro**. Une "
            "interprétation en pourcentage change de grandeur : le pourcentage "
            "viendra plus tard, avec l'élasticité, et ce n'est pas la même chose.",
        ),
        Etape(
            "Interpréter — ne pas inverser les rôles",
            "La pente se lit toujours « variation de la quantité pour une unité de "
            "prix », dans cet ordre. L'inverser reviendrait à traiter la quantité "
            "comme la variable explicative, ce que le modèle ne dit pas.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Lecture correcte",
        indice="Quelles sont les deux unités de la pente ?",
        pieges=[
            (f"Si le prix augmente de 1 €, la demande baisse de {d1} % et l'offre "
             f"augmente de {o1} %.",
             "La pente s'exprime en milliers d'abonnements par euro, **pas en "
             "pourcentage**."),
            (f"La demande vaut {d1} milliers d'abonnements en moyenne, l'offre {o1}.",
             "Vous décrivez un **niveau**. La pente décrit une variation."),
            (f"Si la demande baisse de 1 millier, le prix augmente de {d1} €.",
             "Les rôles sont inversés : la pente donne l'effet du **prix sur la "
             "quantité**."),
        ],
    )


# --- 3. Sur la courbe ou de la courbe ? (QCM) ------------------------------


CHOCS = [
    ("Mélodia augmente son prix mensuel de 2 €", "sur"),
    ("Mélodia enrichit fortement son catalogue", "de"),
    ("Un concurrent lance une offre gratuite financée par la publicité", "de"),
    ("Le revenu moyen des utilisateurs augmente", "de"),
    ("Mélodia baisse son prix pour la rentrée", "sur"),
    ("Une promotion temporaire ramène le prix à 4 €", "sur"),
]


def gen_deplacement() -> Exercice:
    choc, nature = random.choice(CHOCS)

    bonne = (
        "On se déplace **le long** de la courbe de demande"
        if nature == "sur"
        else "La courbe de demande **se déplace** tout entière"
    )
    options = [
        "On se déplace **le long** de la courbe de demande",
        "La courbe de demande **se déplace** tout entière",
        "Ni l'un ni l'autre : la demande est inchangée",
    ]

    enonce = f"""
> **Mélodia.** On observe le changement suivant :
>
> > *{choc}.*
>
> Que se passe-t-il sur le graphique de la demande ?
"""

    etapes = [
        Etape(
            "Identifier — la seule question à se poser",
            "Est-ce **le prix** qui change, ou autre chose ? Le prix est la variable "
            "portée par l'axe du graphique : quand il change, on se contente de "
            "glisser le long de la courbe existante.",
        ),
        Etape(
            "Analyser le changement",
            (
                "Ici, c'est bien le **prix** qui varie. La relation entre prix et "
                "quantité demandée, elle, est inchangée : la courbe reste la même, "
                "seul le point d'observation bouge dessus."
                if nature == "sur" else
                "Ici, ce n'est **pas** le prix qui change, mais un élément extérieur "
                "au modèle. À prix inchangé, la quantité demandée n'est plus la "
                "même : c'est toute la courbe qui se déplace."
            ),
        ),
        Etape(
            "Vérifier — le test décisif",
            "Demandez-vous : « à prix constant, la quantité demandée change-t-elle ? » "
            + ("Non — donc simple déplacement le long de la courbe. ✓"
               if nature == "sur" else
               "Oui — donc déplacement de la courbe elle-même. ✓"),
        ),
        Etape(
            "Interpréter — pourquoi la confusion coûte cher",
            "Attribuer au prix une variation causée par un changement de catalogue "
            "conduit à estimer une sensibilité au prix qui n'existe pas. C'est la "
            "faute d'analyse la plus fréquente dans l'usage appliqué de ces courbes, "
            "et elle produit des recommandations tarifaires erronées.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Effet graphique",
        indice="Est-ce le prix qui change, ou autre chose ?",
        pieges=[
            ("La courbe de demande **se déplace** tout entière" if nature == "sur"
             else "On se déplace **le long** de la courbe de demande",
             "Reposez-vous la question : "
             + ("ici c'est le **prix** qui change, et le prix est déjà en abscisse — "
                "la courbe ne bouge pas."
                if nature == "sur" else
                "ici le prix ne change pas ; c'est la relation elle-même qui est "
                "modifiée, donc la courbe entière.")),
            ("Ni l'un ni l'autre : la demande est inchangée",
             "Un changement se produit bien : soit le point observé, soit la courbe."),
        ],
    )


# --- 4. Signe d'un produit : quand le profit est-il positif ? --------------


def gen_profit_positif() -> Exercice:
    seuil = random.choice([150, 180, 200, 250])
    prix_max = random.choice([40, 50, 60])
    pente = random.choice([0.1, 0.2, 0.25])
    q_max = prix_max / pente  # seconde racine
    reponse = float(seuil)

    enonce = f"""
> **Mélodia.** Le profit, en milliers d'euros, s'écrit
>
> $$ \\pi(q) = (q - {seuil})\\,({prix_max} - {str(pente).replace('.', ',')}\\,q) $$
>
> où $q$ est le nombre d'abonnements, en milliers.
>
> À partir de quelle valeur de $q$ le profit devient-il **positif** ?
"""

    etapes = [
        Etape(
            "Identifier — la forme factorisée donne les racines",
            f"Le profit s'annule quand l'un des facteurs s'annule : "
            f"$q = {seuil}$ ou $q = \\frac{{{prix_max}}}{{{pente}}} = {q_max:.0f}$. "
            "Développer ferait perdre cette information, qui est justement celle "
            "qu'on cherche.",
        ),
        Etape(
            "Étudier le signe de chaque facteur",
            f"$(q - {seuil})$ est négatif avant ${seuil}$, positif après. "
            f"$({prix_max} - {pente}q)$ est positif avant ${q_max:.0f}$, négatif "
            "après. Le produit est donc positif uniquement là où les deux facteurs "
            "ont le même signe.",
        ),
        Etape(
            "Vérifier — tester une valeur par zone",
            f"$\\pi({seuil - 50}) = "
            f"{(seuil-50-seuil)*(prix_max-pente*(seuil-50)):.0f}$ (négatif) · "
            f"$\\pi({int((seuil + q_max)/2)}) = "
            f"{((seuil+q_max)/2-seuil)*(prix_max-pente*(seuil+q_max)/2):.0f}$ "
            f"(positif) · $\\pi({int(q_max) + 50}) = "
            f"{(q_max+50-seuil)*(prix_max-pente*(q_max+50)):.0f}$ (négatif). ✓",
        ),
        Etape(
            "Interpréter — deux seuils, pas un",
            f"Le profit est positif uniquement entre **{seuil}** et "
            f"**{q_max:.0f}** milliers d'abonnements. En dessous, les coûts fixes ne "
            "sont pas couverts ; au-dessus, il faut tellement baisser le prix pour "
            "écouler les abonnements que la marge s'effondre. "
            "Un intervalle de rentabilité borné des deux côtés est la situation "
            "normale, pas l'exception.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Seuil bas (milliers d'abonnements)",
        tolerance=1e-6,
        indice="Les deux racines se lisent directement sur la forme factorisée.",
        pieges=[
            (float(q_max),
             "C'est la racine **haute**, au-delà de laquelle le profit redevient "
             "négatif. L'énoncé demande le seuil à partir duquel il devient positif."),
            (0.0,
             "Le profit n'est pas positif dès la première unité : il faut d'abord "
             "couvrir les coûts, ce que traduit le premier facteur."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Prix d'équilibre",
        "2️⃣ Lire les deux pentes",
        "3️⃣ Sur la courbe ou de la courbe ?",
        "4️⃣ Quand le profit est-il positif ?",
    ]
)

with onglets[0]:
    st.subheader("Offre égale demande")
    executer("s1_equilibre", gen_equilibre)

with onglets[1]:
    st.subheader("Interpréter les pentes avec leurs unités")
    executer("s1_pentes", gen_pentes)

with onglets[2]:
    st.subheader("La distinction la plus importante de la séance")
    executer("s1_deplacement", gen_deplacement)

with onglets[3]:
    st.subheader("Signe d'un produit de fonctions affines")
    executer("s1_profit", gen_profit_positif)

st.markdown("---")
st.caption(
    "Semestre — séance n°1 : Reprise, fonctions affines, offre et demande · "
    "Fil rouge D : Mélodia · Sciences Po."
)
