"""Série S1 — Reprise : fonctions affines, offre et demande. Fil rouge D : Mélodia.

Variation sur trois axes (cf. `contextes.py`) : le **marché** étudié, la
**notation** ($D$ et $O$, $D$ et $S$, variable $p$ ou $x$) et la **forme** sous
laquelle les deux courbes sont données — deux formules, une formule et une
phrase, ou deux relevés de prix dont il faut déduire la pente.
"""

import random

import streamlit as st

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S1 | Offre et demande", page_icon="🎧", layout="wide")

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

### ⚠️ Le marché change, la méthode non
Les exercices se déroulent tantôt sur ce marché, tantôt sur celui des studios, des
places de festival ou des vélos reconditionnés ; l'offre peut s'appeler $O$ ou $S$,
et vous être donnée par une formule, par une phrase ou par deux relevés de prix.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 1")
    st.latex(r"f(p) = ap + b")
    st.markdown("**Équilibre**")
    st.latex(r"D(p) = O(p)")
    st.markdown("**Retrouver une pente à partir de deux points**")
    st.latex(r"a = \frac{f(p_2) - f(p_1)}{p_2 - p_1}")
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
        "« Si le prix augmente de 1 €, la quantité demandée baisse de 60 unités. » "
        "Deux unités, jamais un pourcentage."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


#: Les deux courbes changent de nom d'un énoncé à l'autre : $O$ à la française,
#: $S$ (supply) dans la littérature anglo-saxonne que les étudiants liront.
NOTATIONS_MARCHE = [("D", "O", "p"), ("D", "S", "p"), ("D", "O", "x"), ("Q_d", "Q_o", "p")]


# --- 1. Équilibre offre / demande ------------------------------------------


def gen_equilibre() -> Exercice:
    ctx = cx.tirer(cx.MARCHES)
    nom_d, nom_o, var = random.choice(NOTATIONS_MARCHE)
    pente_d = random.choice([40, 50, 60, 75])
    pente_o = random.choice([20, 30, 40])
    prix = random.choice([5, 6, 8, 10])
    base_o = random.choice([100, 150, 200])
    base_d = base_o + (pente_d + pente_o) * prix
    quantite = base_d - pente_d * prix
    presentation = random.choice(["formules", "phrase", "deux_points"])

    demande = rf"{nom_d}({var}) = {L(base_d)} - {pente_d}{var}"
    offre = rf"{nom_o}({var}) = {L(base_o)} + {pente_o}{var}"

    if presentation == "formules":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}) :
