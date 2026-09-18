"""Série S8 — La dérivation : point de vue local. Fil rouge G : l'atelier municipal."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S8 | Dérivation locale", page_icon="🔧", layout="wide")

q = sp.Symbol("q")

st.title("🔧 S8 — La dérivation : point de vue local")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer un **taux d'accroissement**, le faire tendre vers un **nombre dérivé**,
écrire l'**équation de la tangente**, et interpréter le tout comme un **coût
marginal**.

### 🧠 Le coût de l'unité suivante
La question de départ n'est pas mathématique : combien coûte la réparation
supplémentaire ? Le coût total ne répond pas — il augmente toujours. Ce qu'il faut,
c'est la **variation** du coût au voisinage du point où l'on se trouve. C'est
exactement ce que mesure le nombre dérivé.

### 🔧 Fil rouge G — L'atelier municipal de réparation
Son coût total est $C(q) = 40\\,000 + 35q + 0{,}02\\,q^2$, où $q$ est le nombre de
réparations.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 8")
    st.markdown("**Taux d'accroissement**")
    st.latex(r"\tau(h) = \frac{f(a+h) - f(a)}{h}")
    st.markdown("**Nombre dérivé**")
    st.latex(r"f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}")
    st.markdown("**Équation de la tangente en $a$**")
    st.latex(r"y = f'(a)(x - a) + f(a)")
    st.info(
        "**L'interprétation économique**\n\n"
        "$C'(q)$ est le **coût marginal** : ce que coûte approximativement "
        "l'unité suivante."
    )
    st.error(
        "**Niveau, variation totale, variation marginale**\n\n"
        "$C(q)$ : un niveau · $C(b) - C(a)$ : une variation totale · "
        "$C'(q)$ : une variation **par unité**."
    )

ATELIERS = [
    ("l'atelier municipal de réparation", "réparations"),
    ("le centre de tri", "lots traités"),
    ("la cuisine centrale", "repas"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Taux d'accroissement ------------------------------------------------


def gen_taux() -> Exercice:
    atelier, unite = random.choice(ATELIERS)
    fixe = random.choice([30_000, 40_000, 50_000])
    lineaire = random.choice([25, 35, 45])
    quad = random.choice([0.01, 0.02, 0.05])
    q0 = random.choice([200, 400, 600, 800])
    h = random.choice([100, 200, 50])

    C = fixe + lineaire * q + quad * q**2
    c0 = float(C.subs(q, q0))
    c1 = float(C.subs(q, q0 + h))
    reponse = (c1 - c0) / h

    enonce = f"""
> Pour **{atelier}**, le coût total de $q$ {unite} est
>
> $$ C(q) = {fixe:,} + {lineaire}q + {str(quad).replace('.', ',')}\\,q^2
>    \\qquad \\text{{(en euros)}} $$
>
> Calculez le **taux d'accroissement** du coût entre $q = {q0}$ et
> $q = {q0 + h}$ {unite}.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — un taux rapporte une variation à un écart",
            "La variation brute du coût ne suffit pas : elle dépend de la largeur de "
            "l'intervalle. Pour obtenir un coût **par unité**, il faut diviser par "
            "l'écart de quantité.",
            r"\tau = \frac{C(q_0 + h) - C(q_0)}{h}",
        ),
        Etape(
            "Calculer les deux coûts",
            f"$C({q0}) = {c0:,.0f}$ € et $C({q0 + h}) = {c1:,.0f}$ €."
            .replace(",", "\u202f"),
            rf"C({q0 + h}) - C({q0}) = {c1 - c0:.0f}\ \text{{€}}",
        ),
        Etape(
            "Former le rapport",
            "",
            rf"\tau = \frac{{{c1 - c0:.0f}}}{{{h}}} \approx {reponse:.2f}"
            rf"\ \text{{€ par {unite[:-1]}}}",
        ),
        Etape(
            "Vérifier — l'unité et l'ordre de grandeur",
            f"Le résultat s'exprime en **euros par {unite[:-1]}**, et vaut "
            f"{reponse:.2f} € — un peu plus que le coût unitaire de base "
            f"({lineaire} €), ce qui est cohérent avec le terme en $q^2$ qui alourdit "
            "le coût quand la production augmente. ✓",
        ),
        Etape(
            "Interpréter — « en moyenne » sur l'intervalle",
            f"Entre {q0} et {q0 + h} {unite}, chaque {unite[:-1]} supplémentaire a "
            f"coûté **{reponse:.2f} € en moyenne**. Le mot « en moyenne » est "
            "essentiel : le coût du premier et celui du dernier ne sont pas les "
            "mêmes. C'est cette imprécision que la dérivée viendra lever.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux d'accroissement",
        unite=f"€/{unite[:-1]}",
        tolerance=0.005,
        indice="Calculez les deux coûts, puis divisez leur écart par l'écart de "
        "quantité.",
        pieges=[
            (float(c1 - c0),
             f"C'est la **variation totale** du coût en euros. Il reste à la diviser "
             f"par les {h} {unite} d'écart."),
            (float(c1) / (q0 + h),
             "Vous avez calculé un **coût moyen** au point d'arrivée. Le taux "
             "d'accroissement porte sur la variation, pas sur le niveau."),
        ],
    )