>
> - la demande s'écrit $ {demande} $ ;
> - l'offre s'écrit $ {offre} $.
>
> Les quantités sont exprimées en {ctx.unite_quantite}.
>
> Quel est le **prix d'équilibre** ?
"""
        lecture = "Les deux fonctions sont données : il n'y a qu'à les égaliser."
    elif presentation == "phrase":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}), la demande s'écrit
>
> $$ {demande} $$
>
> Du côté de l'offre, les vendeurs mettent sur le marché **{_fr(base_o, 0)}
> {ctx.unite_quantite}** lorsque le prix est nul, et **{pente_o}
> {ctx.unite_quantite} de plus par {ctx.unite_prix} supplémentaire**.
>
> Quel est le **prix d'équilibre** ?
"""
        lecture = (
            f"L'offre est décrite en français : une valeur de départ "
            f"(${L(base_o)}$) et une pente (${pente_o}$ par {ctx.unite_prix}). "
            f"C'est exactement ce que signifie $ {offre} $ — il faut savoir passer "
            "de la phrase à la formule."
        )
    else:
        p1, p2 = 2, 6
        d1_val, d2_val = base_d - pente_d * p1, base_d - pente_d * p2
        enonce = f"""
> **{_maj(ctx.sujet)}.** Deux relevés de la demande, au prix ${var}$ exprimé en
> {ctx.unite_prix} :
>
{chr(10).join('> ' + ligne for ligne in cx.tableau_latex(
    [f"Prix ${var}$", f"${p1}$", f"${p2}$"],
    [[f"Quantité demandée", f"${L(d1_val)}$", f"${L(d2_val)}$"]],
).splitlines())}
>
> La demande est **affine**. L'offre, elle, s'écrit $ {offre} $.
>
> Quel est le **prix d'équilibre** ?
"""
        lecture = (
            f"La demande n'est pas donnée sous forme de formule : il faut la "
            f"reconstruire. Sa pente vaut "
            f"$\\dfrac{{{L(d2_val)} - {L(d1_val)}}}{{{p2} - {p1}}} = {-pente_d}$, "
            f"et son ordonnée à l'origine ${L(base_d)}$ s'obtient en remontant au "
            f"prix nul. On retrouve $ {demande} $."
        )

    etapes = [
        Etape(
            "Identifier — l'équilibre égalise les deux quantités",
            f"{lecture} L'équilibre est l'intersection de deux droites, donc une "
            "équation du premier degré : toute la pré-rentrée suffit à la résoudre.",
            rf"{L(base_d)} - {pente_d}{var} = {L(base_o)} + {pente_o}{var}",
        ),
        Etape(
            "Résoudre",
            f"Les termes en ${var}$ passent du même côté. Attention au signe : les "
            f"deux pentes sont de signes contraires, donc leurs valeurs absolues "
            f"s'**additionnent** : ${pente_d} + {pente_o} = {pente_d + pente_o}$.",
            rf"{L(base_d - base_o)} = {pente_d + pente_o}\,{var} \iff "
            rf"{var} = \frac{{{L(base_d - base_o)}}}{{{pente_d + pente_o}}} "
            rf"= {prix}\ \text{{{ctx.unite_prix}}}",
        ),
        Etape(
            "Vérifier — les deux quantités coïncident",
            f"${nom_d}({prix}) = {L(quantite)}$ et "
            f"${nom_o}({prix}) = {L(base_o + pente_o * prix)}$ "
            f"{ctx.unite_quantite}. Identiques. ✓ Cette vérification coûte dix "
            "secondes et détecte toute erreur de signe.",
        ),
        Etape(
            "Interpréter — ce que l'équilibre décrit",
            f"À {prix} {ctx.unite_prix}, {_fr(quantite, 0)} {ctx.unite_quantite} sont "
            "échangées : ni pénurie ni invendus. Au-dessus de ce prix, l'offre excède "
            "la demande ; en dessous, c'est l'inverse. L'équilibre n'est pas un prix "
            "« juste », c'est simplement le seul où les deux plans sont compatibles.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(prix),
        etapes=etapes,
        libelle="Prix d'équilibre",
        unite=ctx.unite_prix,
        tolerance=1e-6,
        indice="Égalisez les deux expressions et résolvez.",
        pieges=[
            (
                float(base_d - base_o) / (pente_d - pente_o)
                if pente_d != pente_o
                else 0.0,
                "Les pentes sont de signes contraires : en les déplaçant du même côté, "
                f"leurs valeurs absolues s'**additionnent** (${pente_d} + {pente_o}$), "
                "elles ne se retranchent pas.",
            ),
            (
                float(quantite),
                f"C'est la **quantité** d'équilibre, en {ctx.unite_quantite}. L'énoncé "
                f"demande un prix, en {ctx.unite_prix}.",
            ),
        ],
    )


# --- 2. Lire les deux pentes (QCM) -----------------------------------------


def gen_pentes() -> Exercice:
    ctx = cx.tirer(cx.MARCHES)
    nom_d, nom_o, var = random.choice(NOTATIONS_MARCHE)
    pente_d = random.choice([40, 60, 75])
    pente_o = random.choice([20, 30, 40])
    base_d = random.choice([600, 900, 1_200])
    base_o = random.choice([100, 150])
    presentation = random.choice(["formules", "phrase"])

    unite_q = ctx.unite_quantite
    unite_p = ctx.unite_prix

    bonne = (
        f"Si le prix augmente de 1 {unite_p}, la quantité demandée baisse de "
        f"{pente_d} {unite_q} et la quantité offerte augmente de {pente_o} {unite_q}."
    )
    pourcentage = (
        f"Si le prix augmente de 1 {unite_p}, la demande baisse de {pente_d} % et "
        f"l'offre augmente de {pente_o} %."
    )
    niveau = (
        f"La demande vaut en moyenne {pente_d} {unite_q}, l'offre {pente_o} {unite_q}."
    )
    inverse = (
        f"Si la quantité demandée baisse de 1 {unite_q}, le prix augmente de "
        f"{pente_d} {unite_p}."
    )
    options = [bonne, pourcentage, niveau, inverse]
    random.shuffle(options)

    if presentation == "formules":
        enonce = f"""
> **{_maj(ctx.sujet)}.** La demande s'écrit $ {nom_d}({var}) = {L(base_d)} -
> {pente_d}{var} $ et l'offre $ {nom_o}({var}) = {L(base_o)} + {pente_o}{var} $,
> les quantités étant en {unite_q} et le prix en {unite_p}.
>
> Quelle est la bonne lecture des **deux pentes** ?
"""
    else:
        enonce = f"""
> **{_maj(ctx.sujet)}.** Une étude conclut : « chaque {unite_p} supplémentaire sur le
> prix {ctx.du_bien} retire {pente_d} {unite_q} à la demande, et en ajoute
> {pente_o} à l'offre ».
>
> Quelle formulation traduit **correctement** ces deux pentes ?
"""

    etapes = [
        Etape(
            "Identifier — une pente est une variation par unité",
            f"La pente répond à : « de combien la quantité varie-t-elle quand le prix "
            f"augmente d'**un {unite_p}** ? ». Ni un niveau, ni un pourcentage : une "
            "variation, avec deux unités.",
        ),
        Etape(
            "Lire chaque pente avec son signe",
            f"Demande : pente $-{pente_d}$, donc une **baisse** de {pente_d} {unite_q} "
            f"par {unite_p} supplémentaire. Offre : pente $+{pente_o}$, donc une "
            f"**hausse** de {pente_o} {unite_q}. Les signes opposés sont exactement ce "
            "qui fait que les deux courbes se croisent.",
        ),
        Etape(
            "Vérifier — l'unité de la pente",
            f"La pente s'exprime en **{unite_q} par {unite_p}**. Une interprétation en "
            "pourcentage change de grandeur : le pourcentage viendra plus tard, avec "
            "l'élasticité, et ce n'est pas la même chose.",
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
            (
                pourcentage,
                f"La pente s'exprime en {unite_q} par {unite_p}, **pas en pourcentage**.",
            ),
            (niveau, "Vous décrivez un **niveau**. La pente décrit une variation."),
            (
                inverse,
                "Les rôles sont inversés : la pente donne l'effet du **prix sur la "
                "quantité**.",
            ),
        ],
    )


# --- 3. Sur la courbe ou de la courbe ? (QCM) ------------------------------


def _chocs(ctx: cx.Contexte, courbe: str):
    """Chocs possibles, reconstruits sur le marché tiré.

    « sur » : le prix change, on glisse sur la courbe.
    « de »  : autre chose change, la courbe se déplace.
    """
    long_de_la_courbe = [
        f"{_maj(ctx.acteur)} augmente le prix {ctx.du_bien} de 2 {ctx.unite_prix}",
        f"une promotion de rentrée fait baisser le prix {ctx.du_bien}",
        f"une taxe fait monter le prix payé pour {ctx.le_bien}",
    ]
    if courbe == "demande":
        deplacement = [
            "le revenu moyen des acheteurs augmente nettement",
            f"un concurrent lance une offre gratuite qui remplace {ctx.le_bien}",
            f"une campagne de communication rend {ctx.le_bien} beaucoup plus attractif",
            "un produit de substitution devient nettement moins cher",
        ]
    else:
        deplacement = [
            "le coût de production augmente fortement",
            "une subvention publique allège les coûts de production",
            "une nouvelle technique de production double les rendements",
            "une norme impose un équipement supplémentaire aux producteurs",
        ]
    return [(c, "sur") for c in long_de_la_courbe] + [(c, "de") for c in deplacement]


def gen_deplacement() -> Exercice:
    ctx = cx.tirer(cx.MARCHES)
    courbe = random.choice(["demande", "offre"])
    choc, nature = random.choice(_chocs(ctx, courbe))

    de_la = "de la demande" if courbe == "demande" else "de l'offre"
    la_courbe = "la demande" if courbe == "demande" else "l'offre"
    le_long = f"On se déplace **le long** de la courbe {de_la}"
    deplacee = f"La courbe {de_la} **se déplace** tout entière"
    inchangee = f"Ni l'un ni l'autre : {la_courbe} est inchangée"

    bonne = le_long if nature == "sur" else deplacee
    options = [le_long, deplacee, inchangee]

    enonce = f"""
> **{_maj(ctx.sujet)}.** On observe le changement suivant :
>
> > *{choc}.*
>
> Que se passe-t-il sur le graphique **{de_la}** ?
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
                f"quantité {'demandée' if courbe == 'demande' else 'offerte'} est "
                "inchangée : la courbe reste la même, seul le point d'observation "
                "bouge dessus."
                if nature == "sur"
                else "Ici, ce n'est **pas** le prix qui change, mais un élément "
                "extérieur à la relation prix-quantité. À prix inchangé, la quantité "
                f"{'demandée' if courbe == 'demande' else 'offerte'} n'est plus la "
                "même : c'est toute la courbe qui se déplace."
            ),
        ),
        Etape(
            "Vérifier — le test décisif",
            "Demandez-vous : « à prix constant, la quantité "
            f"{'demandée' if courbe == 'demande' else 'offerte'} change-t-elle ? » "
            + (
                "Non — donc simple déplacement le long de la courbe. ✓"
                if nature == "sur"
                else "Oui — donc déplacement de la courbe elle-même. ✓"
            ),
        ),
        Etape(
            "Interpréter — pourquoi la confusion coûte cher",
            "Attribuer au prix une variation causée par un changement de coûts ou de "
            "préférences conduit à estimer une sensibilité au prix qui n'existe pas. "
            "C'est la faute d'analyse la plus fréquente dans l'usage appliqué de ces "
            "courbes, et elle produit des recommandations tarifaires erronées.",
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
            (
                deplacee if nature == "sur" else le_long,
                "Reposez-vous la question : "
                + (
                    "ici c'est le **prix** qui change, et le prix est déjà porté par "
                    "un axe — la courbe ne bouge pas."
                    if nature == "sur"
                    else "ici le prix ne change pas ; c'est la relation elle-même qui "
                    "est modifiée, donc la courbe entière."
                ),
            ),
            (
                inchangee,
                "Un changement se produit bien : soit le point observé, soit la courbe.",
            ),
        ],
    )


# --- 4. Signe d'un produit : quand le profit est-il positif ? --------------


def gen_profit_positif() -> Exercice:
    ctx = cx.tirer(cx.MARCHES)
    nom = random.choice(["\\pi", "B", "\\Pi"])
    var = random.choice(["q", "x"])
    seuil = random.choice([150, 180, 200, 250])
    prix_max = random.choice([40, 50, 60])
    pente = random.choice([0.1, 0.2, 0.25])
    racine_haute = prix_max / pente
    forme = random.choice(["standard", "inversee", "pente_factorisee"])

    if forme == "standard":
        expression = rf"({var} - {seuil})\,({L(prix_max)} - {L(pente)}\,{var})"
    elif forme == "inversee":
        expression = rf"({L(prix_max)} - {L(pente)}\,{var})\,({var} - {seuil})"
    else:
        # Même fonction, second facteur factorisé par la pente.
        expression = (
            rf"{L(pente)}\,({var} - {seuil})\,({L(racine_haute)} - {var})"
        )

    enonce = f"""
> **{_maj(ctx.sujet)}.** Le profit, en milliers d'euros, s'écrit
>
> $$ {nom}({var}) = {expression} $$
>
> où ${var}$ est la quantité vendue, en {ctx.unite_quantite}.
>
> À partir de quelle valeur de ${var}$ le profit devient-il **positif** ?
"""

    milieu = (seuil + racine_haute) / 2
    etapes = [
        Etape(
            "Identifier — la forme factorisée donne les racines",
            f"Le profit s'annule quand l'un des facteurs s'annule : "
            f"${var} = {seuil}$ ou ${var} = \\frac{{{L(prix_max)}}}{{{L(pente)}}} "
            f"= {L(racine_haute)}$. Développer ferait perdre cette information, qui "
            "est justement celle qu'on cherche."
            if forme != "pente_factorisee"
            else f"Les deux racines se lisent directement : ${var} = {seuil}$ et "
            f"${var} = {L(racine_haute)}$. Le facteur ${L(pente)}$ placé devant est "
            "un nombre **positif** : il ne change aucun signe, il ne fait que "
            "changer l'échelle.",
        ),
        Etape(
            "Étudier le signe de chaque facteur",
            f"$({var} - {seuil})$ est négatif avant ${seuil}$, positif après. Le "
            f"second facteur s'annule en ${L(racine_haute)}$ et change de signe là. "
            "Le produit est positif uniquement là où les deux facteurs ont le "
            "**même** signe.",
        ),
        Etape(
            "Vérifier — tester une valeur par zone",
            f"${nom}({seuil - 50}) = "
            f"{L((seuil - 50 - seuil) * (prix_max - pente * (seuil - 50)), 0)}$ "
            f"(négatif) · ${nom}({int(milieu)}) = "
            f"{L((milieu - seuil) * (prix_max - pente * milieu), 0)}$ (positif) · "
            f"${nom}({int(racine_haute) + 50}) = "
            f"{L((racine_haute + 50 - seuil) * (prix_max - pente * (racine_haute + 50)), 0)}$ "
            "(négatif). ✓ Trois tests suffisent : un par zone.",
        ),
        Etape(
            "Interpréter — deux seuils, pas un",
            f"Le profit est positif uniquement entre **{seuil}** et "
            f"**{_fr(racine_haute, 0)}** {ctx.unite_quantite}. En dessous, les coûts "
            "fixes ne sont pas couverts ; au-dessus, il faut tellement baisser le prix "
            "pour écouler la production que la marge s'effondre. Un intervalle de "
            "rentabilité borné des deux côtés est la situation normale, pas l'exception.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(seuil),
        etapes=etapes,
        libelle=f"Seuil bas ({ctx.unite_quantite})",
        tolerance=1e-6,
        indice="Les deux racines se lisent directement sur la forme factorisée.",
        pieges=[
            (
                float(racine_haute),
                "C'est la racine **haute**, au-delà de laquelle le profit redevient "
                "négatif. L'énoncé demande le seuil à partir duquel il devient positif.",
            ),
            (
                0.0,
                "Le profit n'est pas positif dès la première unité : il faut d'abord "
                "couvrir les coûts, ce que traduit le premier facteur.",
            ),
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