# --- 2. Du taux au nombre dérivé -------------------------------------------


def gen_nombre_derive() -> Exercice:
    atelier, unite = random.choice(ATELIERS)
    fixe = random.choice([30_000, 40_000])
    lineaire = random.choice([25, 35, 45])
    quad = random.choice([0.01, 0.02, 0.05])
    q0 = random.choice([200, 400, 500, 800])
    reponse = lineaire + 2 * quad * q0

    enonce = f"""
> Pour **{atelier}**, le coût total est
>
> $$ C(q) = {fixe:,} + {lineaire}q + {str(quad).replace('.', ',')}\\,q^2 $$
>
> On montre que le taux d'accroissement entre $q_0$ et $q_0 + h$ vaut
>
> $$ \\tau(h) = {lineaire} + {2*quad} \\,q_0 + {str(quad).replace('.', ',')}\\,h $$
>
> Quel est le **nombre dérivé** $C'({q0})$, c'est-à-dire la limite de $\\tau(h)$
> quand $h \\to 0$ ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — faire tendre, ce n'est pas remplacer",
            "On ne peut pas poser $h = 0$ dans le rapport initial : le dénominateur "
            "s'annulerait. Mais après simplification, l'expression obtenue est "
            "parfaitement définie en 0, et c'est vers cette valeur que le taux tend.",
        ),
        Etape(
            "Observer terme par terme",
            f"Les deux premiers termes ne dépendent pas de $h$ : ils ne bougent pas. "
            f"Le terme ${quad}h$ devient aussi petit qu'on veut.",
            rf"\tau(1) = {lineaire + 2*quad*q0 + quad:.3f} \quad "
            rf"\tau(0{{,}}1) = {lineaire + 2*quad*q0 + quad*0.1:.4f} \quad "
            rf"\tau(0{{,}}01) = {lineaire + 2*quad*q0 + quad*0.01:.4f}",
        ),
        Etape(
            "Conclure",
            "",
            rf"C'({q0}) = {lineaire} + {2*quad} \times {q0} = {reponse:.2f}"
            rf"\ \text{{€ par {unite[:-1]}}}",
        ),
        Etape(
            "Vérifier — ce que devient la sécante",
            "Quand $h$ diminue, le second point glisse vers le premier et la droite "
            "sécante **pivote**. Sa position limite est la **tangente**, et sa pente "
            f"vaut {reponse:.2f}. Le nombre dérivé n'est rien d'autre que cette pente.",
        ),
        Etape(
            "Interpréter — le coût marginal",
            f"À {q0} {unite}, la {unite[:-1]} suivante coûte environ "
            f"**{reponse:.2f} €**. C'est le **coût marginal**, et c'est ce nombre — "
            "et non le coût total, ni le coût moyen — qui détermine s'il vaut la "
            f"peine de produire davantage : il suffit de le comparer au prix facturé.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"C'({q0}) =",
        unite="€",
        tolerance=0.002,
        indice="Que devient chacun des trois termes quand $h$ s'approche de 0 ?",
        pieges=[
            (float(lineaire + 2 * quad * q0 + quad),
             "Vous avez posé $h = 1$ et non $h \\to 0$ : le terme en $h$ doit "
             "disparaître entièrement."),
            (float(lineaire),
             f"Vous avez oublié le terme ${2*quad}q_0$, qui dépend du point où l'on "
             "se place. Le coût marginal n'est pas constant."),
        ],
    )


# --- 3. Équation de la tangente ---------------------------------------------


def gen_tangente() -> Exercice:
    a = random.choice([0.02, 0.05, 0.1])
    b = random.choice([20, 35, 50])
    c = random.choice([10_000, 20_000, 40_000])
    q0 = random.choice([200, 300, 500])
    q1 = q0 + random.choice([50, 100, 150])

    C = a * q**2 + b * q + c
    Cp = sp.diff(C, q)
    pente = float(Cp.subs(q, q0))
    hauteur = float(C.subs(q, q0))
    reponse = pente * (q1 - q0) + hauteur

    enonce = f"""
> Le coût de l'atelier est $C(q) = {str(a).replace('.', ',')}\\,q^2 + {b}q + {c:,}$.
>
> On trace la **tangente** à cette courbe au point d'abscisse $q = {q0}$.
>
> Quelle est l'**ordonnée de cette tangente** pour $q = {q1}$ ?
""".replace(",", "\u202f")

    vraie = float(C.subs(q, q1))

    etapes = [
        Etape(
            "Identifier — une tangente est une droite, définie par deux données",
            f"Sa pente est $C'({q0})$ et elle passe par le point de la courbe "
            f"$({q0}\\,;\\,C({q0}))$. Ces deux informations la déterminent "
            "entièrement.",
            r"y = C'(a)(q - a) + C(a)",
        ),
        Etape(
            "Calculer les deux ingrédients",
            f"$C'(q) = {sp.latex(Cp)}$, donc $C'({q0}) = {pente:.2f}$. "
            f"Et $C({q0}) = {hauteur:,.0f}$ €.".replace(",", "\u202f"),
            rf"y = {pente:.2f}\,(q - {q0}) + {hauteur:.0f}",
        ),
        Etape(
            f"Évaluer en $q = {q1}$",
            "",
            rf"y = {pente:.2f} \times {q1 - q0} + {hauteur:.0f} \approx {reponse:.0f}"
            rf"\ \text{{€}}",
        ),
        Etape(
            "Vérifier — comparer à la courbe",
            f"La courbe elle-même vaut $C({q1}) = {vraie:,.0f}$ €, contre "
            f"{reponse:,.0f} € pour la tangente. L'écart de "
            f"{abs(vraie - reponse):,.0f} € est normal : la tangente **approche** la "
            "courbe, exactement au point de contact, et s'en éloigne d'autant plus "
            "qu'on s'écarte. ✓".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — à quoi sert la tangente",
            "Remplacer une courbe par sa tangente est l'usage le plus courant de la "
            "dérivée hors des mathématiques : c'est ce que fait tout raisonnement du "
            "type « si on produit 50 unités de plus, cela coûtera environ… ». "
            "Valable localement, trompeur au-delà — et l'écart calculé ci-dessus "
            "chiffre précisément cette limite.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Ordonnée de la tangente en q = {q1}",
        unite="€",
        tolerance=0.002,
        indice="Écrivez l'équation de la tangente, puis remplacez $q$.",
        pieges=[
            (vraie,
             "Vous avez calculé la valeur de la **courbe**, pas celle de la tangente. "
             "Les deux ne coïncident qu'au point de contact."),
            (float(pente * q1 + hauteur),
             f"Vous avez oublié de retrancher $a = {q0}$ : l'équation est "
             "$C'(a)(q - a) + C(a)$."),
        ],
    )


# --- 4. Coût marginal contre coût de l'unité suivante (QCM) ----------------


def gen_marginal() -> Exercice:
    atelier, unite = random.choice(ATELIERS)
    q0 = random.choice([300, 500, 800])
    cm = random.choice([47, 55, 63, 71])
    prix = random.choice([100, 90, 60])

    if cm < prix:
        bonne = (
            f"La {unite[:-1]} suivante coûte environ {cm} € et rapporte {prix} € : "
            "il est avantageux de produire davantage."
        )
    else:
        bonne = (
            f"La {unite[:-1]} suivante coûte environ {cm} € et rapporte {prix} € : "
            "il n'est pas avantageux de produire davantage."
        )
    options = [
        f"La {unite[:-1]} suivante coûte environ {cm} € et rapporte {prix} € : "
        "il est avantageux de produire davantage.",
        f"La {unite[:-1]} suivante coûte environ {cm} € et rapporte {prix} € : "
        "il n'est pas avantageux de produire davantage.",
        f"Le coût total de l'atelier vaut {cm} € à ce niveau de production.",
        f"Chaque {unite[:-1]} coûte {cm} € en moyenne depuis le début.",
    ]
    random.shuffle(options)

    enonce = f"""
> Pour **{atelier}**, on a calculé le coût marginal au niveau de production
> $q = {q0}$ {unite} :
>
> $$ C'({q0}) = {cm} \\ \\text{{€}} $$
>
> Chaque {unite[:-1]} est facturée **{prix} €**.
>
> Quelle est la bonne lecture ?
"""

    etapes = [
        Etape(
            "Identifier — trois grandeurs à ne pas confondre",
            "$C(q)$ est un **niveau** (le coût total). $\\frac{C(q)}{q}$ est un "
            "**coût moyen**. $C'(q)$ est le coût de l'**unité suivante**. "
            "Les trois sont différents, et seule la troisième éclaire la décision de "
            "produire une unité de plus.",
        ),
        Etape(
            "Comparer au prix",
            f"La {unite[:-1]} suivante coûte environ {cm} € et rapporte {prix} €. "
            f"L'écart est de **{prix - cm:+} €** : produire une unité de plus "
            f"{'améliore' if cm < prix else 'dégrade'} donc le résultat.",
        ),
        Etape(
            "Vérifier — la validité de l'approximation",
            f"$C'({q0})$ est une valeur **locale** : elle vaut pour l'unité suivante, "
            "pas pour les cinq cents suivantes. Le coût marginal augmente avec la "
            "production, donc la conclusion peut s'inverser plus loin.",
        ),
        Etape(
            "Interpréter — la règle de décision",
            "Tant que le coût marginal reste inférieur au prix, produire davantage "
            "améliore le résultat ; dès qu'il le dépasse, c'est l'inverse. "
            "L'optimum est donc atteint quand les deux s'égalisent — c'est exactement "
            "ce que la séance 9 formalisera, et c'est la raison pour laquelle on "
            "raisonne sur la dérivée et non sur le coût total.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Lecture correcte",
        indice="Le coût marginal se compare au **prix**, pas au coût total.",
        pieges=[
            (f"Le coût total de l'atelier vaut {cm} € à ce niveau de production.",
             "Vous confondez le coût **marginal** et le coût **total**. "
             "Le total se chiffre en dizaines de milliers d'euros ici."),
            (f"Chaque {unite[:-1]} coûte {cm} € en moyenne depuis le début.",
             "C'est la définition du coût **moyen**, qui inclut la répartition des "
             "coûts fixes. Le coût marginal ne porte que sur l'unité suivante."),
            (f"La {unite[:-1]} suivante coûte environ {cm} € et rapporte {prix} € : "
             + ("il n'est pas avantageux de produire davantage."
                if cm < prix else "il est avantageux de produire davantage."),
             f"Comparez les deux nombres : {cm} € de coût contre {prix} € de recette. "
             f"L'écart est {'favorable' if cm < prix else 'défavorable'} à la "
             "production supplémentaire."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Taux d'accroissement",
        "2️⃣ Le nombre dérivé",
        "3️⃣ Équation de la tangente",
        "4️⃣ Lire un coût marginal",
    ]
)

with onglets[0]:
    st.subheader("Rapporter une variation à un écart")
    executer("s8_taux", gen_taux)

with onglets[1]:
    st.subheader("Quand les deux points se rapprochent")
    executer("s8_derive", gen_nombre_derive)

with onglets[2]:
    st.subheader("Approcher la courbe par sa tangente")
    executer("s8_tangente", gen_tangente)

with onglets[3]:
    st.subheader("Le coût de l'unité suivante")
    executer("s8_marginal", gen_marginal)

st.markdown("---")
st.caption(
    "Semestre — séance n°8 : La dérivation, point de vue local · "
    "Fil rouge G : l'atelier municipal de réparation · Sciences Po."
)
